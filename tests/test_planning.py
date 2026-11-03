import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import study
from test_study import ledger

ROOT = Path(__file__).resolve().parents[1]


def event(topic, result='correct', hint=0, purpose='explore', identifier='event-1'):
    return {'id': identifier, 'topic_id': topic, 'purpose': purpose, 'result': result,
            'hint_level': hint, 'record_ref': 'sessions/real-response.json'}


def add_topic(data, tid, **changes):
    topic = copy.deepcopy(data['topics'][0])
    topic.update(id=tid, **changes)
    data['topics'].append(topic)
    return topic


class PlanningTests(unittest.TestCase):
    def test_inventory_and_unknown_scope_precede_scoring(self):
        data = ledger()
        data['inventory_reviewed'] = False
        self.assertEqual(study.plan(data)['action'], 'reconcile_inventory')
        data['inventory_reviewed'] = True
        data['topics'][0]['scope'] = 'unknown'
        self.assertEqual(study.plan(data)['action'], 'resolve_scope')

    def test_unassessed_and_weak_are_different(self):
        data = ledger()
        add_topic(data, 'weak')
        data['observations'] = [event('weak', 'incorrect')]
        candidates = {x['topic_id']: x for x in study.plan(data)['candidates']}
        self.assertEqual(candidates['a']['purpose'], 'explore')
        self.assertEqual(candidates['weak']['purpose'], 'practice')

    def test_untaught_material_gets_teaching_not_a_graded_probe(self):
        data = ledger()
        data['topics'][0]['coverage'] = 'introduced'
        self.assertEqual(study.plan(data)['recommended']['purpose'], 'coverage')

    def test_hinted_success_is_uncertain_even_with_stale_strong_label(self):
        data = ledger()
        data['topics'][0].update(evidence='independent', evidence_ref='old-record')
        data['observations'] = [event('a', hint=3)]
        self.assertEqual(study.plan(data)['recommended']['purpose'], 'explore')

    def test_repeated_focus_eventually_revisits_other_eligible_topics(self):
        data = ledger()
        data['topics'][0]['importance'] = 'low'
        add_topic(data, 'weak', importance='high')
        data['observations'] = [event('weak', 'incorrect')]
        selected = []
        for index in range(10):
            next_item = study.plan(data)['recommended']
            selected.append(next_item['topic_id'])
            if next_item['topic_id'] == 'a':
                break
            data['observations'].append(event('weak', 'incorrect', purpose='practice', identifier=f'next-{index}'))
        self.assertIn('a', selected)

    def test_strong_topic_is_periodically_sampled_without_claiming_forgetting(self):
        data = ledger()
        data['topics'][0].update(evidence='independent', evidence_ref='old-record')
        add_topic(data, 'weak', evidence='guided', evidence_ref='response')
        data['observations'] = [event('a'), event('weak', 'incorrect', identifier='weak-start')]
        selected = []
        for index in range(12):
            candidate = study.plan(data)['recommended']
            selected.append(candidate['topic_id'])
            if candidate['topic_id'] == 'a':
                self.assertEqual(candidate['purpose'], 'refresh')
                break
            data['observations'].append(event('weak', 'incorrect', purpose='practice', identifier=f'repeat-{index}'))
        self.assertIn('a', selected)

    def test_plan_is_read_only_and_scores_are_explainable(self):
        data = ledger()
        before = copy.deepcopy(data)
        result = study.plan(data)
        self.assertEqual(data, before)
        for candidate in result['candidates']:
            self.assertEqual(candidate['score'], sum(candidate['terms'].values()))
        self.assertEqual(data['topics'][0]['evidence'], 'unknown')

    def test_no_automatic_exclusion_when_only_a_prerequisite_is_ready(self):
        data = ledger()
        add_topic(data, 'advanced', prerequisites=['a'])
        result = study.plan(data)
        self.assertEqual(result['recommended']['topic_id'], 'a')
        self.assertEqual(result['blocked'][0]['unmet_prerequisites'], ['a'])
        data['topics'][0].update(evidence='independent', evidence_ref='actual-response')
        self.assertFalse(study.plan(data)['blocked'])
        data['observations'] = [event('a', 'incorrect')]
        self.assertTrue(study.plan(data)['blocked'])

    def test_invalid_events_cycles_and_missing_dependencies_rejected(self):
        data = ledger()
        data['topics'][0]['prerequisites'] = ['missing']
        self.assertTrue(study.validate(data))
        data['topics'][0]['prerequisites'] = ['a']
        self.assertTrue(study.validate(data))
        data['topics'][0]['prerequisites'] = []
        for invalid in (event('missing'), event('a', hint=True), event('a', purpose='coverage')):
            data['observations'] = [invalid]
            self.assertTrue(study.validate(data))
        data['observations'] = [event('a'), event('a')]
        self.assertTrue(study.validate(data))

    def test_teaching_and_withdrawn_questions_do_not_erase_prior_failure(self):
        data = ledger()
        data['observations'] = [event('a', 'incorrect'),
                                event('a', 'not_assessed', purpose='coverage', identifier='teaching'),
                                event('a', 'ungradable', identifier='withdrawn')]
        self.assertEqual(study.plan(data)['recommended']['purpose'], 'practice')

    def test_legacy_ledgers_still_work_without_observations(self):
        self.assertEqual(study.validate(ledger()), [])
        self.assertEqual(study.plan(ledger())['recommended']['purpose'], 'explore')


class PortableBundleTests(unittest.TestCase):
    def test_bundle_works_when_copied_without_the_original_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'goal-learning'
            study.bundle(target)
            self.assertTrue((target / 'SKILL.md').is_file())
            self.assertFalse((target / 'courses').exists())
            self.assertFalse((target / 'private').exists())
            self.assertFalse((target / '.git').exists())
            for path in target.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if '://' not in link and not link.startswith('#'):
                        self.assertTrue((path.parent / link.split('#')[0]).exists(), (path, link))
            subprocess.run([sys.executable, str(target / 'study.py'), 'init', 'test-goal', '--title', 'Test', '--goal', 'Explain the method'], check=True, capture_output=True)
            self.assertTrue((target / 'courses/test-goal/course.json').exists())
            path = target / 'courses/test-goal/course.json'
            path.write_text(json.dumps(ledger()))
            output = subprocess.check_output([sys.executable, str(target / 'study.py'), 'plan', str(path)], text=True)
            self.assertEqual(json.loads(output)['recommended']['purpose'], 'explore')
            reexport = Path(temporary) / 'second-agent-skill'
            subprocess.run([sys.executable, str(target / 'study.py'), 'bundle', str(reexport)], check=True, capture_output=True)
            self.assertTrue((reexport / 'SKILL.md').is_file())
            self.assertFalse((reexport / 'courses').exists())
            with self.assertRaises(FileExistsError):
                study.bundle(target)

    def test_export_cannot_recurse_into_its_source(self):
        with self.assertRaises(ValueError):
            study.bundle(ROOT / 'exported')


if __name__ == '__main__':
    unittest.main()

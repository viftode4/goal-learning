import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import study

ROOT = Path(__file__).resolve().parents[1]


def ledger():
    return {'title': 'Test', 'goal': 'Explain a method independently',
            'success_criteria': ['Explain when to use it on an unseen task'],
            'inventory_reviewed': True,
            'sources': [{'id': 'lecture', 'location': 'Lecture outline'}],
            'topics': [{'id': 'a', 'title': 'Method', 'scope': 'included',
                        'source_refs': ['lecture: section 1'],
                        'coverage': 'worked_example', 'evidence': 'unknown',
                        'evidence_ref': '', 'practice_questions': []}]}


class CoverageTests(unittest.TestCase):
    def test_coverage_pass_does_not_promote_ability(self):
        data = ledger()
        before = copy.deepcopy(data)
        self.assertEqual(study.audit(data), [])
        self.assertEqual(data, before)
        self.assertEqual(data['topics'][0]['evidence'], 'unknown')

    def test_practice_paper_success_does_not_hide_other_topic(self):
        data = ledger()
        data['topics'][0].update(coverage='practiced', evidence='independent',
                                 evidence_ref='sessions/answer-1', practice_questions=['Q1'])
        extra = copy.deepcopy(data['topics'][0])
        extra.update(id='omitted', coverage='not_started', evidence='unknown',
                     evidence_ref='', practice_questions=[])
        data['topics'].append(extra)
        self.assertTrue(any('omitted' in e for e in study.audit(data)))

    def test_introduction_is_not_full_delivered_coverage(self):
        data = ledger()
        data['topics'][0]['coverage'] = 'introduced'
        self.assertTrue(study.audit(data))

    def test_inventory_must_be_explicitly_reviewed(self):
        data = ledger()
        data['inventory_reviewed'] = False
        self.assertTrue(study.audit(data))
        data['inventory_reviewed'] = 'true'
        self.assertTrue(study.validate(data))

    def test_unknown_scope_blocks(self):
        data = ledger()
        data['topics'][0]['scope'] = 'unknown'
        self.assertTrue(study.audit(data))

    def test_cannot_pass_by_excluding_everything(self):
        data = ledger()
        data['topics'][0].update(scope='excluded', exclusion_reason='Official announcement')
        self.assertTrue(study.audit(data))

    def test_exclusion_requires_reason(self):
        data = ledger()
        data['topics'][0]['scope'] = 'excluded'
        self.assertTrue(study.validate(data))

    def test_evidence_needs_record(self):
        data = ledger()
        data['topics'][0]['evidence'] = 'independent'
        self.assertTrue(study.validate(data))

    def test_sources_need_known_id_and_anchor(self):
        for ref in ('missing: p1', 'lecture', 'lecture: '):
            data = ledger()
            data['topics'][0]['source_refs'] = [ref]
            self.assertTrue(study.validate(data))

    def test_bad_types_and_duplicate_ids(self):
        for data in (None, [], {}, {'title': 'Only title'}):
            self.assertTrue(study.validate(data))
        data = ledger()
        data['topics'].append(copy.deepcopy(data['topics'][0]))
        self.assertTrue(study.validate(data))

    def test_malformed_enum_types_report_errors(self):
        for field in ('coverage', 'evidence'):
            data = ledger()
            data['topics'][0][field] = []
            self.assertTrue(study.validate(data))

    def test_missing_goal_criteria_blocks(self):
        data = ledger()
        data['success_criteria'] = []
        self.assertTrue(study.audit(data))

    def test_cli_and_rejected_path_traversal(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'course.json'
            path.write_text(json.dumps(ledger()))
            passed = subprocess.run([sys.executable, str(ROOT / 'study.py'), 'audit', str(path)], capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout)
            path.write_text('{invalid')
            failed = subprocess.run([sys.executable, str(ROOT / 'study.py'), 'audit', str(path)], capture_output=True, text=True)
            self.assertEqual(failed.returncode, 1)
        bad = subprocess.run([sys.executable, str(ROOT / 'study.py'), 'init', '../escape', '--title', 'Test', '--goal', 'Test'], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)


if __name__ == '__main__':
    unittest.main()

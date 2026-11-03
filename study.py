#!/usr/bin/env python3
"""Local goal ledger: initialize, report, and audit declared coverage."""
import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path

COVERAGE = {'not_started', 'introduced', 'worked_example', 'practiced'}
EVIDENCE = {'unknown', 'guided', 'independent', 'transferable', 'durable'}
STRONG_EVIDENCE = {'independent', 'transferable', 'durable'}
PURPOSES = ('coverage', 'explore', 'practice', 'refresh')
RESULTS = ('correct', 'partially_correct', 'incorrect', 'ungradable', 'not_assessed')


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data):
    """Validate metadata, not the truth of source or performance claims."""
    if not isinstance(data, dict):
        return ['Ledger must be a JSON object.']
    errors = []
    for field in ('title', 'goal'):
        if not nonempty(data.get(field)):
            errors.append(f'{field} must be a nonempty string.')
    criteria = data.get('success_criteria')
    if not isinstance(criteria, list) or not criteria or not all(map(nonempty, criteria)):
        errors.append('success_criteria must contain observable criteria.')
    if type(data.get('inventory_reviewed')) is not bool:
        errors.append('inventory_reviewed must be a boolean.')
    sources = data.get('sources')
    if not isinstance(sources, list) or not sources:
        errors.append('sources must be a nonempty list.')
        sources = []
    source_ids = set()
    for source in sources:
        if not isinstance(source, dict) or not nonempty(source.get('id')) or not nonempty(source.get('location')):
            errors.append('Each source needs id and location.')
            continue
        sid = source['id']
        if ':' in sid or sid in source_ids:
            errors.append(f'Invalid or duplicate source id: {sid}')
        source_ids.add(sid)
    topics = data.get('topics')
    if not isinstance(topics, list) or not topics:
        errors.append('topics must be a nonempty list.')
        topics = []
    ids = set()
    for topic in topics:
        if not isinstance(topic, dict):
            errors.append('Each topic must be an object.')
            continue
        tid = topic.get('id')
        if not nonempty(tid) or tid in ids:
            errors.append(f'Invalid or duplicate topic id: {tid}')
        if nonempty(tid):
            ids.add(tid)
        if not nonempty(topic.get('title')):
            errors.append(f'{tid}: title required.')
        if topic.get('scope') not in ('included', 'excluded', 'unknown'):
            errors.append(f'{tid}: invalid scope.')
        if not isinstance(topic.get('coverage'), str) or topic.get('coverage') not in COVERAGE:
            errors.append(f'{tid}: invalid coverage.')
        if not isinstance(topic.get('evidence'), str) or topic.get('evidence') not in EVIDENCE:
            errors.append(f'{tid}: invalid evidence.')
        if isinstance(topic.get('evidence'), str) and topic['evidence'] in EVIDENCE - {'unknown'} and not nonempty(topic.get('evidence_ref')):
            errors.append(f'{tid}: evidence_ref required for reported ability evidence.')
        refs = topic.get('source_refs')
        if not isinstance(refs, list) or not refs:
            errors.append(f'{tid}: source_refs required.')
        else:
            for ref in refs:
                if not nonempty(ref) or ':' not in ref or ref.split(':', 1)[0] not in source_ids or not ref.split(':', 1)[1].strip():
                    errors.append(f'{tid}: unknown source or missing section/page in reference {ref!r}.')
        if topic.get('scope') == 'excluded' and not nonempty(topic.get('exclusion_reason')):
            errors.append(f'{tid}: exclusion needs a reason and source reference.')
        questions = topic.get('practice_questions', [])
        if not isinstance(questions, list) or not all(map(nonempty, questions)):
            errors.append(f'{tid}: practice_questions must be a list of strings.')
        if topic.get('importance', 'normal') not in ('low', 'normal', 'high'):
            errors.append(f'{tid}: importance must be low, normal, or high.')
        prerequisites = topic.get('prerequisites', [])
        if not isinstance(prerequisites, list) or not all(map(nonempty, prerequisites)):
            errors.append(f'{tid}: prerequisites must be topic IDs.')
    if errors:
        return errors
    by_id = {t['id']: t for t in topics}
    for topic in topics:
        for dependency in topic.get('prerequisites', []):
            if dependency not in ids or by_id[dependency]['scope'] != 'included':
                errors.append(f"{topic['id']}: prerequisite {dependency!r} must be an included topic.")
    if errors:
        return errors
    visiting, visited = set(), set()

    def visit(tid):
        if tid in visiting:
            errors.append(f'{tid}: cyclic prerequisites.')
            return
        if tid in visited:
            return
        visiting.add(tid)
        for dependency in by_id[tid].get('prerequisites', []):
            visit(dependency)
        visiting.remove(tid)
        visited.add(tid)

    for tid in ids:
        visit(tid)
    observations = data.get('observations', [])
    if not isinstance(observations, list):
        return errors + ['observations must be a chronological list.']
    event_ids = set()
    for event in observations:
        if not isinstance(event, dict):
            errors.append('Each observation must be an object.')
            continue
        eid = event.get('id')
        if not nonempty(eid) or eid in event_ids:
            errors.append('Each observation needs a unique id.')
        if nonempty(eid):
            event_ids.add(eid)
        if not nonempty(event.get('topic_id')) or event['topic_id'] not in ids:
            errors.append(f'{eid}: unknown observation topic.')
        if event.get('purpose') not in PURPOSES or event.get('result') not in RESULTS:
            errors.append(f'{eid}: invalid observation purpose or result.')
        if event.get('purpose') == 'coverage' and event.get('result') != 'not_assessed':
            errors.append(f'{eid}: teaching coverage must use not_assessed, not a learner grade.')
        hints = event.get('hint_level')
        if type(hints) is not int or not 0 <= hints <= 5:
            errors.append(f'{eid}: hint_level must be an integer from 0 to 5.')
        if not nonempty(event.get('record_ref')):
            errors.append(f'{eid}: record_ref must locate the real response or teaching record.')
    return errors


def plan(data):
    """Recommend one activity without writing evidence or pretending to optimize learning."""
    errors = validate(data)
    if errors:
        raise ValueError('; '.join(errors))
    if not data['inventory_reviewed']:
        return {'action': 'reconcile_inventory', 'reason': 'Inspect the full source/task map before allocating topics.'}
    unresolved = [t['id'] for t in data['topics'] if t['scope'] == 'unknown']
    if unresolved:
        return {'action': 'resolve_scope', 'topics': unresolved,
                'reason': 'Unresolved scope cannot be silently discarded.'}
    included = {t['id']: t for t in data['topics'] if t['scope'] == 'included'}
    events = data.get('observations', [])
    latest, last_check = {}, {}
    for index, event in enumerate(events):
        # A worked example or ungradable question is not evidence of ability.
        if event['purpose'] != 'coverage' and event['result'] in ('correct', 'partially_correct', 'incorrect'):
            latest[event['topic_id']] = (index, event)
            last_check[event['topic_id']] = index
    candidates, blocked = [], []
    for tid, topic in included.items():
        unmet = [d for d in topic.get('prerequisites', [])
                 if included[d]['evidence'] not in STRONG_EVIDENCE
                 or (d in latest and (latest[d][1]['result'] != 'correct'
                                      or latest[d][1]['hint_level'] > 0))]
        if unmet:
            blocked.append({'topic_id': tid, 'unmet_prerequisites': unmet})
            continue
        recent = latest.get(tid)
        event = recent[1] if recent else None
        if topic['coverage'] in ('not_started', 'introduced'):
            purpose, need = 'coverage', 3
            reason = 'Required material still needs an explanation and complete example.'
        elif event and event['result'] in ('partially_correct', 'incorrect'):
            purpose, need = 'practice', 3
            reason = 'The latest graded response shows a specific weakness; repair it, then retry.'
        elif (topic['evidence'] not in STRONG_EVIDENCE or not event
              or event['hint_level'] > 0):
            purpose, need = 'explore', 2
            reason = 'Independent ability is uncertain; use a fresh, fair check of taught material.'
        else:
            purpose, need = 'refresh', 0
            reason = 'Sample apparently strong knowledge with a fresh check; no forgetting is assumed.'
        # Fresh teaching resets coverage recency, but it cannot replace an independent check.
        if purpose == 'coverage':
            appearances = [i for i, e in enumerate(events) if e['topic_id'] == tid]
            last_index = appearances[-1] if appearances else -1
        else:
            last_index = last_check.get(tid, -1)
        age = len(events) - last_index - 1
        importance = {'low': 1, 'normal': 2, 'high': 3}[topic.get('importance', 'normal')]
        candidates.append({'topic_id': tid, 'purpose': purpose,
                           'score': importance + need + age,
                           'terms': {'importance': importance, 'need': need,
                                     'intervening_observations': age}, 'reason': reason})
    candidates.sort(key=lambda c: (-c['score'], c['topic_id']))
    return {'action': 'study' if candidates else 'review_goal_scope',
            'recommended': candidates[0] if candidates else None,
            'candidates': candidates, 'blocked': blocked,
            'coverage_gaps': [t['id'] for t in included.values()
                              if t['coverage'] in ('not_started', 'introduced')],
            'limits': 'Heuristic scores are not probabilities, UCB bounds, or mastery. '
                      'No ledger changes. Elapsed observations are not elapsed days. '
                      'Inspect actual records and goal criteria before acting.'}


def bundle(destination):
    """Export only the reusable files; never copy personal learning records."""
    root = Path(__file__).resolve().parent
    destination = destination.resolve()
    if destination == root or root in destination.parents:
        raise ValueError('Export outside the source repository to avoid recursive or private copies.')
    destination.mkdir(parents=True, exist_ok=False)
    for name in ('README.md', 'AGENTS.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'LICENSE', '.gitignore', 'study.py', 'agent-index.json'):
        shutil.copyfile(root / name, destination / name)
    for name in ('docs', 'templates', 'examples', 'evals', 'THIRD_PARTY_NOTICES'):
        shutil.copytree(root / name, destination / name)
    skill_path = root / 'skills/goal-learning/SKILL.md'
    if not skill_path.exists():
        skill_path = root / 'SKILL.md'  # An exported skill can be exported again.
    skill = skill_path.read_text().replace('../../', '')
    (destination / 'SKILL.md').write_text(skill)
    for path in destination.rglob('*.md'):
        path.write_text(path.read_text().replace('skills/goal-learning/SKILL.md', 'SKILL.md'))
    index_path = destination / 'agent-index.json'
    index = json.loads(index_path.read_text())
    index['skill'] = 'SKILL.md'
    index_path.write_text(json.dumps(index, indent=2) + '\n')
    return destination


def audit(data):
    errors = validate(data)
    if errors:
        return errors
    if not data['inventory_reviewed']:
        errors.append('Source/task inventory has not been manually reconciled.')
    included = [t for t in data['topics'] if t['scope'] == 'included']
    if not included:
        errors.append('No included capabilities: cannot report coverage complete.')
    for topic in data['topics']:
        if topic['scope'] == 'unknown':
            errors.append(f"{topic['id']}: scope unresolved.")
        elif topic['scope'] == 'included' and topic['coverage'] not in ('worked_example', 'practiced'):
            errors.append(f"{topic['id']}: coverage is {topic['coverage']}.")
    return errors


def report(data):
    print(data['title'])
    print('Goal:', data['goal'])
    print('Inventory manually reconciled:', data['inventory_reviewed'])
    included = [t for t in data['topics'] if t['scope'] == 'included']
    print('Included-topic coverage:', dict(Counter(t['coverage'] for t in included)))
    print('Included-topic evidence:', dict(Counter(t['evidence'] for t in included)))
    for topic in data['topics']:
        print(f"- {topic['id']}: scope={topic['scope']}, coverage={topic['coverage']}, evidence={topic['evidence']}")
        if topic['scope'] == 'excluded':
            print('  Exclusion:', topic['exclusion_reason'])
    print('No mastery or goal-completion claim is inferred from this ledger.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Create an ignored local goal workspace')
    init.add_argument('slug')
    init.add_argument('--title', required=True)
    init.add_argument('--goal', required=True)
    for name in ('status', 'audit', 'plan'):
        sub.add_parser(name).add_argument('ledger', type=Path)
    sub.add_parser('bundle', help='Export a self-contained skill without personal data').add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'bundle':
            print(f'Exported portable skill to {bundle(args.destination)}')
            return 0
        if args.command == 'init':
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
                parser.error('slug must contain lowercase words/digits separated by hyphens')
            if not args.title.strip() or not args.goal.strip():
                parser.error('title and goal cannot be blank')
            root = Path(__file__).resolve().parent
            target = root / 'courses' / args.slug
            target.mkdir(parents=True, exist_ok=False)
            (target / 'materials').mkdir()
            (target / 'sessions').mkdir()
            data = {'title': args.title, 'goal': args.goal, 'success_criteria': [],
                    'inventory_reviewed': False, 'sources': [], 'topics': [], 'observations': []}
            (target / 'course.json').write_text(json.dumps(data, indent=2) + '\n')
            print(f'Created {target}. Define criteria and inventory before teaching.')
            return 0
        data = json.loads(args.ledger.read_text())
        if args.command == 'plan':
            print(json.dumps(plan(data), indent=2))
            return 0
        problems = validate(data) if args.command == 'status' else audit(data)
        if problems:
            print('\n'.join(f'- {issue}' for issue in problems))
            return 1
        report(data)
        if args.command == 'audit':
            print('PASS: declared coverage checks. Source completeness and ability still require review.')
        return 0
    except (OSError, ValueError) as exc:
        print(f'Goal Learning: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

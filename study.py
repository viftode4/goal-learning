#!/usr/bin/env python3
"""Local goal ledger: initialize, report, and audit declared coverage."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

COVERAGE = {'not_started', 'introduced', 'worked_example', 'practiced'}
EVIDENCE = {'unknown', 'guided', 'independent', 'transferable', 'durable'}


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
    return errors


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
    for name in ('status', 'audit'):
        sub.add_parser(name).add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
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
                    'inventory_reviewed': False, 'sources': [], 'topics': []}
            (target / 'course.json').write_text(json.dumps(data, indent=2) + '\n')
            print(f'Created {target}. Define criteria and inventory before teaching.')
            return 0
        data = json.loads(args.ledger.read_text())
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

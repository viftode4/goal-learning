# Goal Learning

Learn toward a concrete goal with a source-grounded AI tutor, an explicit coverage map, and evidence of what you can do independently. Use it for an exam, a technical skill, a project, or understanding a field.

This repository brings together a portable tutoring skill, a small local tool, source provenance, research references, and lessons from an actual preparation session. It is a new workflow, not a validated claim to teach anything or guarantee a result.

## Start with a goal

Python 3.10+, no dependencies or API keys:

```sh
python3 study.py init build-a-parser --title "Build a parser" --goal "Independently implement and explain a small expression parser"
python3 study.py status courses/build-a-parser/course.json
python3 study.py audit courses/build-a-parser/course.json
```

The initial audit intentionally fails. Edit the ledger: define observable success criteria, inventory sources and required capabilities, and record evidence as you learn. See [the synthetic example](examples/course.json) and [the workflow](docs/WORKFLOW.md). `courses/` is a local workspace name for any learning goal, not just academic courses.

## Use with an assistant

Open this repository and say:

> Use skills/goal-learning/SKILL.md. My goal is [outcome], my starting point is [experience], and I have [constraints]. Inspect the resources, build a complete capability map, and teach one small part at a time. Keep scope, coverage and demonstrated ability separate.

[AGENTS.md](AGENTS.md) applies to Codex; [CLAUDE.md](CLAUDE.md) points Claude to the same instructions. Any assistant can follow the files directly. This repository does not change global agent configuration or install itself automatically.

The [portable skill](skills/goal-learning/SKILL.md) uses the bundled documents. To install it in another skills directory, copy the **whole repository** to a stable location and symlink that directory's `goal-learning` entry to this repository's `skills/goal-learning`. Copying SKILL.md alone breaks its relative references. Keep the existing `learn-anything` skill separate; this one does not overwrite it.

## What is bundled

- [Workflow](docs/WORKFLOW.md): goals, sources, prerequisites, teaching, evidence and resuming.
- [Provenance](docs/PROVENANCE.md): upstream projects, exact versions and what actually ran.
- [Methods and sources](docs/METHODS.md): research basis, methods used, limits and untested proposals.
- [Exam guide](docs/EXAM-WORKFLOW.md) and [RecSys retrospective](docs/RECSYS-RETROSPECTIVE.md).
- [Improvement plan](docs/IMPROVEMENTS.md) and [behavioral evaluation cases](evals/tutor-cases.json).
- [Session](templates/SESSION.md), [assessment](templates/ASSESSMENT.json) and [debrief](templates/DEBRIEF.md) templates.
- A standard-library CLI for initialization, status and coverage checks. It does not grade answers or run spaced repetition.

## What an audit means

```sh
python3 study.py audit courses/build-a-parser/course.json
python3 -m unittest discover -s tests -v
```

An audit fails for missing goal criteria, an unchecked source inventory, unknown scope, missing references, shallow included topics, or unsupported evidence metadata. It checks the declared ledger. It cannot discover omitted concepts, verify grading, or certify mastery. A human/tutor must reconcile sources and real task requirements against the map first.

Coverage reports and evidence reports stay separate. A worked example counts as delivered coverage, not independent performance. A passing coverage audit is not a completion or grade prediction. Test the actual goal independently before reporting success.

## Keep personal work private

The public repository contains reusable instructions, tooling and synthetic examples. Course files, PDFs, answers, personal responses and transcripts belong in ignored `courses/` or `private/`, with a separate private backup if needed. See [maintenance](docs/MAINTAINING.md). Existing RecSys materials and detailed state remain in their original private workspace.

# Agent reference: commands and state

Use this as a lookup, not a script to recite to the learner. [AGENTS.md](../AGENTS.md) contains the operating invariants; [the file index](../agent-index.json) routes by task. The workflow and allocation policy remain authoritative for teaching decisions.

## Command contract

Run commands from the repository or exported skill root; resolve the private ledger path explicitly. `python3 study.py --help` lists commands. Python 3.10+, standard library only.

| Command | Output and effect |
| --- | --- |
| `init SLUG --title TITLE --goal GOAL` | Creates `courses/SLUG/course.json`, `materials/`, `sessions/`; refuses an existing folder. SLUG uses lowercase words/digits separated by hyphens. The initial ledger is intentionally incomplete. |
| `status LEDGER` | Validates metadata, prints separate coverage/evidence summaries. Does not write state. |
| `audit LEDGER` | Validates metadata and checks declared coverage, scope and inventory review. Does not verify source completeness or learner ability. Does not write state. |
| `plan LEDGER` | Validates metadata and returns JSON describing one proposed action and its reasons. Does not change evidence, coverage or records. |
| `bundle DESTINATION` | Writes reusable files and a portable SKILL.md to a new folder outside the source root. Excludes courses/, private/ and Git metadata. |

Success returns exit code 0. Invalid data, failed coverage checks and file-operation errors return 1; argument errors return 2. Error messages are text, not JSON. Only successful `plan` output is JSON; other successful commands print text.

## Planner actions

| `action` | Agent response |
| --- | --- |
| `reconcile_inventory` | Inspect source/task outlines and reconcile the topic map before marking inventory reviewed. |
| `resolve_scope` | Resolve the listed unknown topics from sources or learner constraints; do not silently exclude them. |
| `study` | Inspect `recommended`, `candidates`, `blocked` and `coverage_gaps`. Check pending assessments and actual records before following or overriding the recommendation. |
| `review_goal_scope` | No eligible candidates were found. Inspect scope, exclusions and prerequisites; this is not a completion verdict. |

`recommended.purpose` is coverage, explore, practice or refresh. Scores expose importance, need and intervening-observation terms. Read [the allocation policy](TOPIC-ALLOCATION.md) for the algorithm and limits. A failed plan does not create a learner failure.

## Ledger fields

All paths below are private learning records unless explicitly synthetic. JSON field names are stable for this version; extra fields are allowed. Examples: [minimal ledger](../examples/course.json), [allocation fixture](../examples/allocation.json).

| Root field | Required value |
| --- | --- |
| `title`, `goal` | Nonempty strings; the goal names an observable outcome. |
| `success_criteria` | Nonempty list of nonempty strings describing assessable behavior. |
| `inventory_reviewed` | Boolean; set true only after actual manual source/task reconciliation. |
| `sources` | Nonempty list of objects with unique nonempty `id` and nonempty `location`. IDs cannot contain `:`. |
| `topics` | Nonempty list of topic objects, below. |
| `observations` | Optional chronological list of activity records; default is an empty list. |

| Topic field | Value |
| --- | --- |
| `id`, `title` | Unique nonempty topic ID and nonempty title. |
| `scope` | included / excluded / unknown. Excluded topics need `exclusion_reason` and source references. Unknown scope blocks allocation and coverage completion. |
| `source_refs` | Nonempty list like `lecture-1: pages 6–12`; source ID must exist and section/page text cannot be empty. |
| `coverage` | not_started / introduced / worked_example / practiced. Only actual delivered material counts. |
| `evidence` | unknown / guided / independent / transferable / durable. |
| `evidence_ref` | Nonempty record reference whenever evidence is not unknown. The tool does not read or verify that record. |
| `importance` | Optional low / normal / high; default normal. Derive from the real goal. |
| `prerequisites` | Optional list of included topic IDs; missing references and cycles fail validation. |
| `practice_questions` | Optional list of nonempty string references; default empty. Does not define scope. |

| Observation field | Value |
| --- | --- |
| `id` | Unique nonempty activity ID. |
| `topic_id` | Existing topic ID. |
| `purpose` | coverage / explore / practice / refresh. |
| `result` | correct / partially_correct / incorrect / ungradable / not_assessed. Coverage demonstrations must use not_assessed. |
| `hint_level` | Integer 0–5, where 0 means no hints. Record actual assistance. |
| `record_ref` | Nonempty reference to the actual teaching record or learner response and frozen assessment. |

Metadata validation does not establish that a response occurred, a referenced file exists, a source was read, or a mastery judgment is justified. The agent checks those facts separately.

## Private record conventions

Use `course.json` for the ledger and a latest `handoff.json` based on [the template](../templates/HANDOFF.json). Keep session and assessment records under `sessions/` with unique IDs. These filenames are conventions; the CLI does not discover or write a handoff automatically.

Resolve references stored in a handoff or ledger relative to that file's directory, unless they are absolute paths. Follow the latest handoff's explicit references; if it is missing, inspect actual session records rather than assuming that filename order proves recency. Never invent a pending question, review event or response.

Before asking a question: save its source basis, rubric and hint ladder using [the assessment template](../templates/ASSESSMENT.json). After the response: preserve exact wording, record hints and grade against that frozen rubric. Save tutor interpretation separately. A withdrawn question keeps its correction history and contributes no negative mastery evidence.

## Repository checks

```sh
python3 -m unittest discover -s tests -v
```

Tests cover ledger/planner behavior, export independence, documentation links and the machine-readable index. They do not establish teaching effectiveness or compatibility with every agent product. Keep actual tutor evaluations separate from these checks.

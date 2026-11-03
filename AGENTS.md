# Agent entrypoint

This repository is a goal-oriented tutoring protocol with optional Python helpers. Start here; the README is the human-facing concept overview. [agent-index.json](agent-index.json) provides the same task routing as structured data.

## Start or resume

1. Read [the skill](skills/goal-learning/SKILL.md), the learner's ledger, latest handoff, and referenced session/assessment records. Reuse known goals and constraints. One tutor writes a goal at a time.
2. Resume a pending unanswered assessment before selecting unrelated work. Otherwise inspect scope, prerequisites, coverage gaps and actual evidence, then choose one useful activity.
3. Read only the references needed for the current task. Source details and future lesson content are loaded or prepared when needed.

| Task | Read |
| --- | --- |
| Set up a new goal | [Quickstart](docs/QUICKSTART.md), [workflow](docs/WORKFLOW.md) |
| Select a topic or balance activities | [Allocation policy](docs/TOPIC-ALLOCATION.md) |
| Operate the CLI or edit a ledger | [Commands and state](docs/AGENT-REFERENCE.md) |
| Prepare for an exam | [Exam guide](docs/EXAM-WORKFLOW.md) |
| Switch agents or export a skill | [Portability](docs/AGENT-PORTABILITY.md), [handoff template](templates/HANDOFF.json) |
| Check a research claim or attribution | [Methods](docs/METHODS.md), [provenance](docs/PROVENANCE.md) |
| Change the system | [Maintenance](docs/MAINTAINING.md), [behavioral cases](evals/tutor-cases.json) |

## Keep these invariants

- **Scope:** map the full goal and authoritative source outlines before choosing depth. Sample questions do not define coverage. State omissions and real time tradeoffs; never silently narrow the learner's request.
- **Selection:** separate required teaching, uncertain ability, demonstrated weakness and refresh. Respect prerequisites. Record why an activity was chosen or a planner recommendation overridden; no fixed exploration quota.
- **Teaching:** introduce unfamiliar terms and work a complete beginner example before a graded check. A generated lesson is not delivered teaching. Prepare only the current part. A progress question is not permission to accelerate.
- **Assessment:** freeze source basis, rubric and hints before asking; reread that rubric before grading. Preserve exact responses separately from interpretation. Clarify ambiguity and distinguish marking slips from conceptual errors. Withdraw unfair questions and affected grades. Visually inspect answer markings or diagrams when extraction omits them.
- **Evidence:** record actual help. Guided success is not independent; transfer and delayed recall need their own observations. Never fabricate responses, ratings or review events. Planning and audit passes never promote mastery.
- **Completion:** reconcile sources manually and run `python3 study.py audit <ledger>` when available before calling coverage complete or entering final review. Then inspect actual independent goal evidence. Never promise a grade; verify actual exam logistics separately from practice-paper rules.
- **Continuity:** save the exact position, pending question, uncertainties and next action. Pausing or restarting does not advance mastery. After an exam or project, preserve uncertain recollections as uncertain and improve the process from confirmed failures.

## Tools and repository boundaries

Python is optional. If files or execution are unavailable, follow the manual/chat fallback in the portability guide and state what could not be verified. Do not require another skill, model, plugin or account.

Keep PDFs, answer keys, personal responses, transcripts and account data in ignored `courses/` or `private/`. Public changes contain reusable material and synthetic examples. Run the regression suite after code or export changes. Preserve upstream attribution and licenses. Publishing requires the user's authorization; local learning does not imply publication permission.

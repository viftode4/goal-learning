# Balancing coverage, exploration and practice

This is a transparent scheduling heuristic motivated by the RecSys preparation failure. It is not a bandit algorithm, a measured estimate of learning gain, or a scientifically established optimal time split. No new empirical claim is made by borrowing the exploration/exploitation vocabulary.

## Four activities with different purposes

| Activity | Trigger | Next action |
| --- | --- | --- |
| Coverage | Required topic has not been taught with a complete example | Explain it and demonstrate it before a graded beginner check |
| Explore | Material was taught but independent ability is unknown, only guided, or insufficiently supported | Ask a small fresh question with a frozen rubric; use the response to decide depth |
| Practice (exploit) | Latest valid graded response is wrong or partially correct | Repair the specific gap and practice a variation with fading help |
| Refresh | Independent evidence exists and the latest valid check succeeded without hints | Occasionally sample with a fresh question; do not assume it has been forgotten |

Unknown is not wrong. A guided success is not independent. An independent label without a usable observation in this ledger prompts verification rather than trust. Check its referenced record before deciding the task. Learner confidence may prompt a check but is not a scheduling reward or a mastery label.

Coverage is a continuing obligation across the whole map; it is not a phase that can be replaced by practicing familiar sample questions. Plan and audit report all coverage gaps even when the next activity is targeted practice. Unclear scope is resolved before topic scoring. Inventory reconciliation stays manual.

## Read-only planning helper

```sh
python3 study.py plan examples/allocation.json
python3 study.py plan courses/my-goal/course.json
```

`plan` returns JSON with a recommendation, candidate reasons and score terms, prerequisites that block advancement, and remaining coverage gaps. It never changes the ledger, creates answers, promotes mastery or declares a goal complete. Recommendations require tutor judgment and may be overridden with a recorded reason: urgent goal importance, learner fatigue, changed constraints, a pending question, or an inaccurate ledger. Respect a pending unanswered assessment before picking a new topic.

Default score for each eligible topic:

`importance + need + intervening observations`

- Importance: low=1, normal=2, high=3, assigned from the actual goal, not from practice-paper frequency.
- Need: coverage=3, practice=3, explore=2, refresh=0. These are adjustable design defaults, not empirical effect sizes.
- Intervening observations: the number of recorded activities since the last valid graded check of that topic. For coverage activities, use the last recorded activity for that topic. An unchecked topic ages from the beginning of the recorded sequence.

The higher-scoring candidate is recommended; ties use topic ID for reproducibility. Aging prevents perpetual concentration on the same familiar topic among continuously eligible candidates with comparable recorded activity. This is an activity-count mechanism, not calendar-based spaced repetition. It has no guarantee of optimal learning or completion within a deadline.

Early on, most topics need coverage. Later, responses reveal weaknesses, independent uncertainty, and candidates for refresh. The balance changes from the evidence and recency without a hardcoded 80/20 quota. Near a deadline, update importance and explain tradeoffs against the real goal. The helper does not infer time pressure, exam probabilities, fatigue or task duration.

## Prerequisites and evidence

Optional `prerequisites` lists included topic IDs. The planner blocks a dependent topic until those prerequisite labels are independent, transferable or durable, and re-blocks when the latest graded response shows a failure or needed hints. Inspect the cited record; labels are not independently verified by the tool. Missing and cyclic prerequisites fail validation.

Optional `observations` is a chronological list. Each record contains `id`, `topic_id`, `purpose` (coverage/explore/practice/refresh), `result` (correct/partially_correct/incorrect/ungradable/not_assessed), `hint_level` (0–5) and `record_ref`. Store exact responses, sources and frozen rubrics privately at that reference. Coverage demonstrations use `not_assessed`. Withdrawn questions and demonstrations do not erase the last valid failure or create ability evidence. Any actual new valid assessment remains distinct from a demonstration.

The agent records only real activities and updates coverage/evidence separately with justification. Never synthesize events to improve allocation. A missing history does not mean forgetting; older ledgers remain readable but uncertain claims need checking. The CLI validates metadata, not the historical truth of the observations.

## Without Python

Follow the same decisions manually: resolve scope, inspect prerequisites, list coverage gaps, distinguish uncertainty from demonstrated weakness, and select one useful next activity. Revisit neglected topics and sometimes test apparently strong ones. Record the purpose, evidence and reason in the handoff. No formula or vendor tool is required to follow this policy.

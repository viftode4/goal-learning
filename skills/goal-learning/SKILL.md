---
name: goal-learning
description: Learn toward a concrete outcome with a complete capability map, source-grounded teaching, frozen assessments, and separate coverage and ability evidence. Use for sustained learning, projects, exam preparation, or resuming a learning goal, not simple factual questions.
---

# Goal Learning

Read [the workflow](../../docs/WORKFLOW.md), [the methods and limits](../../docs/METHODS.md), and the learner's current local ledger and latest session notes. Repository instructions are in [AGENTS.md](../../AGENTS.md).

1. Establish the desired observable outcome, starting evidence, constraints and success criteria. Reuse context before asking questions.
2. Inventory all relevant source outlines or task requirements. Build a provisional capability and prerequisite map. Sample questions or benchmarks do not define the entire goal. Mark uncertainty and exclusions openly.
3. Run the bundled CLI audit. Resolve incomplete inventory and missing scope before claiming complete coverage. Prioritize transparently when time is limited.
4. Choose the next activity using [the allocation policy](../../docs/TOPIC-ALLOCATION.md): required coverage, exploration of uncertain ability, practice of demonstrated weaknesses, or occasional refresh. Respect pending questions and prerequisites. Use `python3 study.py plan <ledger>` if available; otherwise apply the policy manually. Record the reason, without changing evidence merely because a topic was selected.
5. Prepare only the current section. Define terms and work a complete example before assessing a beginner. Use a short explanation and manageable check, adapting pace from actual responses.
6. Use [the assessment template](../../templates/ASSESSMENT.json). Freeze its source basis and rubric before showing the question. Record delivery and actual responses afterward. Read that rubric again before grading; never change it to fit an answer.
7. Give precise feedback, preserve correct subskills, and withdraw flawed questions. Keep learner wording separate from interpretation and hints separate from independence.
8. Update coverage and evidence independently. Do not infer learning from generated material, a due review, a marking slip, familiar answer choices, or a statement that the learner understands.
9. Before final review, reconcile the full map against source headings and required capabilities. Run audit again. Test success criteria with fresh independent tasks; test transfer and delayed recall separately.
10. Save [a concrete resume record](../../templates/SESSION.md). After an exam or project, use [the debrief](../../templates/DEBRIEF.md) and update the process from confirmed failures.

For exams, also read [the exam guide](../../docs/EXAM-WORKFLOW.md). For provenance and research, see [PROVENANCE.md](../../docs/PROVENANCE.md) and [METHODS.md](../../docs/METHODS.md). The sources support individual methods, not this whole AI tutoring system. Evaluate proposed changes using [the behavioral cases](../../evals/tutor-cases.json).

Keep all personal records local under courses/ or private/. No automatic publication, source copying, account actions or global installation. The repository requires no particular AI provider, skill package or scheduler. If sources are unavailable, say so and distinguish research from supplied material.

For cross-agent use or a self-contained export, read [the portability guide](../../docs/AGENT-PORTABILITY.md). Python is optional; file-only agents can follow the same decisions manually and record a [handoff](../../templates/HANDOFF.json).

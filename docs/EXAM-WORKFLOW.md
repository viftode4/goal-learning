# From materials to exam preparation

## 1. Establish scope

Record the course, exam date, available study time, starting knowledge and desired outcome. Treat grades as goals, not promises. Ask for missing information only when it changes the route; inspect available files first.

List the syllabus, every lecture outline, tutorials, assignments, practice papers and authoritative announcements. Record an ID and location for each source. Reconcile lecture headings against the topic list, including subtopics and conceptual contrasts. Only then set `inventory_reviewed` to true. An empty or incomplete topic list must not be represented as complete coverage.

The ledger uses `scope: included`, `excluded`, or `unknown`. Exclusion requires a reason and source reference, such as an official scope announcement. Unknown scope blocks the audit. Weak practice-paper representation is not an exclusion reason.

## 2. Plan openly

Order topics by prerequisites, importance and observed weakness. Estimate time without claiming precision. If the time budget cannot cover everything, show what would remain shallow or untouched. Do not silently redefine the goal to match the time available. Ask for the user's choice when an actual scope reduction is necessary.

Mark `practice_questions` separately. It is a cross-reference, never evidence that the syllabus is complete. A practice paper with only multiple-choice questions can still require understanding formulas and distinctions across all in-scope materials.

## 3. Teach and gather evidence

For the current topic: explain the connection, define terms, work one complete example, then ask a short check. Do not test merely mentioned concepts. Save an assessment's rubric before showing the question. Teach one part at a time and adjust from the response.

Coverage values are `not_started`, `introduced`, `worked_example`, or `practiced`. In this ledger, `worked_example` and `practiced` meet the declared coverage threshold; neither automatically proves understanding. Set them only for material actually delivered, not lesson files generated in advance.

Evidence values are `unknown`, `guided`, `independent`, `transferable`, or `durable`. Record task, source, date, exact response, hint level and result in private session/assessment notes. Reference that record in `evidence_ref`. A coached correct answer stays guided. A new context and later recall require separate checks. This lightweight audit checks evidence references exist as fields, not whether a human grading decision is valid.

## 4. Reconcile before final review

Recheck all source headings against the ledger. Run the audit, inspect unstarted and introduced topics, and compare actual teaching against intended coverage. Explicit exclusions should remain visible even on a passing report. Use fresh questions for weak concepts, including differences between related methods and assumptions hidden by familiar answer choices.

Report two things: what material was covered and what the learner demonstrated. Practice scores are practice scores. Do not convert them into grade predictions. If the session ends with gaps, record them plainly rather than claiming completion.

## 5. Resume and learn after the exam

Use the session template to store exact position, evidence and next action. Do not restart the course from old memory or treat a stopped lesson as completed. Review with retrieval before showing answers; only use difficulty ratings supplied by the learner.

After the exam, use the debrief template. Keep uncertain wording uncertain and grades unverified until results arrive. For a gap, ask: was the source omitted, the explanation too shallow, the assessment too narrow, or the feedback misleading? Update the workflow and regression cases accordingly.

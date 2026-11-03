# Goal-oriented learning instructions

Read README.md, skills/goal-learning/SKILL.md, docs/WORKFLOW.md, the current course ledger, and its latest private session notes before teaching. Use one tutor at a time. Do not require any vendor-specific skill to use this repository.

## Coverage before teaching

- Define the goal and observable success criteria. Inventory task requirements and authoritative sources; for exams include the full syllabus, every lecture/topic outline, tutorials, assignments and stated exam scope. Inspect outlines first; read detailed source pages as each topic is taught.
- Map practice questions onto that inventory. A topic absent from a practice paper remains in scope unless authoritative evidence excludes it.
- Keep source inventory, material coverage, teaching delivered in chat, and learner evidence distinct.
- Never silently narrow the user's requested scope. A time budget permits prioritization, not an undisclosed scope change. State omissions and implications and let the user choose a real tradeoff.
- Check related methods, contrasts, assumptions and formula roles. For example, knowing matrix factorization does not establish understanding of decomposition versus optimization.

## Teaching and assessment

- Assume only the learner's demonstrated prerequisites. Define terms, connect to the previous idea, work a complete example, then ask one manageable check.
- A saved lesson is not delivered teaching. Never test an unintroduced concept as if it were taught. Withdraw unfair questions and their negative evidence.
- Freeze a question, rubric and source basis before displaying it; preserve original versions. Grade actual responses, not inferred understanding. Visually inspect diagram-based answer keys when text extraction loses markings.
- Preserve exact user answers separately from tutor interpretations. Ask about ambiguity rather than manufacturing a misconception. Retain marking slips separately from conceptual errors and original scores.
- Track hints. Correct after coaching is guided evidence; an independent fresh answer is different. Transfer and delayed recall require their own observed responses.
- If the user asks how much remains, report coverage and outstanding gaps. Do not speed up unless requested. Adapt the step size when confused.
- Generate only the current teaching section and assessment; future topics remain a provisional route.

## Reporting and continuity

- Run `python3 study.py audit <ledger>` before calling coverage complete or entering final review. A pass covers only declared topics; manually cross-check source completeness first.
- Never promise a grade. Recognition on familiar practice questions is not a timed unseen exam or durable mastery.
- Separate practice-paper instructions from independently verified actual-exam rules. Record source and verification date for logistics.
- End with a concrete resume position, current uncertainties and next action. Save progress without advancing mastery when the learner pauses or asks for a restart.
- After the exam, preserve the learner's report without inventing the exact question or result. Improve the process, not merely the summary.

## Repository work

Keep source PDFs, exam papers, answers, personal study records, account data and transcripts out of public commits. `courses/` and `private/` are ignored. Do not import another tool's implementation without checking its license. Use standard-library Python and run the regression suite after code changes. Public publishing requires the user's authorization; creating a local course does not authorize publishing it.

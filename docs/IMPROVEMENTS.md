# Improvement plan

## Implemented in this version

- Separate goal criteria, source inventory, scope, delivered coverage and ability evidence.
- Audit unknown scope, shallow topics and undocumented exclusions even when every sample question is passed.
- Keep personal course data local and synthetic examples public.
- Bundle the teaching protocol, source audit, research links, retrospective and behavioral evaluation cases.
- Regression-test the deterministic ledger rules. Passing tests only supports those rules, not tutor quality.

## Next, before making the system larger

1. Run the behavioral cases against an actual tutor and save prompts/responses and a predeclared rubric privately. They are currently evaluation specifications, not passed tests.
2. Trial one small non-exam goal. Compare the capability map to an external reference or independent reviewer; record missing prerequisites and source omissions.
3. Test actual goal criteria with fresh independent tasks, followed by a delayed check. Record failures instead of changing criteria to fit the result.
4. Add a manual subtopic/contrast review: definitions, assumptions, mechanisms, comparisons, numerical tasks, edge cases and application. Record an explicit “not applicable” where appropriate.
5. If review scheduling is useful, integrate an established scheduler with user-provided recall ratings and separately recorded mastery evidence. Do not build a second scheduler just for this repository.

## Only after observed need

Machine-readable evidence records could validate hint levels, dates, rubric versions and delayed intervals. Source adapters could flag untouched outline sections. A small dashboard could make gaps easier to inspect. None is implemented here; an interface would not solve an incomplete map or bad grading by itself.

Success measures: fewer unrecorded scope omissions, fewer unfair questions, accurate distinction between guided and independent work, clean session resumption, and successful independent goal tasks and later recall. Satisfaction is useful feedback, not a substitute for these observations.

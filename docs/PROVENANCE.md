# Provenance and attribution

Audit date: 2026-11-03. This separates historical local configuration from sources checked while creating Goal Learning. Commit existence was verified through GitHub's API. Local files establish what was installed; current upstream default branches are not substituted for those versions.

## Direct upstream influences

| Component | Historical version | Role in the RecSys workspace | Role here |
| --- | --- | --- | --- |
| [Learn Anything by Nar](https://github.com/Nar101/learn-anything/tree/632817b900ea271bae9440096176a61c2e9d371b) | `632817b900ea271bae9440096176a61c2e9d371b` | Teaching protocol, templates, assessment integrity, separate evidence levels and course validator | Credited design adaptation; upstream implementation is not vendored |
| [study-skill by mordor-forge](https://github.com/mordor-forge/study-skill/tree/4a2ae45945a419dc84fbae58d0312962d5896de8) | `4a2ae45945a419dc84fbae58d0312962d5896de8` | Only its Go FSRS-based scheduler was active, through a local adapter | Operational inspiration and optional integration reference; no scheduler bundled |
| [Free Spaced Repetition Scheduler](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler) | No independent upstream algorithm pin established in this audit | The scheduler package identifies FSRS as its algorithmic basis | Linked primary algorithm source; no claim that the local implementation equals Anki or an official reference implementation |

Local setup documentation described English-heading adaptations to Nar's validator and short English teaching in chat while retaining its source checks and frozen assessments. Local tooling combined Python/PyYAML, PDF text extraction, ripgrep, the course state files and the scheduler. These are integration details, not new learning-science methods.

The installed Nar package identifies Nar / 那不然 as creator and MIT as its license. The adapted protocol is credited here and its notice/license are retained in `THIRD_PARTY_NOTICES/`. The study-skill README identifies MIT, but its implementation has not been copied here. Goal Learning's authored code is a new, smaller ledger checker, not a fork or replacement for either complete runtime.

## Historical course sources

The private RecSys workspace used course slide PDFs covering foundations, content-based recommendation, collaborative filtering, factorization, evaluation, ranking objectives, deep and graph models, hybrids, beyond-accuracy objectives, online recommendation and generative recommendation. It also used the supplied practice paper and a visually inspected answer key.

Those files provided domain content, not proof that the tutoring method worked. Their identities and page-level claims remain in the private course source manifest. Original PDFs, answer keys, extracted text, personal responses and transcripts are deliberately not redistributed here. The new synthetic example is authored for this repository and is not a copied exam question.

## Other inspiration and its limits

Nar's learning-science reference lists retrieval practice, spacing, cognitive load, worked examples, self-explanation, feedback, interleaving, mastery learning, deliberate practice, transfer and metacognition. It also names *Make It Stick* and *Peak* as accessible syntheses. We did not independently read or verify those books during this audit; they are indirect upstream influences, not books this project claims to have implemented or validated.

Research references in METHODS.md were checked during this packaging task. They support particular methods and their limits; they are not evidence that the entire protocol was research-validated before the original tutoring session. GitHub project pages establish provenance, not pedagogical effectiveness.

## Original changes from this session

The learner's feedback prompted a full-scope coverage reconciliation before final review, visible scope tradeoffs under time limits, explicit checks of method contrasts, and separation of practice recognition from actual goal performance. The retrospective records the failure; regression tests cover the ledger rules that can be automated. These are local design improvements with future effectiveness still untested.

## Allocation and portability follow-up

The learner explicitly proposed balancing exploration and exploitation of topics. The resulting coverage/explore/practice/refresh policy, transparent planner and private-data-free portable export are local additions. The score weights have no claimed empirical validation. No new upstream scheduler or agent dependency was added.

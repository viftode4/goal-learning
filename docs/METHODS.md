# Methods, evidence and limits

Sources checked on 2026-11-03. Research metadata/abstracts or author-hosted records were inspected; this is a focused provenance review, not an exhaustive literature review. No effect size or universal success claim is inferred. Supporting research concerns particular tasks and populations, not this whole AI tutor.

## What happened in the original preparation

| Method | Actual use | Limit or failure | Goal Learning response |
| --- | --- | --- | --- |
| Worked examples and small steps | Definitions, complete examples and short coached checks | Some concepts were initially tested after inadequate teaching | Require delivered prerequisites and a complete beginner example |
| Retrieval practice | Frequent responses before feedback, later fresh rechecks | Familiar options and coaching reduced independence of some evidence | Record help and use new tasks; do not equate recognition with recall |
| Self-explanation | Asked for reasons, assumptions and differences | Sometimes correct numbers had weak or unsupported explanations | Preserve correct subskills and target the specific reasoning gap |
| Mixed practice | Small batches across topics, including all 24 practice questions | Coverage and depth leaned too heavily on the practice paper | Reconcile the whole capability map before final review |
| Corrective feedback | Targeted explanations, retries and withdrawal of unfair questions | Grading and interpretation sometimes required repair | Freeze rubrics, retain exact words and record withdrawals |
| Source grounding | Local course PDFs, page-level references, visual answer-key checks | Source-backed content did not ensure all source topics were taught deeply | Separate source inventory from delivered coverage |
| Evidence and resume state | Guided/independent labels and concrete next steps | Administrative validity did not establish learning quality | Report ledger checks as structural checks only |
| Spaced repetition | Scheduler configured; 33 cards in the audited store | Zero recorded review events; not demonstrated as completed spaced review | Optional future integration, never fabricate review ratings |
| Transfer and durable retention | Some fresh contexts were checked | No comprehensive delayed or goal-level transfer result | Require separate observed tasks before those claims |

## Research basis checked for this bundle

| Reference | Why it matters | Boundary and application |
| --- | --- | --- |
| [Roediger & Karpicke (2006), Test-enhanced learning](https://pubmed.ncbi.nlm.nih.gov/16507066/), DOI `10.1111/j.1467-9280.2006.01693.x` | Experiments found delayed retention benefits of retrieval relative to repeated study for prose passages | Ask for recall before showing answers; do not assume a same-session answer proves long-term retention |
| [Cepeda et al. (2006), Distributed practice in verbal recall tasks](https://pubmed.ncbi.nlm.nih.gov/16719566/), DOI `10.1037/0033-2909.132.3.354` | Quantitative synthesis connects spacing and the intended retention interval | Schedule later checks according to the retention goal; a fixed interval sequence is not a universal prescription |
| [Sweller & Cooper (1985), The Use of Worked Examples as a Substitute for Problem Solving in Learning Algebra](https://doi.org/10.1207/s1532690xci0201_3), [author publication record](https://research.unsw.edu.au/people/emeritus-professor-john-sweller/publications?page=3&type=journalarticles) | Foundational worked-example research in algebra | Supports beginner demonstrations as a design rationale, not an optimal lesson length or a universal rule for experts |
| [Chi et al. (1989), Self-Explanations](https://doi.org/10.1207/s15516709cog1302_1) | Examines connections between explanations during mechanics examples and later problem solving | Ask why a step works and when it applies; do not turn a specific study into a blanket causal claim about all skills |
| [Rohrer & Taylor (2007), The shuffling of mathematics problems improves learning](https://digitalcommons.usf.edu/psy_facpub/1767/), DOI `10.1007/s11251-007-9015-8` | Investigates spaced and mixed mathematical practice | Mix confusable methods after a usable foundation; applicability depends on task and knowledge level |
| [Soderstrom & Bjork (2015), Learning versus performance](https://pubmed.ncbi.nlm.nih.gov/25910388/), DOI `10.1177/1745691615569000` | Review distinguishes acquisition performance from longer-term learning | Keep immediate success, transfer and delayed evidence separate; no automatic promotion from session fluency |

## Local design decisions, not experimentally established facts

The capability ledger, source-to-topic mapping, frozen-rubric files, exact-response preservation, five evidence labels and audit-before-final-review rule are engineering and assessment safeguards. Their motivation is traceability and the observed failures. The precise schema, thresholds and labels are not standardized psychometric measurements or claims made by the cited studies.

In particular, a worked example is a minimum delivered-coverage threshold in this checker. It is not enough for goal completion. Determining whether all necessary capabilities are in the map remains a manual judgment. An assistant can still miss a subtopic, misread a source or grade badly despite a passing audit.

Mastery-learning and deliberate-practice traditions are upstream inspiration. The original session used targeted correction, but it was not a controlled mastery-learning program or an expert-supervised deliberate-practice intervention. No outcome improvement has been attributed to these labels.

## Allocation policy added after the retrospective

The exploration/exploitation discussion led to [TOPIC-ALLOCATION.md](TOPIC-ALLOCATION.md). Coverage remains obligatory; uncertain knowledge is probed, demonstrated weaknesses receive practice, and apparently strong topics are sampled periodically. The score and its activity-count aging are new engineering heuristics, not UCB, a validated learning reward, or a finding from the cited papers. Automated tests check recommendation behavior; comparative learning effectiveness remains untested.

## Proposed next evaluation

Use small learning goals with observable outputs. Preserve baseline and final independent tasks, record hints, and perform a later check. Audit topic omissions against the source outlines independently of practice questions. Evaluate the tutor against the bundled behavioral cases. Measure failures and repair cost, not just friendliness or practice scores. No controlled comparison or delayed-retention result for Goal Learning exists yet.

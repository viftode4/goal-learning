# Using Goal Learning with different agents

The protocol is Markdown plus JSON. It requires no particular model, plugin, API, scheduler, network service or global configuration. Compatibility means an agent can read and follow those files; it is not a claim that every product has been tested or automatically discovers this skill.

## Use directly from the repository

Give the agent access to this repository and the private goal folder. Ask:

> Read AGENTS.md, skills/goal-learning/SKILL.md, and docs/TOPIC-ALLOCATION.md. My goal ledger is [path]. Read its latest session/handoff and resume any pending question before selecting a new activity. Balance full coverage, uncertainty checks, targeted practice and occasional refresh. Record why you choose the next activity. Do not infer mastery from hints or familiar options.

Codex can read AGENTS.md, and CLAUDE.md points Claude to the same protocol. For other tools, supply the prompt explicitly or use that client's instruction mechanism. Automatic file discovery depends on the client.

## Export a self-contained skill

```sh
python3 study.py bundle ../goal-learning-skill
```

The destination must not already exist and must be outside the source repository. The exporter copies an explicit set of reusable directories and files, creates SKILL.md at the bundle root, and rewrites its references to work within that folder. It excludes the repository's private/, courses/, Git metadata and configuration. It does not install itself or change agent configuration.

Copy the entire exported folder into the client's configured skills directory, naming the installed directory `goal-learning`. Or place it anywhere and tell the agent to read its SKILL.md. The folder must stay intact; a lone SKILL.md does not include the workflow, templates or helper. Native skill discovery is optional.

## Match the actual capabilities

| Agent access | What works |
| --- | --- |
| Files and command execution | Full workflow, CLI audit/plan, and local record updates |
| Files only | Read the protocol and ledger, allocate topics manually, and write records if permitted; the Python helper is optional |
| Chat only | Provide SKILL.md, relevant workflow/policy text, goal ledger and latest handoff in the conversation; the agent must return updated records for you to save |

For chat-only use, external links are not a substitute for supplied content if the agent cannot open them. If the agent cannot read a source, update a file or execute a check, it must say so and request only the missing input needed; it cannot claim the operation occurred.

## A portable handoff

Use templates/HANDOFF.json for goal/ledger location, current topic, pending assessment and frozen rubric reference, coverage gaps, evidence uncertainty, last allocation and next action. Keep long exact learner responses in the referenced private records. One tutor writes a goal at a time. Another agent reads the handoff, ledger and referenced records before acting; it must not depend on a provider's hidden memory or an old chat summary.

The root directory differs between repository and exported bundle, so resolve relative paths against the file containing the reference. Personal source locations stay in private ledgers. Never copy personal materials into a skill bundle just to make a handoff easier.

## What has been verified

Automated tests export a bundle to an isolated location, resolve every local Markdown link, initialize a goal using the exported CLI, and run planning without the original repository layout. They also verify existing destinations are not overwritten and private course directories are not included. Behavioral cases specify tutor decisions, but they have not been run against every agent or model. Portability of files is tested; universal teaching quality is not.

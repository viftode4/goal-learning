# Start a learning goal

The agent can operate these tools for you. You only need to explain your goal, provide available materials, and respond to the learning activities.

## 1. Give the agent a concrete outcome

Open this repository with your agent, or provide its files, and say:

> Follow AGENTS.md. I want to [observable outcome]. I currently know [starting point]. I have [time and constraints]. Inspect the available materials, map the required topics, and start with a small explanation and worked example. Save my responses and a clear place to resume.

For an exam, include the full syllabus and available lecture material. For a project, describe what the finished work must do. A sample paper or benchmark is one source of evidence about the goal.

## 2. Create a local workspace

With Python 3.10 or newer, no dependencies:

```sh
python3 study.py init build-a-parser --title "Build a parser" --goal "Independently implement and explain a small expression parser"
```

This creates `courses/build-a-parser/` with an incomplete `course.json`, `materials/` and `sessions/`. The folder is ignored by Git. Keep a separate private backup if needed.

Edit the ledger with the agent: define observable success criteria, inventory sources, and map the topics and prerequisites. Use [the minimal synthetic example](../examples/course.json) and [the data reference](AGENT-REFERENCE.md). The initial empty ledger intentionally fails validation; it is a starting point, not a complete curriculum.

## 3. Teach, check and record

Once the required ledger fields are filled:

```sh
python3 study.py status courses/build-a-parser/course.json
python3 study.py plan courses/build-a-parser/course.json
python3 study.py audit courses/build-a-parser/course.json
```

`status` reports coverage and evidence separately. `plan` recommends a next activity and explains why. `audit` lists declared coverage gaps; it should fail while included topics remain untouched or shallow. The agent reconciles source completeness manually before marking the inventory reviewed.

During learning, use [the session template](../templates/SESSION.md), [assessment template](../templates/ASSESSMENT.json) and [handoff](../templates/HANDOFF.json). Freeze the assessment before asking it; save actual responses afterward. The tools do not grade responses or automatically update mastery.

## 4. Stop and resume

Ask the agent to save the exact position, unanswered question, remaining gaps and next action. Later, say:

> Follow AGENTS.md and resume courses/build-a-parser. Read the latest handoff and referenced records before continuing.

A different agent uses the same files. See [the portability guide](AGENT-PORTABILITY.md) for file-only and chat-only use.

## Optional: export a skill

```sh
python3 study.py bundle ../goal-learning-skill
```

The destination must be new and outside this repository. Copy the whole exported folder into the agent's configured skills directory, or ask it to read the exported SKILL.md directly. Personal learning folders are excluded. See [export details](AGENT-PORTABILITY.md).

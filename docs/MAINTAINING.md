# Maintaining Goal Learning

Reusable instructions, examples, scripts and regression tests belong in this public repository. Put personal course records in ignored `courses/` folders or a separate private repository. Keep the existing RecSys workspace intact; this project does not migrate or publish its files.

For a new goal or course, initialize a folder, inventory sources and edit the ledger. For a resumed course, read its session notes and run status/audit before teaching. For a workflow change, document the observed problem and expected behavior, update AGENTS.md or the workflow, and add a regression test if the checker changes.

Run `python3 -m unittest discover -s tests -v` before committing code. Inspect `git diff --cached` and `git ls-files` before publishing. Never force-add ignored course folders merely to back up private work. Ignoring a file does not remove it from existing Git history.

The checker is intentionally small. Add scheduling, extraction or interfaces only when an actual need justifies them. Prefer linking an established private runtime to copying a vendor dependency into this repository.

Keep README.md focused on concepts and the learning experience. Put setup instructions in QUICKSTART.md and command/data details in AGENT-REFERENCE.md. Update agent-index.json and AGENTS.md when a route changes. The exporter must carry the index and its rewritten skill path into an independent bundle. Keep public documentation references relative so they work both in GitHub and in an exported skill.

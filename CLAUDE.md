# How I work

These instructions apply in every project. A repo's own `CLAUDE.md` adds to them and wins where they conflict.

## About me

- I build solutions for clients. I'm early in my career with AI tooling, so I'm learning as I go.
- Prefer the simplest thing that solves the problem. Connecting a client's existing tools (for example with n8n) often beats building something new. Only reach for a custom build when it's clearly needed.

## Communication

- Use English for everything: chat, code comments, commit messages and docs.
- Explain as you go. When jargon appears for the first time, explain it in a few words, and say briefly why you chose an approach over the obvious alternative.
- Keep it concrete: show the command, the file or the next step rather than describing it in the abstract.
- If something is ambiguous and the choice matters, ask. If there's a sensible default, take it and say which one you picked.

## Git

- Never commit or push unless I ask. When work is ready, tell me it's ready to commit and suggest a message.
- Work on a branch, not `main`, unless I say otherwise.
- Write commit messages in the imperative mood ("Add login form"), with a short summary line.

## Before acting

Check with me first before you:
- delete files, or overwrite anything you haven't read
- install global packages or change system settings
- touch anything that holds credentials (`.env`, keys, tokens), and never commit them
- send anything to an external service, such as deploys, API calls that change data, messages or published pages

## Code

- Match the style of the existing code: naming, structure and comment density.
- After a change, run the project's tests or check it some other way, and tell me honestly what passed, what failed and what you skipped.

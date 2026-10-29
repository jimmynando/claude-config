# claude-config

My personal Claude Code setup: the global instructions, skills and agents I use in every project, on every machine.

## What's here

| Path | What it is | Ends up at |
|---|---|---|
| `CLAUDE.md` | Global instructions, i.e. how I work in any project | `~/.claude/CLAUDE.md` |
| `skills/<name>/SKILL.md` | Workflows I run with `/<name>` | `~/.claude/skills/<name>` |
| `agents/<name>.md` | Specialist subagents | `~/.claude/agents/<name>.md` |

Project-specific setup (stack, commands, conventions) does **not** go here. It lives in each repo's own `CLAUDE.md` and `.claude/`.

## Setup on a new machine

```sh
git clone <this-repo-url> ~/repos/claude-config
~/repos/claude-config/install.sh
```

`install.sh` creates symlinks, so editing a file in this repo changes what Claude uses straight away. Re-run it after a `git pull` that adds a new skill or agent.

## Day to day

- Edit skills here (or through the `~/.claude` links, since they're the same files).
- Commit and push, then `git pull` on the other machine.

## Never commit

Credentials and machine state stay out of this repo: `.credentials.json`, `settings.json` containing tokens or API keys, `history.jsonl`, `projects/` (memory), `sessions/`.

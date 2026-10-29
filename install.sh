#!/usr/bin/env bash
# Links this repo's skills, agents and global CLAUDE.md into ~/.claude.
# Safe to run again after every `git pull`: existing links are refreshed,
# and any real file in the way is moved to ~/.claude/backups first.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BACKUP_DIR="$CLAUDE_DIR/backups/claude-config-$(date +%Y%m%d-%H%M%S)"

link() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    mkdir -p "$BACKUP_DIR"
    mv "$dest" "$BACKUP_DIR/"
    echo "  backed up existing $(basename "$dest") to $BACKUP_DIR"
  fi
  ln -sfn "$src" "$dest"
  echo "  linked $dest"
}

echo "Installing from $REPO"

for skill in "$REPO"/skills/*/; do
  [ -f "$skill/SKILL.md" ] || continue
  link "${skill%/}" "$CLAUDE_DIR/skills/$(basename "$skill")"
done

for agent in "$REPO"/agents/*.md; do
  [ -f "$agent" ] || continue
  link "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
done

if [ -f "$REPO/CLAUDE.md" ]; then
  link "$REPO/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
fi

echo "Done."

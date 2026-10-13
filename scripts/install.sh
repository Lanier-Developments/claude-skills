#!/usr/bin/env bash
# Install skills from this repo into a Claude skills directory.
#
# Default: symlink each skills/<name> into ~/.claude/skills/<name>, so a
# `git pull` in this repo updates every skill on this machine at once.
#
# Usage: scripts/install.sh [--copy] [--force] [--dry-run] [--target DIR]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/skills"
TARGET="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="link"
FORCE=0
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --copy)    MODE="copy" ;;
    --force)   FORCE=1 ;;
    --dry-run) DRY=1 ;;
    --target)  shift; TARGET="${1:?--target needs a directory}" ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

run() { if [ "$DRY" -eq 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }

run mkdir -p "$TARGET"

installed=0
skipped=0
for dir in "$SRC"/*/; do
  name="$(basename "$dir")"
  case "$name" in _*) continue ;; esac   # skip _template and other private dirs
  [ -f "$dir/SKILL.md" ] || { echo "skip $name: no SKILL.md"; skipped=$((skipped+1)); continue; }

  dest="$TARGET/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ -L "$dest" ] && [ "$(readlink "$dest")" = "${dir%/}" ]; then
      echo "ok   $name (already linked)"; continue
    fi
    if [ "$FORCE" -ne 1 ]; then
      echo "skip $name: $dest exists (use --force to replace)"; skipped=$((skipped+1)); continue
    fi
    run rm -rf "$dest"
  fi

  if [ "$MODE" = "link" ]; then
    run ln -s "${dir%/}" "$dest"
  else
    run cp -R "${dir%/}" "$dest"
  fi
  echo "done $name ($MODE)"
  installed=$((installed+1))
done

echo "installed: $installed, skipped: $skipped, target: $TARGET"

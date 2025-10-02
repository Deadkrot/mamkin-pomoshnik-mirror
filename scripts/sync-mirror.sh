#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${MIRROR_REPO_URL:-}" ]]; then
  echo "Set MIRROR_REPO_URL env var (with token)"
  exit 1
fi

MIRROR_DIR=$(mktemp -d)
rsync -a --delete   --exclude '.git'   --exclude '.env'   --exclude 'data/'   --exclude 'config/config.local.yml'   ./ "$MIRROR_DIR/"

cd "$MIRROR_DIR"
git init
git remote add origin "$MIRROR_REPO_URL"
git checkout -b main
git add -A
git -c user.name="mirror-bot" -c user.email="mirror@users.noreply.github.com"   commit -m "chore(mirror): sync from private repo"
git push -f origin main

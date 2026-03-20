#!/usr/bin/env bash
# publish.sh — squash dev history and push a clean commit to zerohzz/zz-skills (public)
#
# Usage:
#   ./scripts/publish.sh                      # uses latest git tag as version
#   ./scripts/publish.sh v1.1.0               # explicit version
#   ./scripts/publish.sh v1.1.0 "feat: ..."   # explicit version + message

set -euo pipefail

VERSION="${1:-}"
MESSAGE="${2:-}"
PUBLIC_REMOTE="public"
RELEASE_BRANCH="release/publish-$$"

# ── 1. determine version ──────────────────────────────────────────────────────
if [[ -z "$VERSION" ]]; then
  VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
  if [[ -z "$VERSION" ]]; then
    echo "❌  No git tag found and no version specified."
    echo "    Usage: ./scripts/publish.sh v1.0.0"
    exit 1
  fi
fi

# ── 2. build commit message ───────────────────────────────────────────────────
if [[ -z "$MESSAGE" ]]; then
  MESSAGE="release ${VERSION}"
fi

# ── 3. confirm ────────────────────────────────────────────────────────────────
echo ""
echo "  Publishing to $(git remote get-url $PUBLIC_REMOTE)"
echo "  Version : $VERSION"
echo "  Message : $MESSAGE"
echo ""
read -r -p "  Proceed? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ── 4. create a throw-away release branch from main ──────────────────────────
git checkout -b "$RELEASE_BRANCH" main

# ── 5. squash-merge — collapses entire dev history into one staged diff ───────
git merge --squash main 2>/dev/null || true   # already on main content, just stage it
# (merge --squash onto itself is a no-op; the real squash happens via the orphan below)

# go back and use a cleaner approach: orphan branch
git checkout main
git branch -D "$RELEASE_BRANCH" 2>/dev/null || true

# ── 6. fetch the current public main (may diverge) ───────────────────────────
git fetch "$PUBLIC_REMOTE" main 2>/dev/null || true

# ── 7. create orphan commit: single clean snapshot ───────────────────────────
RELEASE_BRANCH="release/publish-$$"
git checkout --orphan "$RELEASE_BRANCH"
git add -A
git commit -m "$MESSAGE"

# ── 8. push to public ─────────────────────────────────────────────────────────
git push "$PUBLIC_REMOTE" "${RELEASE_BRANCH}:main" --force
echo ""
echo "✅  Published ${VERSION} → $(git remote get-url $PUBLIC_REMOTE)"

# ── 9. tag on dev (optional, keeps dev history annotated) ────────────────────
git checkout main
git branch -D "$RELEASE_BRANCH"
if ! git tag -l | grep -qx "$VERSION"; then
  git tag "$VERSION"
  echo "🏷   Tagged ${VERSION} on dev"
fi

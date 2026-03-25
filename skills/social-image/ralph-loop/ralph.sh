#!/usr/bin/env bash
set -euo pipefail

# Ralph Loop — Social Image Quality
# Usage: ./ralph.sh [max_iterations]

DIR="$(cd "$(dirname "$0")" && pwd)"
PROMPT="$DIR/CLAUDE.md"
MAX_ITERS="${1:-20}"
PROGRESS="$DIR/progress.txt"
SCORES="$DIR/scores.json"

# Init state files if missing
[[ -f "$PROGRESS" ]] || echo "# Ralph Loop Progress" > "$PROGRESS"
[[ -f "$SCORES" ]]   || echo '{"iterations":[]}' > "$SCORES"

echo "━━━ Ralph Loop: Social Image Quality ━━━"
echo "Max iterations: $MAX_ITERS"
echo "Prompt: $PROMPT"
echo ""

for i in $(seq 1 "$MAX_ITERS"); do
  echo "━━━ Iteration $i / $MAX_ITERS ━━━"

  OUTPUT=$(claude --print \
    --dangerously-skip-permissions \
    -p "$(cat "$PROMPT")" \
    2>&1 | tee /dev/stderr) || true

  if echo "$OUTPUT" | grep -q '<promise>COMPLETE</promise>'; then
    echo ""
    echo "✅ Ralph completed at iteration $i"
    exit 0
  fi

  echo ""
  echo "⏳ Not yet complete. Next iteration in 3s..."
  sleep 3
done

echo "⚠️  Max iterations ($MAX_ITERS) reached without completion."
exit 1

#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAX_ITERATIONS=${1:-20}
SCORES_FILE="$SCRIPT_DIR/scores.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"

# Initialize scores tracking
if [ ! -f "$SCORES_FILE" ]; then
  echo '{"iterations": [], "best_score": 0, "status": "running"}' > "$SCORES_FILE"
fi

# Initialize progress file
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Visual Quality Loop - Progress Log" > "$PROGRESS_FILE"
  echo "# Started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

echo "=== Ralph Visual Quality Loop ==="
echo "Max iterations: $MAX_ITERATIONS"
echo "Prompt: $SCRIPT_DIR/CLAUDE.md"
echo ""

for i in $(seq 1 "$MAX_ITERATIONS"); do
  echo "--- Iteration $i / $MAX_ITERATIONS --- $(date '+%H:%M:%S')"

  OUTPUT=$(claude --dangerously-skip-permissions --print < "$SCRIPT_DIR/CLAUDE.md" 2>&1) || true

  echo "$OUTPUT" | tail -5

  if echo "$OUTPUT" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "=== COMPLETE at iteration $i ==="
    jq '.status = "complete"' "$SCORES_FILE" > "$SCORES_FILE.tmp" && mv "$SCORES_FILE.tmp" "$SCORES_FILE"
    exit 0
  fi

  echo "Score not perfect yet. Continuing..."
  sleep 2
done

echo "=== Exhausted $MAX_ITERATIONS iterations without achieving perfect score ==="
exit 1

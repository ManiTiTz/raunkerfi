#!/usr/bin/env bash
# Push to GitHub, pull on the Pi and sync the venv there.
# Usage: ./build.sh                                  # update the Pi only
#        ./build.sh --run 9Lab/collision_Avoidance.py # update, then run
set -euo pipefail

PI_HOST="${PI_HOST:-fridaypi}"        # Host from ~/.ssh/config
PI_REPO="${PI_REPO:-~/raunkerfi}"     # Where the repo lives on the Pi
REPO_URL="$(git remote get-url origin)"

RUN_CMD=""
if [ "${1:-}" = "--run" ]; then
    RUN_CMD="uv run python ${2:?usage: ./build.sh --run <path/to/script.py>}"
fi

if ! git diff --quiet HEAD; then
    echo "Uncommitted changes — commit first, the Pi only gets what's pushed." >&2
    exit 1
fi

git push

# -t so Ctrl+C reaches the script on the Pi (and the motors stop)
ssh -t "$PI_HOST" "
    set -e
    [ -d $PI_REPO ] || git clone $REPO_URL $PI_REPO
    cd $PI_REPO
    git pull --ff-only
    uv sync
    $RUN_CMD
"
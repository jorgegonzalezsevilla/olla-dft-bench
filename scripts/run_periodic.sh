#!/usr/bin/env bash
# Periodic benchmark: run, verify, commit and push. Meant for the systemd timer in ./systemd.
set -euo pipefail
cd "$(dirname "$0")/.."
git pull -q --ff-only || true
.venv/bin/pip install -q --upgrade "olla-dft @ git+https://github.com/jorgegonzalezsevilla/olla-dft@main" >/dev/null
.venv/bin/pip freeze > requirements.lock
OUT=$(python3 bench.py run --reps 5 --isolate --with-qe --label periodic 2>&1 | tee /dev/stderr)
RUN=$(echo "$OUT" | grep -oE 'results/[0-9]{8}-[0-9]{6}' | head -1)
python3 bench.py verify "$RUN"
python3 bench.py judge-pack "$RUN"
git add -A results docs judge requirements.lock
git commit -qm "Periodic benchmark $(basename "$RUN")" || exit 0
git push -q origin main

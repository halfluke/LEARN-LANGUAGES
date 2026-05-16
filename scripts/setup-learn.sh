#!/usr/bin/env bash
# First-time setup for learners: hub + Python tracks, runtime dependencies only.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/bootstrap.py --learn

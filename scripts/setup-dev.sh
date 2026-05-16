#!/usr/bin/env bash
# First-time setup for contributors: hub + Python tracks with [dev] (pytest, etc.).
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/bootstrap.py --dev

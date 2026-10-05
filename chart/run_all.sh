#!/usr/bin/env bash
# Reproduce every output from BIRTH_INPUT.json. Requires .venv (see CALCULATION_MANIFEST.json) and `npm ci` in ziwei/.
# Usage: CHART_DIR=charts/<person> chart/run_all.sh   (CHART_DIR defaults to the repository root)
set -euo pipefail
if [[ -n "${CHART_DIR:-}" ]]; then export CHART_DIR="$(cd "$CHART_DIR" && pwd)"; fi
cd "$(dirname "$0")"
PY=../.venv/bin/python
$PY builder.py
$PY verify.py
$PY synthesize.py > /dev/null
$PY report.py

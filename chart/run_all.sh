#!/usr/bin/env bash
# Reproduce every output from BIRTH_INPUT.json. Requires .venv (see CALCULATION_MANIFEST.json) and `npm ci` in ziwei/.
set -euo pipefail
cd "$(dirname "$0")"
PY=../.venv/bin/python
$PY builder.py
$PY verify.py
$PY synthesize.py > /dev/null
$PY report.py

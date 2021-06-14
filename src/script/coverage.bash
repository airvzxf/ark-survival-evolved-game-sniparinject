#!/usr/bin/env bash
set -e

CURRENT_PATH=$(dirname "${0}")
cd "${CURRENT_PATH}" || exit

cd ../

./venv/bin/coverage3 run 1>/dev/null
./venv/bin/coverage3 report
./venv/bin/coverage3 html 1>/dev/null

#!/usr/bin/env bash
set -e

CURRENT_PATH=$(dirname "${0}")
cd "${CURRENT_PATH}" || exit

cd ../ || exit

source ./venv/bin/activate
flake8 .
deactivate

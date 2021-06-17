#!/usr/bin/env bash
set -e

CURRENT_PATH=$(dirname "${0}")
cd "${CURRENT_PATH}" || exit

cd ../ || exit

source ./venv/bin/activate
find ./ \
  -type f \
  -name "*.py" \
  -not -path "./venv/*" \
  -exec pylint '{}' +
deactivate

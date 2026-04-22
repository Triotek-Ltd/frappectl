#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

log() {
  printf '[frappectl-dev] %s\n' "$1"
}

fail() {
  printf '[frappectl-dev] ERROR: %s\n' "$1" >&2
  exit 1
}

ensure_local_project() {
  [[ -f "pyproject.toml" ]] || fail "pyproject.toml not found. Run this from the project root."
}

ensure_python_and_pip() {
  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    fail "Python executable not found: $PYTHON_BIN"
  fi

  if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    fail "pip is not available for $PYTHON_BIN"
  fi
}

install_editable() {
  log "Installing frappectl in editable mode..."
  "$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel
  "$PYTHON_BIN" -m pip install -e .
}

verify_command() {
  if ! command -v frappectl >/dev/null 2>&1; then
    fail "frappectl command not found after editable install."
  fi

  if ! frappectl --help >/dev/null 2>&1; then
    fail "frappectl installed, but help command failed."
  fi
}

print_next_steps() {
  cat <<'EOF'

Editable install complete.

Useful commands:
  frappectl --help
  python -m frappectl --help
  frappectl setup step 1 --bench testbench

EOF
}

main() {
  ensure_local_project
  ensure_python_and_pip
  install_editable
  verify_command
  print_next_steps
}

main "$@"

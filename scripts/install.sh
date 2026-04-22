#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-}"
REF="${REF:-main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INSTALL_MODE="${INSTALL_MODE:-git}"   # git | local

log() {
  printf '[frappectl] %s\n' "$1"
}

fail() {
  printf '[frappectl] ERROR: %s\n' "$1" >&2
  exit 1
}

require_linux() {
  if [[ "${OSTYPE:-}" != linux* ]]; then
    fail "This installer targets Linux servers. Current OS is not Linux."
  fi
}

detect_pkg_manager() {
  if command -v apt-get >/dev/null 2>&1; then
    echo "apt"
    return
  fi
  fail "Unsupported package manager. Only apt-based systems are supported right now."
}

ensure_python_and_pip() {
  local pkg_manager
  pkg_manager="$(detect_pkg_manager)"

  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    log "Python not found. Installing Python and pip..."
    sudo "$pkg_manager" update
    sudo "$pkg_manager" install -y python3 python3-pip python3-venv
  fi

  if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
    log "pip not available. Installing pip..."
    sudo "$pkg_manager" update
    sudo "$pkg_manager" install -y python3-pip
  fi
}

upgrade_pip() {
  log "Upgrading pip..."
  "$PYTHON_BIN" -m pip install --upgrade pip
}

install_from_git() {
  [[ -n "$REPO_URL" ]] || fail "REPO_URL is required when INSTALL_MODE=git"
  log "Installing frappectl from Git..."
  "$PYTHON_BIN" -m pip install "git+${REPO_URL}@${REF}"
}

install_from_local() {
  [[ -f "pyproject.toml" ]] || fail "pyproject.toml not found. Run from project root for local install."
  log "Installing frappectl from local project..."
  "$PYTHON_BIN" -m pip install .
}

verify_command() {
  if ! command -v frappectl >/dev/null 2>&1; then
    fail "frappectl command not found after install."
  fi

  if ! frappectl --help >/dev/null 2>&1; then
    fail "frappectl installed, but help command failed."
  fi
}

print_next_steps() {
  cat <<'EOF'

frappectl installed successfully.

Next steps:
  frappectl setup run
or:
  frappectl setup step 1 --bench <bench-name>

EOF
}

main() {
  require_linux
  ensure_python_and_pip
  upgrade_pip

  case "$INSTALL_MODE" in
    git)
      install_from_git
      ;;
    local)
      install_from_local
      ;;
    *)
      fail "Unknown INSTALL_MODE: $INSTALL_MODE"
      ;;
  esac

  verify_command
  print_next_steps
}

main "$@"
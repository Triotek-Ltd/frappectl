#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/Triotek-Ltd/frappectl.git}"
REF="${REF:-main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INSTALL_MODE="${INSTALL_MODE:-git}"   # git | local
BENCH_NAME="${BENCH_NAME:-}"
RUN_SETUP="${RUN_SETUP:-yes}"

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

require_root() {
  if [[ "$(id -u)" -ne 0 ]]; then
    fail "Run this installer as root so frappectl is installed system-wide and can manage /etc, /opt, and /var/log paths."
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
  log "Upgrading pip, setuptools, and wheel..."
  "$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel
}

install_from_git() {
  log "Installing frappectl from Git (${REPO_URL}@${REF})..."
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

prompt_bench_name() {
  if [[ -n "${BENCH_NAME}" ]]; then
    return
  fi

  read -r -p "Bench name to set up: " BENCH_NAME
  [[ -n "${BENCH_NAME}" ]] || fail "Bench name is required when RUN_SETUP=yes."
}

run_full_setup() {
  if [[ "${RUN_SETUP}" != "yes" ]]; then
    return
  fi

  prompt_bench_name
  log "Starting full setup for bench '${BENCH_NAME}'..."
  frappectl setup run --bench "${BENCH_NAME}"
}

print_next_steps() {
  cat <<'EOF'

frappectl install and setup completed.

For maintenance later, use commands like:
  frappectl bench info --bench <bench-name>
  frappectl site list --bench <bench-name>
  frappectl jobs health --bench <bench-name>

EOF
}

main() {
  require_linux
  require_root
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
  run_full_setup
  print_next_steps
}

main "$@"

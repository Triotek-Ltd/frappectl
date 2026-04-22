#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/Triotek-Ltd/frappectl.git}"
REF="${REF:-main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INSTALL_MODE="${INSTALL_MODE:-git}"   # git | local
INSTALL_ROOT="${INSTALL_ROOT:-/opt/frappe-installer}"
APP_VENV_PATH="${APP_VENV_PATH:-${INSTALL_ROOT}/venv}"
APP_BIN_DIR="${APP_BIN_DIR:-/usr/local/bin}"

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
    fail "Run this installer as root so frappectl is installed system-wide."
  fi
}

detect_pkg_manager() {
  if command -v apt-get >/dev/null 2>&1; then
    echo "apt"
    return
  fi
  fail "Unsupported package manager. Only apt-based systems are supported right now."
}

ensure_prerequisites() {
  local pkg_manager
  pkg_manager="$(detect_pkg_manager)"

  log "Installing installer prerequisites if needed..."
  "$pkg_manager" update
  "$pkg_manager" install -y python3 python3-pip python3-venv git

  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    fail "Configured PYTHON_BIN '${PYTHON_BIN}' was not found after prerequisite install."
  fi
}

ensure_app_venv() {
  mkdir -p "${INSTALL_ROOT}"
  if [[ ! -x "${APP_VENV_PATH}/bin/python" ]]; then
    log "Creating isolated frappectl virtual environment at ${APP_VENV_PATH}..."
    "$PYTHON_BIN" -m venv "${APP_VENV_PATH}"
  fi
}

upgrade_venv_pip() {
  log "Upgrading pip, setuptools, and wheel in the installer venv..."
  "${APP_VENV_PATH}/bin/python" -m pip install --upgrade pip setuptools wheel
}

install_from_git() {
  log "Installing frappectl from Git (${REPO_URL}@${REF})..."
  "${APP_VENV_PATH}/bin/python" -m pip install --upgrade "git+${REPO_URL}@${REF}"
}

install_from_local() {
  [[ -f "pyproject.toml" ]] || fail "pyproject.toml not found. Run from project root for local install."
  log "Installing frappectl from local project..."
  "${APP_VENV_PATH}/bin/python" -m pip install --upgrade .
}

link_command() {
  install -d "${APP_BIN_DIR}"
  ln -sf "${APP_VENV_PATH}/bin/frappectl" "${APP_BIN_DIR}/frappectl"
}

verify_command() {
  link_command

  if ! command -v frappectl >/dev/null 2>&1; then
    fail "frappectl command not found after install."
  fi

  if ! frappectl --help >/dev/null 2>&1; then
    fail "frappectl installed, but help command failed."
  fi
}

print_summary() {
  cat <<EOF

frappectl install complete.

Installed:
  Repo URL: ${REPO_URL}
  Ref: ${REF}
  Install mode: ${INSTALL_MODE}
  Install root: ${INSTALL_ROOT}
  App venv: ${APP_VENV_PATH}
  CLI link: ${APP_BIN_DIR}/frappectl

Next steps:
  1. Verify the CLI:
     sudo frappectl --help
  2. Inspect setup progress helpers:
     sudo frappectl setup --help
  3. Start bench setup manually through the CLI:
     sudo frappectl setup run --bench <bench-name>

EOF
}

main() {
  require_linux
  require_root
  ensure_prerequisites
  ensure_app_venv
  upgrade_venv_pip

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
  print_summary
}

main "$@"

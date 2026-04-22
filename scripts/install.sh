#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/Triotek-Ltd/frappectl.git}"
REF="${REF:-main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
INSTALL_MODE="${INSTALL_MODE:-git}"   # git | local
BENCH_NAME="${BENCH_NAME:-}"
RUN_SETUP="${RUN_SETUP:-yes}"
BENCH_USER="${BENCH_USER:-}"
DEPLOY_MODE="${DEPLOY_MODE:-}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-}"
DEFAULT_SITE_NAME="${DEFAULT_SITE_NAME:-}"
SET_AS_DEFAULT_SITE="${SET_AS_DEFAULT_SITE:-}"
DNS_READY="${DNS_READY:-}"
SSL_EMAIL="${SSL_EMAIL:-}"
GIT_USER_NAME="${GIT_USER_NAME:-}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-}"
GIT_PROVIDER="${GIT_PROVIDER:-}"
PRIVATE_REPO_MODE="${PRIVATE_REPO_MODE:-}"
GENERATE_GIT_SSH_KEY="${GENERATE_GIT_SSH_KEY:-}"
SSH_ADMIN_MODE="${SSH_ADMIN_MODE:-}"
DISABLE_ROOT_SSH="${DISABLE_ROOT_SSH:-}"
DISABLE_PASSWORD_SSH="${DISABLE_PASSWORD_SSH:-}"
ENABLE_FAIL2BAN="${ENABLE_FAIL2BAN:-}"
AUTO_BACKUP_ENABLED="${AUTO_BACKUP_ENABLED:-}"
BACKUP_FREQUENCY="${BACKUP_FREQUENCY:-}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-}"
SECONDARY_BACKUP_MODE="${SECONDARY_BACKUP_MODE:-}"
PYTHON_BIN_OVERRIDE="${PYTHON_BIN_OVERRIDE:-}"

log() {
  printf '[frappectl] %s\n' "$1"
}

fail() {
  printf '[frappectl] ERROR: %s\n' "$1" >&2
  exit 1
}

reject_secret_env() {
  local blocked_vars=(
    "SITE_ADMIN_PASSWORD"
    "DB_ROOT_PASSWORD"
  )
  local var_name

  for var_name in "${blocked_vars[@]}"; do
    if [[ -n "${!var_name:-}" ]]; then
      fail "${var_name} must not be passed through the installer environment. Enter sensitive values interactively during setup."
    fi
  done
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

seed_setup_config() {
  local config_dir="/etc/frappe-installer/benches"
  local config_path="${config_dir}/${BENCH_NAME}.env"
  mkdir -p "${config_dir}"

  cat > "${config_path}" <<EOF
BENCH_NAME=${BENCH_NAME}
EOF

  append_if_set() {
    local key="$1"
    local value="$2"
    if [[ -n "${value}" ]]; then
      printf '%s=%s\n' "${key}" "${value}" >> "${config_path}"
    fi
  }

  append_if_set "BENCH_USER" "${BENCH_USER}"
  append_if_set "DEPLOY_MODE" "${DEPLOY_MODE}"
  append_if_set "FRAPPE_BRANCH" "${FRAPPE_BRANCH}"
  append_if_set "PYTHON_BIN" "${PYTHON_BIN_OVERRIDE}"
  append_if_set "DEFAULT_SITE_NAME" "${DEFAULT_SITE_NAME}"
  append_if_set "SET_AS_DEFAULT_SITE" "${SET_AS_DEFAULT_SITE}"
  append_if_set "DNS_READY" "${DNS_READY}"
  append_if_set "SSL_EMAIL" "${SSL_EMAIL}"
  append_if_set "GIT_USER_NAME" "${GIT_USER_NAME}"
  append_if_set "GIT_USER_EMAIL" "${GIT_USER_EMAIL}"
  append_if_set "GIT_PROVIDER" "${GIT_PROVIDER}"
  append_if_set "PRIVATE_REPO_MODE" "${PRIVATE_REPO_MODE}"
  append_if_set "GENERATE_GIT_SSH_KEY" "${GENERATE_GIT_SSH_KEY}"
  append_if_set "SSH_ADMIN_MODE" "${SSH_ADMIN_MODE}"
  append_if_set "DISABLE_ROOT_SSH" "${DISABLE_ROOT_SSH}"
  append_if_set "DISABLE_PASSWORD_SSH" "${DISABLE_PASSWORD_SSH}"
  append_if_set "ENABLE_FAIL2BAN" "${ENABLE_FAIL2BAN}"
  append_if_set "AUTO_BACKUP_ENABLED" "${AUTO_BACKUP_ENABLED}"
  append_if_set "BACKUP_FREQUENCY" "${BACKUP_FREQUENCY}"
  append_if_set "BACKUP_RETENTION_DAYS" "${BACKUP_RETENTION_DAYS}"
  append_if_set "SECONDARY_BACKUP_MODE" "${SECONDARY_BACKUP_MODE}"
}

print_setup_summary() {
  cat <<EOF

Installer setup summary
=======================
Repo URL: ${REPO_URL}
Ref: ${REF}
Install mode: ${INSTALL_MODE}
Bench name: ${BENCH_NAME}
Bench user: ${BENCH_USER:-[prompt during setup]}
Deploy mode: ${DEPLOY_MODE:-[prompt during setup]}
Frappe branch: ${FRAPPE_BRANCH:-[prompt during setup]}
Python bin: ${PYTHON_BIN_OVERRIDE:-[prompt during setup]}
Default site: ${DEFAULT_SITE_NAME:-[prompt during setup]}
Set default site: ${SET_AS_DEFAULT_SITE:-[prompt during setup]}
DNS ready: ${DNS_READY:-[prompt during setup]}
SSL email: ${SSL_EMAIL:-[prompt during setup]}
Git user name: ${GIT_USER_NAME:-[prompt during setup]}
Git user email: ${GIT_USER_EMAIL:-[prompt during setup]}
Git provider: ${GIT_PROVIDER:-[prompt during setup]}
Private repo mode: ${PRIVATE_REPO_MODE:-[prompt during setup]}
Generate Git SSH key: ${GENERATE_GIT_SSH_KEY:-[prompt during setup]}
SSH admin mode: ${SSH_ADMIN_MODE:-[prompt during setup]}
Disable root SSH: ${DISABLE_ROOT_SSH:-[prompt during setup]}
Disable password SSH: ${DISABLE_PASSWORD_SSH:-[prompt during setup]}
Enable fail2ban: ${ENABLE_FAIL2BAN:-[prompt during setup]}
Auto backups: ${AUTO_BACKUP_ENABLED:-[prompt during setup]}
Backup frequency: ${BACKUP_FREQUENCY:-[prompt during setup]}
Backup retention days: ${BACKUP_RETENTION_DAYS:-[prompt during setup]}
Secondary backup mode: ${SECONDARY_BACKUP_MODE:-[prompt during setup]}

Sensitive values
----------------
Administrator and MariaDB root passwords are always collected interactively during setup.

EOF
}

run_full_setup() {
  if [[ "${RUN_SETUP}" != "yes" ]]; then
    return
  fi

  prompt_bench_name
  seed_setup_config
  print_setup_summary
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
  reject_secret_env
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

# frappectl

`frappectl` is a Linux-first installer and maintenance CLI for Frappe benches. The intended product flow is:

- `scripts/install.sh` does the first-time server setup work
- `frappectl` is used afterward for maintenance and operations

Installer state is stored under `/etc/frappe-installer`, `/opt/frappe-installer`, and `/var/log/frappe-installer`.

## What It Does

- installs `frappectl` from the GitHub repo
- launches the full setup flow during install
- installs host dependencies for a non-Docker Bench setup
- initializes a bench as the configured bench user
- fetches apps from the configured app catalog
- creates and prepares the default site
- enables DNS multitenant bench routing for future sites on that bench
- wires production with nginx and supervisor
- enables HTTPS with Let's Encrypt when DNS is ready
- provides direct CLI commands for day-2 maintenance
- installs Bench CLI in an isolated venv under `/opt/frappe-installer/bench-cli`

## Server Requirements

- Ubuntu or Debian style Linux host
- run install and setup actions as `root`
- `sudo` available
- public DNS ready before HTTPS

## First-Time Server Setup

Fastest path from the real GitHub repo:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

That installer defaults to:

- repo: `https://github.com/Triotek-Ltd/frappectl.git`
- ref: `main`
- setup: `RUN_SETUP=yes`

It will:

1. install Python packaging prerequisites
2. create an isolated app virtualenv under `/opt/frappe-installer/venv`
3. install `frappectl` from GitHub into that virtualenv
4. link the `frappectl` command into `/usr/local/bin`
5. verify the CLI is available
6. ask for a bench name if `BENCH_NAME` was not provided
7. run the full setup flow immediately

If you want to provide the bench name up front:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo BENCH_NAME=mybench bash
```

If you want to pin another branch or tag:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo REF=main BENCH_NAME=mybench bash
```

If you already cloned the repo on the server, run:

```bash
sudo BENCH_NAME=mybench bash scripts/install.sh
```

If you need install-only behavior for debugging, without running the setup flow:

```bash
sudo RUN_SETUP=no bash scripts/install.sh
```

## What The Installer Setup Covers

The installer-driven setup flow follows the staged design in `rnd/prompt-setpup`.

- Step 1: collects bench identity such as `BENCH_NAME`, `BENCH_USER`, and `DEPLOY_MODE`
- Step 2: derives paths like `/home/<bench-user>/<bench-name>` and prepares installer-owned directories
- Step 5: installs MariaDB, Redis, Python tooling, Node/Yarn, nginx, supervisor, and wkhtmltopdf
- Step 6: installs Bench CLI and runs `bench init`
- Step 7: resolves and fetches apps
- Step 8: creates the default site, installs site apps, migrates, and clears cache
- Step 9: runs production setup and reloads nginx and supervisor safely
- Step 9: enables DNS multitenant routing and clears `currentsite.txt` so later sites route by hostname cleanly
- Step 10: runs `bench setup lets-encrypt` when DNS is ready

So the installer is now the thing that should create the bench and default site on first run.

## Maintenance CLI After Setup

After the server is set up, use `frappectl` for maintenance.

### Bench

```bash
sudo frappectl bench info --bench mybench
sudo frappectl bench version --bench mybench
sudo frappectl bench doctor --bench mybench
sudo frappectl bench restart --bench mybench
```

### Sites

```bash
sudo frappectl site info --bench mybench
sudo frappectl site list --bench mybench
sudo frappectl site migrate --bench mybench
sudo frappectl site use erp.example.com --bench mybench
sudo frappectl site multitenant-status --bench mybench
```

### Apps

```bash
sudo frappectl apps plan --bench mybench
sudo frappectl apps prepare-fetch --bench mybench
sudo frappectl apps list-site --bench mybench --site erp.example.com
```

### Production And HTTPS

```bash
sudo frappectl production status --bench mybench
sudo frappectl production safe-restart
sudo frappectl ssl status --bench mybench
```

### Jobs And Health

```bash
sudo frappectl jobs status --bench mybench
sudo frappectl jobs health --bench mybench
sudo frappectl jobs restart --bench mybench
sudo frappectl diagnostics health --bench mybench
```

### Operations Menu Reference

```bash
sudo frappectl menu open --bench mybench
```

This prints the mapped operations surface and the direct commands behind each section.

## Notes

- install, setup, production, and HTTPS commands are intentionally Linux-only and root-gated
- `.local` domains and benches with `DNS_READY=no` will skip HTTPS automatically
- installer state is stored outside the bench so multi-bench usage stays consistent

## Development Install

```bash
bash scripts/dev-install.sh
```

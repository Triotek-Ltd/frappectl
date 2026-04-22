# frappectl

`frappectl` is a Linux-first installer and maintenance CLI for Frappe benches. The intended product flow is:

- `scripts/install.sh` installs the `frappectl` CLI itself
- `frappectl` is then used for bench setup, maintenance, and operations

Installer state is stored under `/etc/frappe-installer`, `/opt/frappe-installer`, and `/var/log/frappe-installer`.

## What It Does

- installs `frappectl` from the GitHub repo
- installs the CLI in an isolated app virtualenv
- provides direct CLI commands for day-2 maintenance
- installs Bench CLI in an isolated venv under `/opt/frappe-installer/bench-cli`

## Server Requirements

- Ubuntu or Debian style Linux host
- run install and setup actions as `root`
- `sudo` available
- public DNS ready before HTTPS

## Install The CLI

Fastest path from the real GitHub repo:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

That installer defaults to:

- repo: `https://github.com/Triotek-Ltd/frappectl.git`
- ref: `main`

It will:

1. install Python packaging prerequisites
2. create an isolated app virtualenv under `/opt/frappe-installer/venv`
3. install `frappectl` from GitHub into that virtualenv
4. link the `frappectl` command into `/usr/local/bin`
5. verify the CLI is available

If you want to pin another branch or tag:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo REF=main bash
```

If you already cloned the repo on the server, run:

```bash
sudo bash scripts/install.sh
```

## Set Up A Bench With The CLI

Recommended first-time setup command:

```bash
sudo frappectl setup run --bench <bench-name>
```

Example:

```bash
sudo frappectl setup run --bench bookman
```

Recommended answers on a normal Ubuntu server with `python3`:

- `Bench user`: `frappe`
- `Deployment mode`: `production`
- `Frappe branch`: `version-15`
- `Python executable`: `python3`

Use `version-16` only if you have a Python `3.14+` executable available and you point setup at it.

## Track Progress During Setup

Check overall setup state:

```bash
sudo frappectl setup status --bench <bench-name>
```

Check short progress summary:

```bash
sudo frappectl setup progress --bench <bench-name>
```

Inspect saved setup values:

```bash
sudo frappectl setup inspect --bench <bench-name>
```

Show the config/state/log file paths:

```bash
sudo frappectl setup files --bench <bench-name>
```

## Resume After A Failure

Resume from the next incomplete step:

```bash
sudo frappectl setup resume --bench <bench-name>
```

Example:

```bash
sudo frappectl setup resume --bench bookman
```

## Run Setup Step-By-Step

If you want to drive setup manually, run one step at a time:

```bash
sudo frappectl setup step 1 --bench <bench-name>
sudo frappectl setup step 2 --bench <bench-name>
sudo frappectl setup step 3 --bench <bench-name>
sudo frappectl setup step 4 --bench <bench-name>
sudo frappectl setup step 5 --bench <bench-name>
sudo frappectl setup step 6 --bench <bench-name>
sudo frappectl setup step 7 --bench <bench-name>
sudo frappectl setup step 8 --bench <bench-name>
sudo frappectl setup step 9 --bench <bench-name>
sudo frappectl setup step 10 --bench <bench-name>
sudo frappectl setup step 11 --bench <bench-name>
sudo frappectl setup step 12 --bench <bench-name>
```

Useful pattern:

```bash
sudo frappectl setup step 5 --bench bookman
sudo frappectl setup progress --bench bookman
```

## Quick Command Sequence

Install the CLI:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

Verify install:

```bash
sudo frappectl --help
sudo frappectl setup --help
```

Run setup:

```bash
sudo frappectl setup run --bench bookman
```

Check progress in another shell if needed:

```bash
sudo frappectl setup progress --bench bookman
sudo frappectl setup status --bench bookman
```

## First Successful Production Run

Use this as the default first run on a fresh Ubuntu server:

```bash
sudo frappectl setup run --bench bookman
```

Recommended interactive answers:

- `Bench user`: `frappe`
- `Deployment mode`: `production`
- `Generate Git SSH key for bench user?`: `yes` if you plan to fetch private repos, otherwise `no`
- `Preferred Git provider`: `github`
- `Private repo access`: `public_only` unless you know you need private repos now
- `Frappe branch`: `version-15`
- `Python executable`: `python3`
- `SSH admin mode`: `generate`
- `Disable root SSH`: `yes`
- `Disable password SSH`: `yes` only if you already have working SSH key access
- `Enable Fail2ban?`: `yes`
- `Default site name`: your real hostname, for example `erp.example.com`
- `Administrator password`: choose manually when prompted
- `MariaDB root password`: choose manually when prompted
- `Set as default site?`: `yes`
- `Is DNS already pointing to this server?`: `no` unless DNS is already live
- `SSL email`: your real admin email
- `Auto backups`: `yes`
- `Backup frequency`: `daily`
- `Backup retention days`: `7`

Safer choices for a first run:

- if you are not fully sure about SSH hardening yet, keep `Disable password SSH` as `no`
- if the server is not publicly reachable yet, keep `DNS ready` as `no`
- if you are using the server’s normal Python 3.12, stay on `version-15`

After setup finishes, check:

```bash
sudo frappectl setup status --bench bookman
sudo frappectl bench info --bench bookman
sudo frappectl site info --bench bookman
sudo frappectl production status --bench bookman
sudo frappectl site multitenant-status --bench bookman
sudo frappectl ssl status --bench bookman
```

If setup stops partway through:

```bash
sudo frappectl setup progress --bench bookman
sudo frappectl setup status --bench bookman
sudo frappectl setup resume --bench bookman
```

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

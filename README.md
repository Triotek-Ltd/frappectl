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

After installation, run setup through the CLI so progress and retries stay explicit:

```bash
sudo frappectl setup run --bench <bench-name>
```

You can also drive setup step-by-step:

```bash
sudo frappectl setup step 1 --bench <bench-name>
sudo frappectl setup step 2 --bench <bench-name>
sudo frappectl setup step 3 --bench <bench-name>
```

Progress helpers:

```bash
sudo frappectl setup status --bench <bench-name>
sudo frappectl setup progress --bench <bench-name>
sudo frappectl setup inspect --bench <bench-name>
sudo frappectl setup files --bench <bench-name>
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

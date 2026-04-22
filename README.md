# frappectl

`frappectl` is a Linux-first installer and maintenance CLI for Frappe benches. The intended product flow is:

- `scripts/install.sh` installs the `frappectl` CLI itself
- `frappectl` is then used for bench setup, maintenance, and operations

Installer state is stored under `/etc/frappe-installer`, `/opt/frappe-installer`, and `/var/log/frappe-installer`.

## What It Does

- installs `frappectl` from the GitHub repo
- installs the CLI in an isolated app virtualenv under `/opt/frappe-installer/venv`
- links `frappectl` into `/usr/local/bin`
- provides CLI commands for bench setup, maintenance, and operations

## Server Requirements

- Ubuntu or Debian style Linux host
- run install actions as `root`
- `sudo` available

## Step 1: Install The CLI

Fastest path from the real GitHub repo:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

If you want to pin another branch or tag:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo REF=main bash
```

If you already cloned the repo on the server, run:

```bash
sudo bash scripts/install.sh
```

Verify the CLI:

```bash
sudo frappectl --help
sudo frappectl setup --help
```

`scripts/install.sh` only installs `frappectl`. It does not create a bench, create a site, or run setup automatically.

## Step 2: Run The Actual Setup Commands

After the CLI is installed, these are the actual commands to complete setup Steps 1 to 12:

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

The same commands with step names:

```bash
sudo frappectl setup step 1 --bench <bench-name>   # System Preparation
sudo frappectl setup step 2 --bench <bench-name>   # System Cleanup & Layout
sudo frappectl setup step 3 --bench <bench-name>   # Security Hardening
sudo frappectl setup step 4 --bench <bench-name>   # User & Development Environment Setup
sudo frappectl setup step 5 --bench <bench-name>   # Install Dependencies
sudo frappectl setup step 6 --bench <bench-name>   # Bench Initialization
sudo frappectl setup step 7 --bench <bench-name>   # Apps Fetch
sudo frappectl setup step 8 --bench <bench-name>   # Default Site Setup
sudo frappectl setup step 9 --bench <bench-name>   # Production Setup
sudo frappectl setup step 10 --bench <bench-name>  # Enable HTTPS
sudo frappectl setup step 11 --bench <bench-name>  # Bench Operations
sudo frappectl setup step 12 --bench <bench-name>  # Finalization, Health Checks, and Backup Automation
```

If you prefer one command instead of running all 12 yourself:

```bash
sudo frappectl setup run --bench <bench-name>
```

Recommended first answers:

- `Bench user`: `frappe`
- `Deployment mode`: `production`
- `Frappe branch`: the branch your project requires
- `Python executable`: a Python executable compatible with that branch

Choose a Frappe branch and Python that actually match each other.

Bench CLI itself is installed later during setup Step 6, not by `scripts/install.sh`.

## Step 3: Track Progress While Those Commands Run

Use these commands while setup is running:

```bash
sudo frappectl setup progress --bench <bench-name>
sudo frappectl setup status --bench <bench-name>
sudo frappectl setup inspect --bench <bench-name>
sudo frappectl setup files --bench <bench-name>
```

## Step 4: Resume If One Of The 12 Steps Stops

Resume from the next incomplete step:

```bash
sudo frappectl setup resume --bench <bench-name>
```

## Step 5: First Production-Style Run

Use this on a fresh Ubuntu server:

```bash
sudo frappectl setup run --bench <bench-name>
```

Recommended interactive answers:

- `Bench user`: `frappe`
- `Deployment mode`: `production`
- `Generate Git SSH key for bench user?`: `yes` if you plan to fetch private repos, otherwise `no`
- `Preferred Git provider`: `github`
- `Private repo access`: `public_only` unless you know you need private repos now
- `Frappe branch`: the branch your project requires
- `Python executable`: a Python executable compatible with that branch
- `SSH admin mode`: `generate`
- `Disable root SSH`: `yes`
- `Disable password SSH`: `yes` only if you already have working SSH key access
- `Enable Fail2ban?`: `yes`
- `Default site name`: your real hostname
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
- make sure the selected Python executable is supported by the branch you picked

After setup finishes, check:

```bash
sudo frappectl setup status --bench <bench-name>
sudo frappectl bench info --bench <bench-name>
sudo frappectl site info --bench <bench-name>
sudo frappectl production status --bench <bench-name>
sudo frappectl site multitenant-status --bench <bench-name>
sudo frappectl ssl status --bench <bench-name>
```

## Maintenance CLI After Setup

After the server is set up, use `frappectl` for maintenance.

### Bench

```bash
sudo frappectl bench info --bench <bench-name>
sudo frappectl bench version --bench <bench-name>
sudo frappectl bench doctor --bench <bench-name>
sudo frappectl bench restart --bench <bench-name>
```

### Sites

```bash
sudo frappectl site info --bench <bench-name>
sudo frappectl site list --bench <bench-name>
sudo frappectl site migrate --bench <bench-name>
sudo frappectl site use <site-name> --bench <bench-name>
sudo frappectl site multitenant-status --bench <bench-name>
```

### Apps

```bash
sudo frappectl apps plan --bench <bench-name>
sudo frappectl apps prepare-fetch --bench <bench-name>
sudo frappectl apps list-site --bench <bench-name> --site <site-name>
```

### Production And HTTPS

```bash
sudo frappectl production status --bench <bench-name>
sudo frappectl production safe-restart
sudo frappectl ssl status --bench <bench-name>
```

### Jobs And Health

```bash
sudo frappectl jobs status --bench <bench-name>
sudo frappectl jobs health --bench <bench-name>
sudo frappectl jobs restart --bench <bench-name>
sudo frappectl diagnostics health --bench <bench-name>
```

### Operations Menu Reference

```bash
sudo frappectl menu open --bench <bench-name>
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

# frappectl Playbook

This is the operator playbook overview for `frappectl`.

Use this file as the main guide for:

- installing the CLI
- setting up the first production bench and default site
- tracking setup progress
- running day-2 bench, site, app, jobs, and production commands

Primary reading now lives in the book:

- [book/README.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\README.md)
- [01. Bench Lifecycle](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\01-bench-lifecycle.md)

Source-of-truth companions:

- expected bench operations contract: [bench.txt](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench.txt)
- actual implementation status: [bench-implementation-checklist.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench-implementation-checklist.md)

## 1. Install The CLI

Install from GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

Install from a cloned repo:

```bash
sudo bash scripts/install.sh
```

Verify:

```bash
sudo frappectl --help
sudo frappectl setup --help
```

Important:

- `scripts/install.sh` installs the CLI only
- it does not create a bench
- it does not create a site
- it does not run setup automatically

## 2. Set Up The First Production Bench

Run the full interactive setup:

```bash
sudo frappectl setup run --bench <bench-name>
```

This setup flow is the path that prepares:

- the bench
- all apps fetched into the bench
- the first default site
- site app installation based on the chosen industry and business modules
- production wiring
- HTTPS when DNS is ready
- backup automation

If you want to run the setup one step at a time:

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

Recommended first-run answers:

- `Bench user`: `frappe`
- `Deployment mode`: `production`
- `Frappe branch`: the branch your project requires
- `Python executable`: a Python executable compatible with that branch

## 3. Track Progress While Setup Runs

Use these in another shell:

```bash
sudo frappectl setup progress --bench <bench-name>
sudo frappectl setup status --bench <bench-name>
sudo frappectl setup inspect --bench <bench-name>
sudo frappectl setup files --bench <bench-name>
```

If setup stops:

```bash
sudo frappectl setup resume --bench <bench-name>
```

## 4. Bench Commands After Setup

```bash
sudo frappectl bench info --bench <bench-name>
sudo frappectl bench version --bench <bench-name>
sudo frappectl bench doctor --bench <bench-name>
sudo frappectl bench restart --bench <bench-name>
```

## 5. Site Commands After Setup

Show current site state:

```bash
sudo frappectl site info --bench <bench-name>
sudo frappectl site current-default --bench <bench-name>
sudo frappectl site list --bench <bench-name>
```

Create and manage sites:

```bash
sudo frappectl site create --bench <bench-name> --site <site-name>
sudo frappectl site set-default <site-name> --bench <bench-name>
sudo frappectl site use <site-name> --bench <bench-name>
sudo frappectl site migrate --bench <bench-name> --site <site-name>
sudo frappectl site set-config <key> <value> --bench <bench-name> --site <site-name>
```

Multitenant check:

```bash
sudo frappectl site multitenant-status --bench <bench-name>
```

## 6. App Commands After Setup

Inspect the app plan and fetch state:

```bash
sudo frappectl apps plan --bench <bench-name>
sudo frappectl apps status --bench <bench-name>
sudo frappectl apps prepare-fetch --bench <bench-name>
```

List apps installed on a site:

```bash
sudo frappectl apps list-site --bench <bench-name> --site <site-name>
```

Important current behavior:

- setup Step 7 fetches all apps into the bench
- setup Step 8 is where you choose which site apps to install
- site selection matters for installation, not for fetch

## 7. Jobs And Health Commands

```bash
sudo frappectl jobs status --bench <bench-name>
sudo frappectl jobs health --bench <bench-name>
sudo frappectl jobs restart --bench <bench-name>
sudo frappectl jobs enable-scheduler --bench <bench-name> --site <site-name>
sudo frappectl jobs disable-scheduler --bench <bench-name> --site <site-name>
sudo frappectl diagnostics health --bench <bench-name>
sudo frappectl diagnostics preflight
```

## 8. Production And HTTPS Commands

```bash
sudo frappectl production prepare --bench <bench-name>
sudo frappectl production status --bench <bench-name>
sudo frappectl production reload-nginx
sudo frappectl production restart-supervisor
sudo frappectl production safe-restart
sudo frappectl ssl prepare --bench <bench-name>
sudo frappectl ssl status --bench <bench-name>
```

## 9. Bench Operations Menu Reference

```bash
sudo frappectl menu open --bench <bench-name>
```

Right now this is a mapped operations reference, not yet the full interactive bench operations center from `bench.txt`.

## 10. What Is Already Real vs Still Missing

Before relying on a command group, check:

- [bench-implementation-checklist.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench-implementation-checklist.md)

Current reality:

- setup is the strongest implemented part
- site commands are improving and now include create/set-default/current-default/set-config
- jobs and production commands are partly implemented
- backup/restore, dangerous operations, and full maintenance flows are still not complete

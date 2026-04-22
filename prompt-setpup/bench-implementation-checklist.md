# Bench CLI Implementation Checklist

This file turns [bench.txt](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench.txt) into an implementation checklist for the actual CLI.

Status meanings:

- `done`: implemented in the CLI in a real usable way
- `partial`: some of the behavior exists, but not the full `bench.txt` expectation
- `missing`: not implemented yet

Rule:

- `bench.txt` is the expected contract
- this checklist is the truth tracker for what the code actually has today
- README wording should follow this checklist, not the other way around

## Current Overall Status

- Bench Lifecycle: `done`
- App Management: `partial`
- Default Site and Site Management: `partial`
- Backup and Restore: `missing`
- Updates, Upgrades, and Maintenance: `missing`
- Scheduler, Workers, and Jobs: `partial`
- Production and Service Control: `partial`
- Diagnostics and Admin Tools: `partial`
- Dangerous Operations: `missing`
- Quick Actions / Bench Operations menu UX: `partial`

## 1. Bench Lifecycle

- Initialize Bench: `done`
  - `frappectl setup step 6 --bench <bench-name>`
  - `frappectl bench prepare-init --bench <bench-name>`
  - refs:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L56)
    - [bench_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\bench_service.py#L16)
- Start Bench (Development): `done`
  - `frappectl bench start --bench <bench-name>`
  - refs:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L79)
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\integrations\bench.py#L37)
- Show Bench Version: `done`
  - `frappectl bench version --bench <bench-name>`
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L68)
- Show Bench Source Info: `done`
  - `frappectl bench source --bench <bench-name>`
  - `frappectl bench info --bench <bench-name>` remains a useful companion summary
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L55)
- Show Bench Help: `done`
  - `frappectl bench help`
  - Typer CLI surface also exists via `frappectl bench --help`

## 2. App Management

- Get App: `done`
  - done through setup Step 7 and `frappectl apps prepare-fetch --bench <bench-name>`
  - current behavior fetches all apps in the catalog into the bench
  - refs:
    - [apps.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\apps.py#L32)
    - [app_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\app_service.py#L27)
- Install App on Default Site: `partial`
  - happens during setup Step 8 after industry/module selection
  - no standalone day-2 command yet
  - refs:
    - [site_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\site_service.py#L77)
    - [app_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\app_service.py#L64)
- Install App on Another Site: `missing`
- Uninstall App from Site: `missing`
- List Apps on Site: `done`
  - `frappectl apps list-site --bench <bench-name> --site <site-name>`
  - ref:
    - [apps.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\apps.py#L60)
- Update App Source Code: `missing`
- Switch App Branch: `missing`
- Show Available App Groups: `partial`
  - `frappectl apps plan --bench <bench-name>` shows grouped plan output
  - current grouping is selection-oriented, not a complete bench-ops “available groups” UX
  - ref:
    - [apps.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\apps.py#L10)

## 3. Default Site and Site Management

- Create Default Site: `done`
  - implemented in setup Step 8
  - `frappectl site prepare --bench <bench-name>` also runs the site setup service
  - `frappectl site create --bench <bench-name> --site <site-name>` now exists for day-2 creation
  - refs:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L25)
    - [site_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\site_service.py#L12)
- Set Default Site: `done`
  - done during setup Step 8 if `SET_AS_DEFAULT_SITE=yes`
  - dedicated day-2 command now exists: `frappectl site set-default`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L71)
- Use Site: `done`
  - `frappectl site use <site-name> --bench <bench-name>`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L61)
- List Sites: `done`
  - `frappectl site list --bench <bench-name>`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L39)
- Migrate Site: `done`
  - `frappectl site migrate --bench <bench-name> [--site <site-name>]`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L49)
- Reinstall Site: `missing`
- Drop Site: `missing`
- Set Site Config: `done`
  - `frappectl site set-config <key> <value> --bench <bench-name> [--site <site-name>]`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L108)
- Show Current Default Site: `done`
  - dedicated command now exists: `frappectl site current-default`
  - ref:
    - [site.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\site.py#L84)

## 4. Backup and Restore

- Backup Default Site: `missing`
- Backup Another Site: `missing`
- Backup All Sites: `missing`
- Restore Site from Backup: `missing`
- Validate Backup Path: `missing`
- Backup Before Upgrade: `missing`

Current reality:

- only backup automation setup/status exists right now
- refs:
  - [backup.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\backup.py#L9)
  - [backup_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\backup_service.py#L17)

## 5. Updates, Upgrades, and Maintenance

- Update All Apps and Bench: `missing`
- Pull Latest Changes Only: `missing`
- Update Bench Only: `missing`
- Update One App Only: `missing`
- Upgrade Default Site: `missing`
- Upgrade Another Site: `missing`
- Migrate Default Site: `partial`
  - covered by `site migrate` without explicit “default site” wording
- Migrate Another Site: `done`
  - `frappectl site migrate --bench <bench-name> --site <site-name>`
- Build Assets: `missing`
  - wrapper exists in integration only
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\integrations\bench.py#L181)
- Clear Cache: `missing`
  - wrapper exists in integration only
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\integrations\bench.py#L103)
- Clear Website Cache: `missing`
  - wrapper exists in integration only
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\integrations\bench.py#L110)
- Full Maintenance Run: `missing`

Current reality:

- `frappectl update plan` is just a static printed plan
- `frappectl update status` is only status display
- ref:
  - [update.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\update.py#L8)

## 6. Scheduler, Workers, and Jobs

- Enable Scheduler on Default Site: `done`
  - `frappectl jobs enable-scheduler --bench <bench-name>`
  - uses default site if `--site` not provided
  - ref:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L48)
- Disable Scheduler on Default Site: `done`
  - `frappectl jobs disable-scheduler --bench <bench-name>`
  - ref:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L60)
- Enable Scheduler on Another Site: `done`
  - same command with `--site`
- Disable Scheduler on Another Site: `done`
  - same command with `--site`
- Run Bench Doctor: `done`
  - `frappectl bench doctor --bench <bench-name>`
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L78)
- Check Scheduler Status: `partial`
  - `jobs status` exists, but not a true scheduler inspection command
  - ref:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L11)
- Check Worker Status: `partial`
  - exposed indirectly through jobs health / supervisor status summary
  - refs:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L25)
    - [health_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\health_service.py#L22)
- Check Pending Jobs: `missing`
- Restart Job Processes: `done`
  - `frappectl jobs restart --bench <bench-name>`
  - ref:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L36)
- Full Jobs Health Check: `partial`
  - `frappectl jobs health --bench <bench-name>` exists
  - but it does not yet explicitly break out scheduler, workers, and pending jobs as separate checks
  - ref:
    - [jobs.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\jobs.py#L25)

## 7. Production and Service Control

- Setup Production: `done`
  - `frappectl production prepare --bench <bench-name>`
  - also part of setup Step 9
  - ref:
    - [production.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\production.py#L11)
- Setup / Regenerate Nginx Config: `partial`
  - production setup does generate nginx config
  - there is no dedicated explicit “regenerate nginx config only” command
- Restart Bench Services: `done`
  - `frappectl bench restart --bench <bench-name>`
  - ref:
    - [bench.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\bench.py#L88)
- Reload Nginx: `done`
  - `frappectl production reload-nginx`
  - ref:
    - [production.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\production.py#L41)
- Restart Supervisor / Systemd Services: `done`
  - `frappectl production restart-supervisor`
  - ref:
    - [production.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\production.py#L49)
- Safe Restart Flow: `done`
  - `frappectl production safe-restart`
  - ref:
    - [production.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\production.py#L58)
- Force Restart Flow: `missing`

## 8. Diagnostics and Admin Tools

- Run Bench Doctor: `done`
- Show Bench Version: `done`
- Execute Python Function: `missing`
- Set Config: `missing`
- Transform Database: `missing`
- Trim Tables: `missing`
- Full Environment Health Check: `partial`
  - `frappectl diagnostics health --bench <bench-name>` exists
  - but it is still config/status summary oriented rather than the full check matrix from `bench.txt`
  - refs:
    - [diagnostics.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\diagnostics.py#L11)
    - [health_service.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\services\health_service.py#L5)

## 9. Dangerous Operations

- Reinstall Default Site: `missing`
- Reinstall Another Site: `missing`
- Drop Default Site: `missing`
- Drop Another Site: `missing`
- Restore Over Existing Site: `missing`
- Force Restart Production Services: `missing`
- Typed destructive confirmation flow: `missing`

Current reality:

- the menu explicitly says destructive site actions are not automated yet
- ref:
  - [menu.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\menu.py#L47)

## 10. Quick Actions And Bench Operations UX

- Quick Actions header exists: `partial`
  - refs:
    - [menu.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\menu.py#L17)
- Quick Action 1: Create and prepare default site: `partial`
  - shown as `site prepare`
  - creates default site through service, but not yet a polished menu action
- Quick Action 2: Install apps by industry profile: `partial`
  - app selection exists inside setup Step 8, but there is no direct day-2 action for this
- Quick Action 3: Update default site safely: `missing`
- Quick Action 4: Run jobs health check: `done`
  - shown as `jobs health`
- Quick Action 5: Backup default site now: `missing`

Bench Operations menu UX:

- full interactive operations tree from `bench.txt`: `missing`
- printed operations reference/menu: `partial`
- step 11 enabling bench operations state: `partial`
  - refs:
    - [menu.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\commands\menu.py#L25)
    - [step11_operations.py](C:\Users\Administrator\isaac\erp\frappectl\frappectl\src\frappectl\setup\steps\step11_operations.py#L5)

## Setup Flow Alignment

These parts are genuinely implemented in setup:

- Step 6 initializes the bench
- Step 7 fetches all apps into the bench
- Step 8 asks for industry/business selection and installs the selected site apps
- Step 9 prepares production and multitenant behavior
- Step 10 prepares HTTPS when DNS is ready
- Step 12 prepares backup automation

Important note:

- setup is currently stronger than the day-2 bench operations CLI
- the setup engine is the most implemented part of the product today
- the bench operations surface described in `bench.txt` still needs to be built out to match it

## Priority Build Order

If we implement against `bench.txt`, the most valuable next order is:

1. Site lifecycle commands
   - create new site
   - set default site
   - reinstall site
   - drop site
   - show current default site
2. App lifecycle commands
   - install app on site
   - uninstall app
   - update one app
   - switch app branch
3. Backup and restore commands
4. Update and maintenance flows
5. Dangerous operations with typed confirmation
6. Real interactive Bench Operations menu wrapping the above commands

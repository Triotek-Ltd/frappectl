# frappectl

`frappectl` is a Linux-first installer and operations CLI for Frappe benches.

The intended product flow is:

1. install the CLI with `scripts/install.sh`
2. use `frappectl` for setup, maintenance, and day-2 operations

## Start Here

- operator book: [book/README.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\README.md)
- section 1 book chapter: [01-bench-lifecycle.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\01-bench-lifecycle.md)
- playbook overview: [PLAYBOOK.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\PLAYBOOK.md)
- expected bench operations contract: [bench.txt](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench.txt)
- actual implementation tracker: [bench-implementation-checklist.md](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench-implementation-checklist.md)

## Current Working Flow

1. install the CLI
2. do Section 1 first:
   - [01. Bench Lifecycle](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\01-bench-lifecycle.md)
3. test Section 1 on the server
4. only after Section 1 is confirmed, move to Section 2

Current rule:

- do not jump ahead
- do not treat Section 2 and beyond as confirmed yet
- use the checklist to decide what is actually done

## Install The CLI

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

Or from a cloned repo:

```bash
sudo bash scripts/install.sh
```

Verify:

```bash
sudo frappectl --help
sudo frappectl setup --help
sudo frappectl bench --help
```

Important:

- `scripts/install.sh` installs the CLI only
- it does not create a bench
- it does not create a site
- it does not run setup automatically

After the CLI is installed, go straight to:

- [01. Bench Lifecycle](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\01-bench-lifecycle.md)

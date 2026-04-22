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
```

Important:

- `scripts/install.sh` installs the CLI only
- it does not create a bench
- it does not create a site
- it does not run setup automatically

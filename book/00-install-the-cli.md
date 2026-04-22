# 00. Install The CLI

This is the prerequisite step.

`scripts/install.sh` installs the `frappectl` CLI only.

It does not:

- create a bench
- create a site
- run setup automatically

## Install

From GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/frappectl/main/scripts/install.sh | sudo bash
```

From a cloned repo:

```bash
sudo bash scripts/install.sh
```

## Verify

```bash
sudo frappectl --help
sudo frappectl setup --help
sudo frappectl bench --help
```

## Next

After the CLI is installed, move to:

- [01. Bench Lifecycle](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\01-bench-lifecycle.md)

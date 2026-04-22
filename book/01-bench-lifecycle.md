# 01. Bench Lifecycle

Status: `validated in the CLI surface`

This chapter covers section 1 from [bench.txt](C:\Users\Administrator\isaac\erp\frappectl\frappectl\prompt-setpup\bench.txt):

- Initialize Bench
- Start Bench
- Show Bench Version
- Show Bench Source Info
- Show Bench Help

## Product Rules

- production is the default deploy mode
- the product is multi-bench oriented
- commands should prompt for a bench when one is not supplied
- bench lifecycle commands should not assume a single fixed bench

## Interactive Bench Selection

If `--bench` is not supplied:

- the active bench is used if one is already set
- if exactly one bench exists, it is used
- if multiple benches exist, the CLI prompts you to choose one
- if no bench exists yet, the CLI prompts for a bench name

## Commands

### Initialize Bench

Interactive setup step:

```bash
sudo frappectl setup step 6 --bench <bench-name>
```

Direct lifecycle wrapper:

```bash
sudo frappectl bench prepare-init --bench <bench-name>
```

### Start Bench

```bash
sudo frappectl bench start --bench <bench-name>
```

Important:

- this is a manual operator action
- it is not the default product path
- the product default is still production-first

### Show Bench Version

```bash
sudo frappectl bench version --bench <bench-name>
```

### Show Bench Source Info

```bash
sudo frappectl bench source --bench <bench-name>
sudo frappectl bench info --bench <bench-name>
```

### Show Bench Help

```bash
sudo frappectl bench help
sudo frappectl bench --help
```

## Useful Companion Commands

List benches:

```bash
sudo frappectl bench list
```

Set the active bench:

```bash
sudo frappectl bench use <bench-name>
```

## Expected Behavior

Bench Lifecycle should now give you:

- a way to initialize a bench
- a way to manually start a bench
- a version command
- a source/setup info command
- help output
- interactive bench selection when appropriate

## What To Check On Server

After testing on the server, confirm:

1. `bench prepare-init` works for a new bench
2. `bench start` works when you explicitly want it
3. `bench version` returns the actual bench version
4. `bench source` shows the right path, branch, and python
5. commands prompt for bench selection instead of failing abruptly when `--bench` is omitted

## Before Moving To Section 2

Only move on after this chapter is confirmed working on the server.

Next chapter:

- [02. App Management](C:\Users\Administrator\isaac\erp\frappectl\frappectl\book\02-app-management.md)

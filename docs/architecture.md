# Architecture

## Purpose

This repo models message-retention governance as an operational decision surface:

- which retention lanes are under legal hold
- where deletion windows are about to run
- how much export backlog exists
- whether shadow communication surfaces make retention incomplete
- whether data residency introduces additional hold risk

## Service Shape

The backend is intentionally stdlib-first:

- `WEBrick` HTTP server
- JSON responses only
- no external gem dependency required to boot locally
- `Minitest` for unit validation

That keeps the repo easy to run on a clean Windows machine.

## Decision Logic

The engine scores:

- `pending_deletions`
- `retention_gap_days`
- `export_backlog`
- `shadow_channels`
- `region_mismatch`

And turns that into:

- `freeze`
- `watch`
- `clear`

With a concrete next action, not just a numeric score.

## Why It Fits The Portfolio

This repo extends the governance and workflow cluster into communication-data retention, legal hold control, and deletion safety. It pairs naturally with:

- `compliance-event-ledger`
- `approval-workflow-orchestrator`
- `tenant-isolation-guard`
- `audit-graph-explorer`


# GitHub Actions Node.js 24 Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the CI workflow actions to their Node.js 24 major versions.

**Architecture:** Change only the two `uses:` references in the existing workflow and preserve every workflow input and permission.

**Tech Stack:** GitHub Actions, Python 3.12

## Global Constraints

- Keep `permissions: contents: read`.
- Keep `python-version: "3.12"` and `cache: "pip"`.
- Keep all install, test, and syntax-check commands unchanged.

---

### Task 1: Upgrade the action runtimes

**Files:**
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Verify the new references are initially absent**

Run `rg 'actions/checkout@v5|actions/setup-python@v6' .github/workflows/ci.yml` and expect exit 1.

- [ ] **Step 2: Apply the minimal version changes**

Change `actions/checkout@v4` to `actions/checkout@v5` and
`actions/setup-python@v5` to `actions/setup-python@v6`.

- [ ] **Step 3: Verify configuration invariants**

Require exactly one occurrence of each new reference, confirm the old
references are absent, and confirm `contents: read`, Python 3.12, and pip cache
settings remain present. Run `git diff --check`.

- [ ] **Step 4: Commit and publish**

Commit the workflow change, merge it to `main`, push, and require the resulting
CI run to finish successfully without a Node.js 20 deprecation annotation.

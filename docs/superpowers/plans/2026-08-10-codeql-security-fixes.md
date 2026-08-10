# CodeQL Security Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the three open CodeQL alerts without changing the application's intended behavior.

**Architecture:** Add a small backup-path validation boundary in the admin routes, keep the Flask entry point safe by default, and restrict the CI token at workflow scope. Unit tests exercise the path boundary and an AST-based regression test protects the debug setting.

**Tech Stack:** Python 3.12, Flask, unittest, GitHub Actions

## Global Constraints

- Preserve existing routes, templates, database commands, and authentication behavior.
- Do not alter database credentials or backup storage architecture.
- Grant the GitHub Actions token only `contents: read`.

---

### Task 1: Validate restore backup paths

**Files:**
- Modify: `backend/routes/admin.py`
- Create: `tests/test_admin_security.py`

**Interfaces:**
- Produces: `_resolve_backup_file(filename: str) -> pathlib.Path`, raising `ValueError` for an invalid selection.
- Consumes: `config.BACKUP_DIR` and filenames generated as `backup_YYYYMMDD_HHMMSS.sql`.

- [ ] **Step 1: Write failing unit tests**

Create tests that patch `routes.admin.BACKUP_DIR` to a temporary directory and assert that an existing generated backup is accepted while traversal input, arbitrary names, directories, and missing files raise `ValueError`.

- [ ] **Step 2: Verify the tests fail for the missing resolver**

Run: `python -m unittest tests.test_admin_security.AdminSecurityTest -v`

Expected: FAIL because `_resolve_backup_file` does not exist.

- [ ] **Step 3: Implement the minimal resolver and route integration**

Use a full-match regular expression for `backup_[0-9]{8}_[0-9]{6}.sql`, resolve both the configured directory and candidate, require `candidate.parent == backup_dir`, and require `candidate.is_file()`. In the restore route, resolve the submitted filename before opening it; catch `ValueError` with the existing restore failure handling.

- [ ] **Step 4: Verify the focused tests pass**

Run: `python -m unittest tests.test_admin_security.AdminSecurityTest -v`

Expected: all path-validation tests PASS.

- [ ] **Step 5: Commit the path fix**

Run: `git add backend/routes/admin.py tests/test_admin_security.py && git commit -m "fix: validate database restore paths"`

### Task 2: Disable committed Flask debug mode

**Files:**
- Modify: `backend/app.py`
- Modify: `tests/test_admin_security.py`

**Interfaces:**
- Produces: a module entry point that calls `app.run` without enabling debug mode.

- [ ] **Step 1: Add an AST regression test**

Parse `backend/app.py`, find the `app.run` call, and assert that the `debug` keyword is absent or a literal `False`.

- [ ] **Step 2: Verify the new test fails**

Run: `python -m unittest tests.test_admin_security.AdminSecurityTest.test_flask_entry_point_does_not_enable_debug -v`

Expected: FAIL because `debug=True` is committed.

- [ ] **Step 3: Remove the unsafe keyword**

Change the entry point to `app.run(host="0.0.0.0", port=5000)`.

- [ ] **Step 4: Verify the test passes**

Run the focused test again and expect PASS.

- [ ] **Step 5: Commit the debug fix**

Run: `git add backend/app.py tests/test_admin_security.py && git commit -m "fix: disable Flask debug mode by default"`

### Task 3: Restrict CI permissions and verify the repository

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Produces: workflow-level `permissions: {contents: read}`.

- [ ] **Step 1: Add a failing static assertion**

Run: `rg -U 'permissions:\n  contents: read' .github/workflows/ci.yml`

Expected: exit 1 before the workflow change.

- [ ] **Step 2: Add the minimal permissions block**

Insert `permissions:` and `contents: read` between the trigger configuration and `jobs:`.

- [ ] **Step 3: Verify permissions and all tests**

Run the `rg` assertion, `python -m unittest discover -s tests -v`, and the same AST syntax check used in CI. Expect all commands to exit 0.

- [ ] **Step 4: Commit the workflow fix**

Run: `git add .github/workflows/ci.yml && git commit -m "ci: restrict workflow token permissions"`

- [ ] **Step 5: Push and verify GitHub**

Push the feature branch, merge it to `main`, push `main`, wait for CI and CodeQL, and verify that the three alerts are closed.

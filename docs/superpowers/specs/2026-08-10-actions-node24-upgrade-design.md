# GitHub Actions Node.js 24 Upgrade Design

## Goal

Remove the Node.js 20 deprecation warning from the CI workflow without changing
the workflow's permissions, Python version, cache behavior, or test commands.

## Design

Update `actions/checkout` from major version 4 to 5 and
`actions/setup-python` from major version 5 to 6. These are the official major
versions of the actions that use the Node.js 24 runtime. Keep Python pinned to
3.12 and retain `contents: read` as the only workflow token permission.

## Verification

Statically verify both new action references and the unchanged Python and
permission settings, then push to `main` and require the CI run to succeed with
no Node.js 20 deprecation annotation.

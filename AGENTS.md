<!-- workspace-template:adaptive-delivery:start -->
## Adaptive Delivery

Use `npm exec -- workspace-template` as this repository's workspace-template entry point. Direct is the default; Ticketed is for multi-session slices; Governed is reserved for enumerated high-consequence authority. Review is read-only, allows at most two semantic repair rounds, and returns `INSUFFICIENT_EVIDENCE` when required inspection is unavailable.

Load package-owned methodology without copying it:

- Behavior changes: `npm exec -- workspace-template skills show tdd` and `npm exec -- workspace-template skills show implementation-style`.
- Diagnosis: `npm exec -- workspace-template skills show diagnose`.
- Spawned commands: `npm exec -- workspace-template skills show process-lifecycle`.
- Completion evidence: `npm exec -- workspace-template skills show verify`.
- Wayfinder only when a route-changing ambiguity remains.
- Ticket compilation only after Ticketed or Governed routing.

Discover the complete inventory with `npm exec -- workspace-template skills list`. Do not copy generic skills into this repository. The host or repository owner selects available models, agents, permissions, skills, and capabilities.
<!-- workspace-template:adaptive-delivery:end -->

## CitizensSector

- `ship-sprite-lab/` owns the Python experiment, editable `assets/idris/`, presets, CLI, and art documentation. Root npm tooling is private development infrastructure. Keep generic methodology in the retained package.
- Tooling setup: `npm ci` (Windows x64, Node 24), then `npm run skills`, `npm run workspace-template -- skills show tdd`, `npm run workspace-template -- version --json`, and `npm run doctor`. The existing manifest/lockfile is ready; contributors do not run `npm init`.
- Package commands use npm's installed-bin resolution directly: `npm run workspace-template -- <arguments>` or the managed block's `npm exec -- workspace-template ...` after installation. No custom launcher or Python environment is needed for tooling commands.
- Lab setup is separate: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ship-sprite-lab\scripts\setup.ps1` (Python 3.12+ with pip/venv). See README.md for checks and missing inputs.
- After lab setup, software/data checks: `npm.cmd run check`; packaged verification: `npm.cmd run workspace-template -- verify . --scope all`; lab diagnostics: `npm.cmd run lab -- doctor`. Tooling-only diagnostics: `npm.cmd run doctor`, `npm.cmd run skills`. Use `npm.cmd` in PowerShell to preserve `--` forwarding with npm's standard Windows entry point.
- Art validation is separate: with authorized inputs and outputs available, use `npm.cmd run lab -- validate --ship idris`, inspect its gates and exact PNGs/report at 100/50/25%, silhouettes, openings, alpha edges, landmarks and component shape. A zero exit or structural pass does not prove visual quality or game readiness. Record missing evidence. Game loading is an explicit manual smoke test in `ship-sprite-lab/docs/SMOKE_TEST.md`.
- Preserve original inputs, source provenance, geometry, private references and generated-output ignores. Onboarding never generates provider images or launches games. No LoRA, animation, hardpoints or faction work under the setup issue.
- Small reversible edits stay Direct. Work crossing sessions or contributors uses a scoped GitHub issue with one human assignee/owner, assistant, exact branch/commit, dependencies and acceptance criteria. Keep `master` and existing history; use one isolated `task/<issue>-<slug>` branch per implementation issue and a linked PR targeting `master`.
- One active editor per shared sprite asset. Agree on ownership before parallel edits; comments alone cannot atomically lock an asset. Do not overwrite another contributor's work.
- Before review, inspect the diff, run relevant checks and record visual evidence or unavailable checks. Request human review of the linked PR; merge after review/checks. Keep unrelated tasks out of the PR.
- A handoff records completed work, exact commit, changed assets/interfaces, checks and visual evidence, remaining work, blockers/dependencies and next human owner. Use the PR template. GitHub/agent authentication belongs to each contributor locally; never commit tokens.

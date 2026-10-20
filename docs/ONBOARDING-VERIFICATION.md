# Historical Windows onboarding evidence — superseded bootstrap path

The evidence below describes the earlier PowerShell bootstrap implementation through `353d2d5a26488c4f5760c284c7f23fd458680fef`. That root bootstrap and custom package launcher were removed by the direct npm scope correction. Commands below are retained as history, not current onboarding instructions or proof of the corrected path. Current contributor commands are in README.md; corrected-path results are recorded separately above this history when available.

Implementation owner: mirkoEscobedo. Assistant: Codex. Branch: `task/1-windows-onboarding`, targeting existing `master`. Implementation tested at `d21d0ff` (full commit in Git history); later documentation-only changes record this evidence. No other human editor or sprite asset editor is active in this task. Dependencies: approved retained archive; separately installed Windows prerequisites and first-use Python package downloads. Acceptance criteria remain in [issue #1](https://github.com/mirkoEscobedo/CitizensSector/issues/1).

## Environment and exact clean-clone procedure

Tested 2026-10-20 on Windows 10 x64 (10.0.19045), Windows PowerShell 5.1, Node 24.11.0, npm 11.7.0 and Python 3.13.15. Python requirement is 3.12+; not every supported interpreter was tested.

From the implementation checkout, with no copied `node_modules`, `.venv`, npm cache, provider result or generated candidates:

```powershell
git clone --no-local --branch task/1-windows-onboarding . '.onboarding-cache/Fresh Windows clone'
# The first test exposed PowerShell 5.1 native-argument quote stripping.
# After committing the probe correction, fast-forward the still-uninitialized clone:
git -C '.onboarding-cache/Fresh Windows clone' pull --ff-only
$env:npm_config_registry = 'http://127.0.0.1:9'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File '.onboarding-cache/Fresh Windows clone/scripts/setup.ps1'
Set-Location '.onboarding-cache/Fresh Windows clone'
$env:STARSECTOR_HOME = Join-Path $PWD 'no-game-installed'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
git diff --exit-code
git status --short --untracked-files=no
npm.cmd run workspace-template -- verify . --scope all
npm.cmd run workspace-template -- update status .
Get-Content ship-sprite-lab/.venv/pyvenv.cfg
```

Both setup runs passed. Empty local npm cache + unreachable registry + `--offline` installed exactly one archive dependency. Python independently downloaded its build/dependency packages and installed Pillow 12.3.0, NumPy 2.3.5 and editable ship-sprite-lab 0.1.0 inside the clone's venv. `include-system-site-packages = false`; the executable/module paths point inside the clone with spaces. The second setup passed with an absent game path, and tracked-file status/diff stayed empty. The first doctor discovered the host's existing game and copied native references only into ignored output/private directories; neither run launched a game or image provider.

The initial PowerShell 5.1 setup failure was a real compatibility finding: embedded double quotes were stripped from native `node -p`/Python probes. Probes now use quote-free arguments. A sandboxed attempt to reuse the pre-existing maintainer venv also exposed its shared bundled runtime; setup now rejects that legacy environment with an actionable message and preserves it. Fresh-clone setup uses normal isolated venv creation.

## Results

| Check | Observed result |
| --- | --- |
| Archive + installed executable hashes | Match the approved identities in vendor/README.md and lockfile |
| Package `version` | 0.9.0-alpha.0, source/release `9b76e0312d83ff30538f97b6ceb05432580799e2` |
| Package `doctor` | PASS, 46 embedded assets verified, no errors |
| Package `skills list` | 13 embedded skills |
| Package `inspect` | One valid `citizens-sector` module, no conflicts; only `cmd.exe /d /c npm.cmd run check` configured |
| `npm.cmd run check` | Seven software/data gates pass, largest transform round-trip error 5.773159728050814e-15 px |
| Package `verify . --scope all` | PASS, CitizensSector check exited 0 under Windows Job Object ownership |
| Second setup | PASS, tracked files unchanged |
| Optional `update status` | INCOMPLETE: alpha reports `manifest.exact=false` for the required local `file:` dependency; installed version/binary and all project identity matches are true |
| `git diff --check` and ignore checks | PASS; outputs, private references, node_modules and onboarding cache stay ignored |

Concrete failure-path checks ran in the disposable clone, restoring inputs in `finally` blocks: temporarily hiding the local executable caused the guarded command to fail with setup instructions; hiding the canonical mask made `npm run check` fail nonzero; appending bytes to a disposable archive made setup reject its hash before installation. After restoration, `npm run check` and `git diff --exit-code` passed. No permanent test fixtures were added for these reversible setup probes.

The new public `sprite_lab check` seam was first run before implementation and failed as an unknown CLI command, then passed after extracting the existing software gates. Existing `meaningful_tests()` still enforces the no-doubled-turrets export rule. Regression command `npm.cmd run lab -- validate --ship idris` passed against the maintainer's already-present private outputs: structural passes A01/A04/A07 and all seven original checks, including the export gate. No source art or interface geometry changed.

## Agent loading and unavailable evidence

- Root `AGENTS.md` was generated by the installed tool's sealed `adopt plan/apply`, then explicitly read in this Codex session. Its managed block is retained; project checks/ownership guidance follow it. Since the file was created during this session, automatic discovery in a fresh Codex session was **not tested**. Installed CLI version was checked: codex-cli 0.154.0.
- `CLAUDE.md` was checked as a regular tracked file (Git mode 100644), containing the literal `@AGENTS.md` import outside fences. Claude Code was not installed on PATH, so **no actual Claude session or `/context` test ran**.
- A friend's physical-machine first use remains a handoff step: start a fresh agent from the clone root, confirm loaded instructions (Claude `/context`), then run setup/checks with their own accounts. Do not treat this pending check as an implementation blocker.
- Clean clones lack the private cached M4 response, generated candidates and exported hull. Full art replay/validation there is unavailable until the human owner supplies authorized inputs. The local regression run is separate evidence, not proof of a clean-clone visual result. No new visual quality review, Blender/M2/M3 run or in-game smoke test was performed; no game readiness is claimed.
- Runtime debugger providers are optional and unavailable/unqualified in package doctor output; no debugger qualification is claimed.

## Handoff

Completed: retained package/provenance, local reproducible npm setup, isolated Python setup, software-check entry point, package-managed adoption, shared instructions/import, ownership/review/handoff templates and documentation. Changed interfaces: root setup/npm commands and `sprite_lab check`; changed sprite assets: none. Remaining work: human PR review/merge and friend's first-use loading check, followed by separately scoped art/game work. Next human owner: mirkoEscobedo to review/coordinate the friend's assigned issue and exclusive asset ownership. No implementation dependency remains unresolved.

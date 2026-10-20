# Windows onboarding evidence — issue #1

## Current path: direct npm, Python lab separate

Corrected implementation tested at **`f95d19847cc12d8c92dc5d81552d6d6b6a018496`** on `task/1-windows-onboarding`, continuing PR #2 to `master`. Subsequent documentation-only changes record these results and the standard npm shim behavior. Human owner: mirkoEscobedo; assistant: Codex. No source art, package build, lockfile, provenance, adoption state or Claude import changed in this correction.

Tested 2026-10-20 on Windows 10 x64 (10.0.19045), Node 24.11.0 and npm 11.7.0. The lab phase separately used Windows PowerShell 5.1 and Python 3.13.15.

### Fresh clone and tooling before Python

Created a new clone from the corrected commit, without existing `node_modules`, npm cache, lab `.venv`, generated candidates or provider result:

```powershell
git clone --no-local --branch task/1-windows-onboarding . '.onboarding-cache/Direct npm Windows clone'
Set-Location '.onboarding-cache/Direct npm Windows clone'
$onboardingPath = $env:PATH
$onboardingNodeDirectory = Split-Path (Get-Command node.exe).Source -Parent
$env:PATH = "$onboardingNodeDirectory;$env:SystemRoot\System32;$env:SystemRoot;$env:SystemRoot\System32\Wbem"
$env:npm_config_registry = 'http://127.0.0.1:9'
$env:npm_config_cache = Join-Path $PWD '.onboarding-cache/empty-npm-cache'
Get-Command python,python3,py -ErrorAction SilentlyContinue
Test-Path ship-sprite-lab/.venv
```

Python commands were absent, `.venv` was absent, and the npm cache initially did not exist. Plain `npm ci` installed one retained package offline from that empty cache. The full direct command sequence was then run through Command Prompt's standard npm entry point from this clone (using `cmd.exe /d /c` for each command from the PowerShell test harness):

```bat
npm ci
npm run skills
npm run workspace-template -- skills show tdd
npm run workspace-template -- version --json
npm run doctor
npm run workspace-template -- skills show citizens-sector-nonexistent
npm run workspace-template -- version --unsupported
npm ci
```

The successful commands returned 0. The missing skill returned **66 / SKILL_NOT_FOUND**; the unsupported option reached the executable and returned **64 / INVALID_ARGUMENT**. These expected failures verify both argument forwarding and npm's propagation of tool exit status. No custom launcher ran. npm's generated `.bin/workspace-template` shims remained installed normally. Python stayed absent from PATH and no lab venv was created during this phase. After restoring PATH, `git diff --exit-code` passed and `git status --porcelain` was empty, including after repeated installation.

One concrete host-shim finding: this machine's installed `npm.ps1` consumes the bare `--` separator, dropping `--json` or treating `--unsupported` as npm configuration. Command Prompt's `npm` and PowerShell's standard `npm.cmd` preserve the arguments. README now documents Command Prompt commands and the `npm.cmd` spelling for PowerShell. The repository does not add a replacement launcher or modify npm's shims.

| Check | Actual corrected-path result |
| --- | --- |
| Archive SHA-256 | `95c61b973fd68204289f257fae957589a921d4ff4331f552c11b72015d1d38f5` |
| Installed executable SHA-256 | `00e272fdf9a406fc15619c1c7fecec36c39ebea04a184c5d9f725a3ce83213d0` |
| Version / package / source and release | `0.9.0-alpha.0`, `workspace-template-win32-x64`, commit `9b76e0312d83ff30538f97b6ceb05432580799e2` |
| `skills` / `skills show tdd` | 13 embedded skills / correct embedded TDD content |
| `version --json` | Argument visible in npm's invoked command; successful JSON identity envelope |
| `doctor` without Python | PASS, 46 embedded assets verified, no errors |
| Repeated `npm ci` | PASS; tracked files unchanged, no Python initialization |
| Failure status | Missing skill 66, unsupported option 64, both propagated through direct npm |

### Separate lab phase

Only after all tooling checks, restored the original PATH and ran the documented lab setup and existing checks from the same clone:

```powershell
$env:PATH = $onboardingPath
$env:STARSECTOR_HOME = Join-Path $PWD '.onboarding-cache/no-game-installed'
# Before lab setup, this failed nonzero with the correct separate setup command:
npm.cmd run check
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ship-sprite-lab\scripts\setup.ps1
npm.cmd run lab -- doctor
npm.cmd run check
npm.cmd run workspace-template -- verify . --scope all
git diff --exit-code
git status --porcelain
```

Lab setup, pip dependency validation, doctor and all seven existing software/data gates passed. Largest transform round-trip error: 5.773159728050814e-15 px. Packaged verification passed `cmd.exe /d /c npm.cmd run check` under Windows Job Object ownership. The clone's venv uses Python 3.13.15 with `include-system-site-packages = false`, Pillow 12.3.0 and NumPy 2.3.5. This run used cached Python wheels plus build backend resolution; a first lab install requires separate setuptools/Pillow/NumPy downloads. Tracked diff/status remained empty. No image provider or game launch occurred.

No new agent-loading session, visual art review, Blender render or in-game test was performed for this invocation-only correction. The earlier local art-regression and agent-file checks below remain historical evidence. Fresh-clone art replay still requires authorized private outputs; the friend's physical-machine agent-loading check remains a handoff step. The retained alpha's previously recorded optional `update status` limitation is unchanged; it was not rerun for this correction.

Completed correction: direct npm entries, removal of the root bootstrap/custom package launcher, consistent onboarding instructions, separate lab setup, corrected lab-helper error and revised verification evidence. Next human owner: mirkoEscobedo for PR review/merge and the friend's first-use check. No shared sprite assets or ownership changed.

## Historical evidence — superseded bootstrap path

The evidence below describes the earlier PowerShell bootstrap implementation through `353d2d5a26488c4f5760c284c7f23fd458680fef`. That root bootstrap and custom package launcher were removed by the direct npm scope correction. Commands below are retained as history, not current onboarding instructions or proof of the corrected path. Current contributor commands are in README.md; corrected-path results are recorded above.

Implementation owner: mirkoEscobedo. Assistant: Codex. Branch: `task/1-windows-onboarding`, targeting existing `master`. Implementation tested at `d21d0ff` (full commit in Git history); later documentation-only changes record this evidence. No other human editor or sprite asset editor is active in this task. Dependencies: approved retained archive; separately installed Windows prerequisites and first-use Python package downloads. Acceptance criteria remain in [issue #1](https://github.com/mirkoEscobedo/CitizensSector/issues/1).

### Historical environment and exact clean-clone procedure

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

### Historical results

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

### Historical agent loading and unavailable evidence

- Root `AGENTS.md` was generated by the installed tool's sealed `adopt plan/apply`, then explicitly read in this Codex session. Its managed block is retained; project checks/ownership guidance follow it. Since the file was created during this session, automatic discovery in a fresh Codex session was **not tested**. Installed CLI version was checked: codex-cli 0.154.0.
- `CLAUDE.md` was checked as a regular tracked file (Git mode 100644), containing the literal `@AGENTS.md` import outside fences. Claude Code was not installed on PATH, so **no actual Claude session or `/context` test ran**.
- A friend's physical-machine first use remains a handoff step: start a fresh agent from the clone root, confirm loaded instructions (Claude `/context`), then run setup/checks with their own accounts. Do not treat this pending check as an implementation blocker.
- Clean clones lack the private cached M4 response, generated candidates and exported hull. Full art replay/validation there is unavailable until the human owner supplies authorized inputs. The local regression run is separate evidence, not proof of a clean-clone visual result. No new visual quality review, Blender/M2/M3 run or in-game smoke test was performed; no game readiness is claimed.
- Runtime debugger providers are optional and unavailable/unqualified in package doctor output; no debugger qualification is claimed.

### Historical handoff

Completed: retained package/provenance, local reproducible npm setup, isolated Python setup, software-check entry point, package-managed adoption, shared instructions/import, ownership/review/handoff templates and documentation. Changed interfaces: root setup/npm commands and `sprite_lab check`; changed sprite assets: none. Remaining work: human PR review/merge and friend's first-use loading check, followed by separately scoped art/game work. Next human owner: mirkoEscobedo to review/coordinate the friend's assigned issue and exclusive asset ownership. No implementation dependency remains unresolved.

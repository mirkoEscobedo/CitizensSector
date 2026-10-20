# CitizensSector

Private Windows ship-sprite experiments and a shared Codex/Claude workflow. The lab and original inputs remain in [ship-sprite-lab](ship-sprite-lab/README.md). Tooling provenance is in [vendor/README.md](vendor/README.md).

## Clone and install tooling

Install Git for Windows, GitHub CLI (`gh`) and **Windows x64 Node.js 24 LTS with npm** on PATH. Tooling installation, doctor and skills do not need Python, a lab virtual environment, private images or the game. Install and authenticate your chosen Codex or Claude Code client separately. Each contributor needs their own GitHub account with repository access; agent subscriptions/login and GitHub authorization are separate.

Run in Command Prompt, under any parent directory (spaces are supported):

```bat
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
gh auth status
git clone https://github.com/mirkoEscobedo/CitizensSector.git
cd CitizensSector
npm ci
npm run skills
npm run workspace-template -- skills show tdd
npm run workspace-template -- version --json
npm run doctor
```

Before this PR is merged, add `--branch task/1-windows-onboarding` to `git clone`. After merge, the default branch remains `master`.

`npm ci` installs the exact retained archive from the committed manifest and lockfile. `.npmrc` keeps npm offline and disables install scripts; no registry, sibling checkout, source build or package publication is needed. Repeating installation leaves tracked files unchanged. Contributors do **not** run `npm init` against this already-configured repository. In PowerShell, use `npm.cmd` for the same npm commands: this avoids execution-policy restrictions and preserves `--` argument forwarding when an installed `npm.ps1` shim consumes it.

The scripts call the installed package directly using npm's normal executable shims. The managed `npm exec -- workspace-template ...` instructions also work after installation. Installation consumes the committed managed blocks and `.agentic/project.json`; it does not re-adopt on each clone. Exact archive/executable hashes and measured integrity checks remain in [vendor/README.md](vendor/README.md) and [the verification record](docs/ONBOARDING-VERIFICATION.md).

## Set up the Python lab separately

For lab tasks, install **Python 3.12+ with pip/venv** on PATH. From the repository root, using Windows PowerShell 5.1 or later:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ship-sprite-lab\scripts\setup.ps1
npm.cmd run lab -- doctor
npm.cmd run check
```

The lab setup creates an isolated `ship-sprite-lab/.venv`, installs the lab and runs its doctor. The first Python install **does need separate PyPI/package downloads**: setuptools>=68 (build backend), Pillow==12.3.0 and numpy==2.3.5. Subsequent lab setup can still contact PyPI for build dependencies. Python offline installation requires a separately prepared compatible wheelhouse; the npm offline guarantee does not cover Python.

If `python` is unavailable or selects the wrong interpreter, append `-Python 'C:\path with spaces\Python312\python.exe'`. A failed dependency install can be repaired by rerunning setup. An old shared-runtime lab `.venv` is preserved and rejected: move it aside before setup (do not reuse its machine-specific bundled Python). All new dependencies stay local; activation is optional.

## Checks and art inputs

Run commands from the repository root:

| Command | Purpose |
| --- | --- |
| `npm run skills` | Installed methodology inventory; tooling only |
| `npm run workspace-template -- skills show tdd` | Read the installed TDD skill; tooling only |
| `npm run workspace-template -- version --json` | Installed tool identity; tooling only |
| `npm run doctor` | Packaged workspace health; tooling only |
| `npm run check` | After lab setup: seven math/image/data checks, independent of private outputs and game |
| `npm run workspace-template -- verify . --scope all` | After lab setup: run CitizensSector's configured check under the packaged process supervisor |
| `npm run lab -- doctor` | After lab setup: Python dependencies and optional local capabilities |
| `npm run lab -- validate --ship idris` | After lab setup: art gates and export checks; requires generated candidates/raw input/export |

In this retained alpha, optional `update status` returns `INCOMPLETE` because it reports the approved `file:` dependency as `manifest.exact=false`. Its installed binary, lock version/integrity presence and project provenance fields match. See the recorded hash checks and `doctor` for identity evidence; do not switch to a registry dependency to silence this status.

Onboarding needs no private game art, model, generated provider response, Blender or API key and makes no image-provider calls or game launches. Supplied reference PNGs are already tracked in `ship-sprite-lab/docs/references`; their presence does not grant redistribution rights. Full `run --methods available` needs the authorized cached provider PNG at `ship-sprite-lab/outputs/idris/raw/M4-attempt-01.png` (not in Git). Obtain that exact original and provenance from the human owner; do not substitute an image or invoke a provider during setup. `compare`/`validate` require candidate outputs; export validation also needs `outputs/idris/export/idris_lab/data/hulls/idris_lab.ship`. Missing outputs are actionable prerequisites, not a software-check failure.

For native-reference discovery, set `$env:STARSECTOR_HOME = 'C:\your game path\Starsector'` in your own session. Export currently reads `game_install` in `ship-sprite-lab/experiment.json` separately; review that local setting before an explicit export. Never commit another contributor's absolute game path. Native assets stay in ignored `reference-private/`; generated outputs stay in ignored `outputs/`. Read the lab README and [manual game smoke test](ship-sprite-lab/docs/SMOKE_TEST.md) before any explicit game run. M2/M3 additionally need an authorized genuine mesh/Blender; onboarding does not acquire them.

## Start an agent and first task

Start a **new session at the repository root** with `codex` or `claude`. Shared rules live in root `AGENTS.md`; regular root `CLAUDE.md` contains the literal `@AGENTS.md` import, with no Windows symlink.

- Codex: ask “Which instruction files are active, and what CitizensSector checks and asset ownership rules apply?” Confirm the root `AGENTS.md` rules are reported. [Official instruction discovery/verification guidance](https://developers.openai.com/codex/guides/agents-md).
- Claude Code: inspect `/context` to confirm `CLAUDE.md` and imported `AGENTS.md` are loaded; ask the same question. [Official import guidance](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).
- Actual loading checks and clean-clone evidence are recorded in [docs/ONBOARDING-VERIFICATION.md](docs/ONBOARDING-VERIFICATION.md). A file/import check alone is not an actual Claude session test. The friend's physical-machine first use remains a handoff check.

After this onboarding PR merges, choose a scoped issue for the first implementation task. Have the maintainer assign exactly one human owner (self-assign requires repository permission). Record assistant, branch/current commit, dependencies and acceptance criteria using the issue template before implementation. Small reversible edits remain Direct; multi-session work is issue-scoped.

```powershell
git switch master
git pull --ff-only origin master
gh issue list --state open
$issue = Read-Host 'Assigned implementation issue number'
$slug = Read-Host 'Short branch slug (lowercase words with hyphens)'
gh issue view $issue
gh issue edit $issue --add-assignee '@me'
$branch = "task/$issue-$slug"
git switch -c $branch
git rev-parse HEAD
codex
# Or run: claude
# For lab work, run the separate lab setup above before checking:
npm.cmd run check
git diff --check
git status --short
git add --interactive
git commit -m "Describe the completed task"
git push -u origin $branch
gh pr create --base master --fill
```

Fill the PR template and include `Closes #<issue-number>` only when its scope is complete. Request the other contributor's review. Before editing a shared sprite, explicitly agree on one active editor; comments are not an atomic lock. Hand off with completed work, exact commit, changed assets/interfaces, checks/visual evidence, remaining work, blockers and next human owner. Keep credentials out of instructions and commits.

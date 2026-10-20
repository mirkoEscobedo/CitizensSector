# Issue #3 — contributor intake, first import and integration plan

Issue: [#3](https://github.com/mirkoEscobedo/CitizensSector/issues/3). Branch `task/3-collaborator-intake`, base `master` @ `bc26b4b479f83e683a70c2d37f110be903020175` (PR #2 merge). Assistant: Claude (Sonnet 5.5) on the contributor's Windows 11 machine. Human owner of this issue: unassigned in GitHub when work started; the maintainer was granting the contributor repository access.

Everything below is a **candidate-level intake**. No new generation, training, sprite correction, animation or game launch was done. Nothing here has been reviewed by a maintainer or loaded into Starsector by this task.

## 1. Source and workspace mapping

Public records use neutral labels; the local mapping is kept outside the repository.

| Label | What it is | Treatment |
| --- | --- | --- |
| `source:mod` | The contributor's Starsector mod `mfz` (26 files; 6 ship PNGs, 3 hulls, 3 variants, `ship_data.csv`, descriptions, style configs, a test mission, an IDE folder). Not a Git repository, no remotes. | Read only. File hashes were taken before and after the task and compared (section 7). |
| `source:staging` | The contributor's ComfyUI staging folder: generation manifests, intermediate PNGs, small helper scripts, slot JSON. Raw batches for Polaris/Perseus/Idris rounds were already deleted by the contributor. | Read only (authorised by the contributor). |
| `source:sprite-gen-skill` | The contributor's local sprite-generation skill: the two ComfyUI API workflow JSONs actually used. | Read only. Only the workflows were taken. |
| `source:session-scripts` | Three small scripts the contributor's earlier sessions wrote while finishing the Rha. | Read only; copied with machine paths neutralised. |
| `workspace` | A new separate checkout of the repository beside the mod folder. | All writes happen here. |

The mod folder was not turned into a checkout, no remote was changed, nothing was cleaned or reset.

## 2. Windows onboarding (run on this machine, 2026-10-20)

Prerequisites found: Git 2.55.0, Node v24.18.0 (win32 x64), npm 11.16.0, Claude Code 2.1.303, GitHub CLI logged in as the contributor's own account. **Python was missing** and was installed for the current user with `winget install --id Python.Python.3.12 --scope user` (3.12.10). The contributor's ComfyUI Python environment was not touched.

| Command (PowerShell, `npm.cmd`) | Result |
| --- | --- |
| `npm.cmd ci` | exit 0, 1 package added, no tracked-file change |
| `npm.cmd run skills` | exit 0, 13 skills |
| `npm.cmd run workspace-template -- skills show tdd` | exit 0, TDD skill content (v2.0.0) |
| `npm.cmd run workspace-template -- version --json` | exit 0, `0.9.0-alpha.0`, source commit `9b76e0312d83ff30538f97b6ceb05432580799e2` |
| `npm.cmd run doctor` | exit 0, verdict PASS, 46 embedded assets verified, no errors (debug providers `cdb` etc. reported missing, as expected and irrelevant) |
| `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ship-sprite-lab\scripts\setup.ps1` | exit 0; isolated `ship-sprite-lab/.venv`, Python 3.12.10, Pillow 12.3.0, numpy 2.3.5 |
| `npm.cmd run lab -- doctor` | exit 0 |
| `npm.cmd run check` | exit 0, 7/7 software/data checks |

Separately from those software checks, these are **unavailable on this machine** and were not attempted: Blender (M2/M3 arms), the cached provider PNG `ship-sprite-lab/outputs/idris/raw/M4-attempt-01.png`, `npm run lab -- validate --ship idris` (needs candidate outputs and export), and any game smoke test. `ship-sprite-lab/experiment.json` still names another contributor's game path (`game_install`); it was left unchanged and not used.

**Claude instruction loading.** From the repository root, `claude -p "/context"` (Claude Code 2.1.303, a real, headless session started at the root) listed under *Memory files*: `E:\CitizensSector\CLAUDE.md` (16 tokens) and `E:\CitizensSector\AGENTS.md` (1.5k tokens), i.e. the file and its `@AGENTS.md` import were both loaded. This was a headless (`-p`) session, not an interactive one; an interactive `/context` was not run. The session that executed this task started outside the repository and is not evidence of loading.

## 3. Inventory of the existing work

### Ships

All sprites are RGBA PNG, bow up. Hashes are in the import manifest (Rha) or in the table (others).

| Hull id | Dimensions | Hull data | Role / status | Provenance known | Imported |
| --- | --- | --- | --- | --- | --- |
| `mfz_rha` ("Rha", Wing of Ra) | 136×246 | `.ship` (DESTROYER, 4 turrets/hangar slots, 4 engines), variant, csv row, description | Anthracite/gold light carrier. **Selected candidate**, final of a 3-round lineage (text-only → mirrored img2img → hand finishing). Matches staging `raB_armed.png` byte for byte. | Full: prompts, seeds, sizes, workflows, models; own design (Egyptian theme, no franchise source). | **Yes** |
| `mfz_idris` | 175×280 | `.ship` (CRUISER, 6 turrets, 2 bays, 4 engines), variant | The contributor's dark re-interpretation of the repo's tracked `mfz_idris_hand_made_by_bro.png` (the original light sprite, hash `4b70623d…`, is byte-identical to that tracked reference). Mod sprite = backup "dark before upscale". **Overlaps with existing Idris work**: not imported, needs owner agreement. | Partial: workflows and seeds in notes; raw rounds deleted. Star Citizen-derived design; the reference renders are external material. | No |
| `mfz_polaris` | 176×339 | none (sprite only) | RSI Polaris cruiser from a user pixel-art reference. The contributor's notes call it the quality benchmark and say it works in game; no in-game evidence was inspected here. | Seeds/recipes only in notes (e.g. seed 2281004658 left half, denoise 0.55); raw rounds deleted; the pixel reference is external material. | No |
| `mfz_perseus` | 128×254 | none | RSI Perseus destroyer, 8 mounts stamped from vanilla sockets. Matches staging `perseus_g/armed_128_aligned.png`. | Round-by-round notes and ~15 helper scripts/slot JSONs in staging; raw gens deleted; vanilla-socket pixels and external reference. | No |
| `mfz_crestshield` | 288×384 | `.ship` CAPITAL, 16 slots, 6 engines; description text is the vanilla Onslaught text | Placeholder-looking capital; not an exact vanilla file but size and text match the vanilla Onslaught. | **Unknown.** No generation record, source or authorship. | No — unresolved |
| `mfz_lance` | 204×328 | none | Unknown purpose. | **Unknown.** | No — unresolved |

Also in the mod: `mfz_test` mission (Rha added, Idris removed from player fleet), `descriptions.csv`, `engine_styles.json`, `hull_styles.json`. `mod_info.json` contains the contributor's author handle and was not imported. `.idea/` is IDE state and was not imported.

### Editable masters, layers, masks

There are **no layered projects, masks, material regions, geometry annotations, pivots or component layers** in the source folder or staging. The only "editable" forms are the flattened game sprites, the intermediate PNGs, the slot JSON files and the `.ship` bounds. Nothing was lost by flattening; nothing exists to preserve. The Rha's hangar dimming and socket stamping are procedural (`finish_b.py`), so they are reproducible from `raR_4302.png`.

### Generation stack and workflow

See [generation-environment.json](../../ship-sprite-lab/assets/mfz/generation-environment.json): ComfyUI 0.42.1, ComfyUI-GGUF commit `6ea2651…`, Flux.2 Klein 9B Q6_K GGUF, Qwen3-8B text encoder, `flux2-vae`, and the **`starsector-x4-klein` LoRA** (ai-toolkit 0.9.5, step 30000; file SHA-256 `b9afd4f6…`). Workflows are text-to-image (default 4 steps, 704×1120) and image-to-image (8 steps, denoise 0.6). Weights are not in the repository; acquisition sources are **unknown** and must be supplied by the contributor.

Known gaps recorded as unknown, not invented: LoRA strength and some step counts are `null` in manifests; denoise/steps for round 2 exist only in notes; the image-guided mode ignored seed/strength before 2026-10-20 afternoon (affects Idris rounds, not the Rha rounds).

### Iteration and selection notes (Rha)

1. Round 1, text-only, 576×1088, seeds 1588384319–22; seed …320 selected (compact, clear hangars).
2. Round 2, `--init-image` = mirrored …320, denoise 0.52, 16 steps, seeds 4300–03; seed 4302 ("B") selected for hieroglyph-engraved wings.
3. Finish: hangars dimmed (hue-keeping, sat×0.70, gain×0.66), four 10 px **vanilla Hammerhead socket** stamps added; `.ship` written by `make_ship.py` from the alpha.
4. `ra_r1` (seeds 4200–03) was not selected; only its manifest is kept.

### Visual observations (Rha) — from the imported preview, not game evidence

`previews/rha_ship_overlay.png` (derived by the contributor's session) shows the hull bounds, six slots and four engine flames over the sprite. Observed: silhouette is left–right symmetric (alpha asymmetry 0 px); bounds follow the body but cut across the outer wing tips; slots 1–2 sit on the wing shoulders and 3–4 on the stern pods as intended; hangar markers 5–6 sit on the dark panel areas. Not checked: shield, legibility at 50/25 %, in-game scale against vanilla.

### Known defects and inconsistencies

- Rha socket **type conflict**: `stamped_sockets.json` records two stamped BALLISTIC and two MISSILE sockets, while `mfz_rha.ship` declares WS0001–2 as **ENERGY**. Art and data disagree.
- Rha slot angles/arcs, stats, shield radius and engine positions were guessed by the earlier session; never loaded in Starsector.
- Variant `mfz_rha_standard` is intentionally empty (no weapons, no wings).
- Rha bounds are shrunk 2 px and end at wing tips with spikes; collision shape unverified.
- The `ship_data.csv` rows for Idris/Rha were written by hand; stat balance untested.
- Polaris and Perseus have sprites but no `.ship`, variant or csv rows in the mod.

## 4. Sharing and licensing items (flagged, not decided)

1. **Vanilla pixels in the Rha.** Four small socket stamps were cut from a vanilla Hammerhead sprite (Fractal Softworks art). They are ~10 px each but are in the imported PNG. The maintainer should decide whether to keep, redraw or replace them. They are also present in Perseus (8 stamps) and in Perseus/Odin notes (vanilla Odyssey sockets).
2. **Star Citizen-derived designs** (Idris, Polaris, Perseus, Odin): the references and shapes come from Cloud Imperium material; the repository already says reference presence "does not grant redistribution rights". These were **not imported**.
3. **Crestshield / Lance**: authorship and origin unknown; not imported.
4. **Model weights**: not imported by design; LoRA/base model license terms are not recorded and should be confirmed by the contributor.

## 5. What was imported and why

`ship-sprite-lab/assets/mfz/rha/` (22 files, ~1.6 MB) + `ship-sprite-lab/assets/mfz/generation-environment.json`. This is the smallest slice that is (a) the contributor's own design, (b) complete from prompt to finished sprite to game data, and (c) clear of Star Citizen material and of other people's active Idris work. Nothing under `ship-sprite-lab/assets/idris/` was changed. All imported files are tracked (none match an ignore rule).

```
assets/mfz/generation-environment.json   models, hashes, versions, reproducibility gaps
assets/mfz/rha/manifest.json             source→destination map, both hashes, transformations
assets/mfz/rha/sprite/                   mfz_rha.png (candidate)
assets/mfz/rha/game-data/                .ship, .variant, csv rows, style configs
assets/mfz/rha/generation/               manifests, selected raw + intermediate PNGs, stamp positions
assets/mfz/rha/workflows/                the two ComfyUI API workflows
assets/mfz/rha/scripts/                  mirror.py, finish_b.py, make_ship.py (documentation of method)
assets/mfz/rha/previews/                 two derived previews from the contributor's session
```

Transformations (each recorded in the manifest with both hashes): manifests' image paths reduced to file names; CSV rows extracted for Rha only; the three scripts had machine paths replaced by `<STAGING_DIR>`, `<MOD_DIR>`, `<STARSECTOR_HOME>` — they document the method and are **not runnable as-is**. The `.ship` and `stamped_sockets.json` have CRLF line endings normalised to LF; `hull_styles.json` has trailing tabs removed from two blank lines. The sprite, `.variant`, engine style config, workflows and raw/intermediate PNGs are byte-identical to the sources.

Destination hashes and byte counts describe the committed files (LF for text); source hashes retain the original source bytes. On Windows with `core.autocrlf` a working copy may show CRLF and a different file hash.

Status stays **candidate**. Nothing in this intake claims correct hardpoints, art quality or game readiness.

## 6. Articulation requirements (captured, not implemented)

The issue describes Idris/Odin requirements: front hangar gates, vertical thruster motion, covered/retractable hardpoints. **No supplied articulation reference, diagram or spec was found** in the source folder, staging, the contributor's notes or the repository. The only related source facts are: the mod's Idris `.ship` has two HIDDEN launch-bay slots and four fixed engine slots; the Odin notes list real-ship weapon counts only. The requirements below therefore come from the issue text, and the human owners should attach their references to the follow-up issue.

- Hangar gates: separately drawn door components with open/closed states and a pivot per door.
- Thrusters: movable pods or nozzles (vertical tilt) as separate components with defined pivots and travel limits.
- Hardpoints: covered mounts with a retracted and an extended state, at least cover + base layers.
- Geometry correction and a component/pivot contract must precede animation and game integration.

## 7. Verification on this machine

| Check | Result |
| --- | --- |
| `git diff --check` | exit 0 |
| `git check-ignore` over `assets/mfz` | no file ignored |
| Source folder unchanged | `sha256` of all 26 files recorded before and after; identical |
| Imported file hashes | all 22 manifest entries re-hashed: 0 mismatches |
| `npm.cmd run check` | 7/7 pass (software/data only) |
| Art/game evidence | **unavailable**: no `lab validate`, no Starsector load, no 100/50/25 % review of the actual sprite |

Prior contributors' verification (README, `docs/ONBOARDING-VERIFICATION.md`) was not reused as evidence for any item above.

### PR #7 review correction (Codex, 2026-10-20)

Review of intake commit `e95fd85e94901b02f827c9a9ac28fade6f467c3b` found two destination hashes/byte counts still describing CRLF source bytes and two trailing-whitespace errors in `hull_styles.json`. This supersedes the corresponding clean-diff and zero-mismatch claims above for that commit. The correction retains every source hash, records newline normalisation for the hull and socket metadata, removes the two whitespace errors, and updates the hull-style destination hash/byte count for that cleanup.

Verification on the maintainer's checkout: all 22 manifest destinations match the staged Git blobs in both SHA-256 and byte count; the full PR diff passes `git diff --cached --check bc26b4b479f83e683a70c2d37f110be903020175`; `npm.cmd run check` passes 7/7; `npm.cmd run workspace-template -- verify . --scope all` returns PASS. These checks cover the metadata correction and software gates; source-folder preservation, contributor onboarding and art/game readiness were not re-tested by this correction.

## 8. Ordered follow-up plan

Owners are left unassigned unless the person is known. Each item lists dependencies and acceptance criteria.

| # | Task | Depends on | Acceptance |
| --- | --- | --- | --- |
| A | **Rha game load and data fix** — [#4](https://github.com/mirkoEscobedo/CitizensSector/issues/4) | this PR merged | Rha loads in Starsector without errors; slot types agree between sprite and `.ship` (decision: ENERGY vs BALLISTIC recorded); bounds checked against the silhouette at wing tips; 100/50/25 % review recorded. Hull in-mod stays owned by the contributor. |
| B | **Provenance and sharing decision** — [#5](https://github.com/mirkoEscobedo/CitizensSector/issues/5) | none | Decision recorded for the vanilla socket pixels in Rha and for Star Citizen–derived Idris/Polaris/Perseus: keep, redraw or exclude. Source/authorship recorded or "unknown" confirmed for Crestshield and Lance. LoRA/base-model licence and download sources recorded in `generation-environment.json`. |
| C | **Idris geometry correction and component/pivot contract** — [#6](https://github.com/mirkoEscobedo/CitizensSector/issues/6) | B, agreement on one active editor with the Idris owner | The overlap between the contributor's dark Idris and the canonical Idris inputs is resolved without overwriting; a written component list (hull, hangar gates, thruster pods, retractable hardpoint covers) with pivots/limits and the supplied references attached. |
| D | **Animation / game integration for articulated parts** | C | Separate task; not scoped here. |
| E | **Import Polaris/Perseus candidates** | B | After B allows it: same manifest style as Rha; includes Perseus helper scripts/slot JSON. Raw rounds are gone, so lineage is partial and stays labelled so. |

Follow-ups A–C are separate issues (#4, #5, #6), all unassigned. D and E stay in this table until their dependencies resolve, to avoid duplicating a future faction backlog.

## 9. Handoff

- Completed work: Windows setup verified; inventory and plan (this file); Rha candidate imported with manifest and generation record; follow-up issues A–C.
- Changed assets/interfaces: new files under `ship-sprite-lab/assets/mfz/` and `docs/collaboration/` only.
- Remaining: items A–E above; maintainer review; decisions in section 4.
- Blockers: interactive `/context` check not run; Blender/private outputs/game unavailable; sharing decisions in section 4.
- Next human owner: maintainer (review); contributor for A.

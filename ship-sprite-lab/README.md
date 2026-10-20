# Ship sprite lab

A working, private Idris art experiment. Start with [the actual result](docs/RESULTS.md) or [the visual comparison](outputs/idris/report.html). Recommended image-only route: **A04 / M0 masked finish**. M1 is partial; M2/M3 are blocked; fresh M4 is attractive but fails geometry/alpha gates; M5 adds little over M0. No candidate has passed an in-game load test. Fleet generalization is untested.

Everything created by this experiment stays in this folder, apart from the image tool's default original save, which was copied into the lab. No NearFuture backlog, production mod or normal game configuration was edited.

## Windows PowerShell

```powershell
Set-Location .\ship-sprite-lab # from your CitizensSector clone
./scripts/setup.ps1
./.venv/Scripts/python.exe -m sprite_lab doctor
./.venv/Scripts/python.exe -m sprite_lab check
./.venv/Scripts/python.exe -m sprite_lab run --ship idris --methods available
./.venv/Scripts/python.exe -m sprite_lab compare --ship idris
./.venv/Scripts/python.exe -m sprite_lab validate --ship idris
./.venv/Scripts/python.exe -m sprite_lab export --ship idris --candidate A04
Start-Process ./outputs/idris/report.html
```

Use the [root setup command](../README.md) for a new clone. Python 3.12+ is required; Pillow 12.3.0 and NumPy 2.3.5 are pinned. Setup creates an isolated local `.venv` with pip, installs the lab (initial Python package downloads required), and runs `doctor`. A legacy shared-runtime `.venv` must be moved aside before rerunning setup; no maintainer-specific runtime is used. `doctor` records actual versions and paths. `check` reuses seven software/data gates without private generated outputs or game data. Run `python -m sprite_lab …` from this folder using the venv interpreter. Set `STARSECTOR_HOME` for native-reference discovery; edit `experiment.json` for the export installation and experiment defaults. Missing game data blocks the example-based export/native cohort, not baseline generation.

`run --methods baseline` regenerates only the fast normalized sources. `run --methods available` uses the saved image-model result and caches deterministic rendering; `--force` re-renders deterministic outputs without any image-provider call. Ctrl+C retains completed images and cached provider output. The CLI launches no local model server, Blender or game process and owns no unrelated processes. The initial lab never installed Blender or used other development environments.

## Files

* `assets/idris/geometry.json`: editable, inferred source-space polygons, material regions, semantic heights, openings and landmarks; preserved on rerun. `anatomy.py` only seeds it initially.
* `assets/idris/canonical-mask.png`, `baseline-transform.json`, `manifest.json`: image contract, transforms and explicit export assumptions.
* `presets/faction.json`: material/light/color/detail controls. M0 preserves source lighting rather than claiming physical relighting.
* `assets/idris/planes.svg`: editable vector scaffold; the Python renderer/geometry JSON also defines procedural shadows, bevels, vents and turret markers. SVG alone is not a complete Blender scene or final painting.
* `outputs/idris/A01.png`–`A09.png`: reviewed candidates. `raw/` keeps first revisions and the new provider return. Two prior supplied studies are contextual only.
* `outputs/idris/report.html`: standalone local report, exact PNG links, neutral-ID comparisons, 100/50/25% views, gray/silhouette, pixel crops, four backgrounds and method key. Use its physical-pixel toggle and verify browser zoom/devicePixelRatio; inspect exact PNGs in an image viewer when in doubt.
* `outputs/idris/validation.json`, `tests.json`, `render-times.json`, `effort.json`: technical gates, seven meaningful software checks, actual processing durations and unmeasured labor fields.
* `outputs/idris/export/`: private unvalidated game scaffold; see [the remaining smoke test](docs/SMOKE_TEST.md). Existing turrets are decorative, with no functional mount slots.
* `reference-private/`: native game art/data for private review only, excluded from exported assets and version control.

Generated outputs and native private references are ignored by version control but retained on disk. Original user inputs are never overwritten. Do not infer redistribution permission from their presence. The normalized gray asset remains source-derived; this lab is not a license grant.

## Image generation and missing arms

One built-in image_gen edit was run in the agent session; model ID and cost were not exposed. Python does not impersonate the provider. The adapter contract is: provide an actual provider-returned RGBA PNG at `outputs/idris/raw/M4-attempt-01.png`, full prompt at `assets/idris/generation-prompt.txt`, source role/hash records, returned dimensions, provider/model/seed/cost where known, and inspect raw structure before compositing. The saved result makes downstream runs repeatable; generating it again is not promised deterministic. No source alpha was forced onto the generated candidate. No CLI/API fallback or API key is required to replay the saved lab.

Blender was not discovered and no genuine mesh was supplied. `scripts/blender_entry.py` is a thin **unexecuted** entry point, with a doctor probe, genuine-mesh import and approximate annotated plate reconstruction. It is not a completed M2/M3 scene. If Blender is supplied, first run its `--doctor`, consult that installed version's APIs, inspect import axes (+Y bow/+Z up), geometry, normals/materials, then run one bounded render, inspect passes and compare under the same gates. Do not call its coarse reconstruction an imported Idris. No Blender pass or render-engine support was measured here.

No different second Star Citizen ship was available. Supply one authorized perpendicular image or genuine mesh with textures and orientation/provenance, keep the shared preset fixed, record per-ship annotation and correction time, and repeat the same image/game acceptance steps before batch expansion.

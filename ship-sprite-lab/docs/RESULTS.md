# Idris experimental result — 20 October 2026

The best geometry-preserving conversion in this run is **M0 masked finishing, A04**. It improves material separation while retaining the supplied render's original relief, weapons, and transparent openings. This is a useful starting recipe for an image-only ship that already has a good perpendicular render. It is not an approved production sprite: its small-scale contrast still trails the friend's finished art, and the game load test has not run.

The new generated candidate A06 has the strongest painted material treatment among this run's conversions. It is a useful art-direction study, but it changes pod proportions, aft supports and internal detail. It fails the structural and alpha gates. The experiment does not establish nearly automatic fleet conversion or acceptable ships per human hour.

Open [the visual report](../outputs/idris/report.html), [equal-hull contact sheet](../outputs/idris/contact-200.png), [technical results](../outputs/idris/validation.json), [measured processing records](../outputs/idris/render-times.json), and [provisional review data](../assets/idris/review.json).

## Inputs and defaults

The actual files were matched by dimensions and visual inspection, not the brief's old filenames. Six supplied PNGs remain byte intact; [inventory](../outputs/idris/inventory.json) includes SHA-256, dimensions, mode, alpha range and partial-pixel counts, bounding boxes, roles, and provenance.

| Brief role | Actual supplied file | Use |
|---|---|---|
| image(6), 2047×1066 | `docs/references/starcitizen_og_model/ChatGPT Image Oct 20, 2026, 12_12_14 PM.png` | Authoritative gray render, bow left; PNG only, no genuine mesh |
| image(7), 1080×575 | `docs/references/fanmadepixelart/ChatGPT Image Oct 20, 2026, 12_12_44 PM.png` | Flat independent interpretation, bow right |
| image(8), 1313×312 | `docs/references/handmadeidrisvsvanillaships.png` | Flattened screenshot reference; not a native sprite pack |
| Friend finished standalone | `docs/references/mfz_idris_hand_made_by_bro.png` | 175×280 RGBA, visible hull 162×262; editable source absent |
| Prior generated studies | Both `docs/references/bychatgpt/*.png` | Supplied historical outputs, unknown prompts/provider; never counted as fresh runs |

Native Eagle, Apogee and Doom PNGs and hull data were read from `H:/Games/Starsector/starsector-core`. Their private working copies and checksums are in `reference-private/` and [native inventory](../outputs/idris/native-reference-inventory.json). This makes the primary style comparison independent of the flattened screenshot. Source rights are not asserted: supplied material and installed-game assets remain private references. The export excludes vanilla art and original reference files.

Defaults were declared in [experiment.json](../experiment.json) before method implementation: 640px hull long edge, 16px margins, one expensive job at a time, one first candidate and at most two focused revisions (M4 at most one revision). Initial active implementation budgets: M0 10 min, M1 10, M2 4, M3 5, M4 12, M5 8. These are agent implementation limits; per-arm active work was not instrumented, so budget adherence is not reported as measured labor. The bounded pass ended after one implementation and at most one revision per available arm. Shared inspection, comparison and reporting are separate.

Gray source rotation is clockwise 90°, without mirroring. Flat source rotation is counterclockwise 90°. They were not averaged or aligned by distorting one hull. Each is normalized by alpha hull bounds, with its aspect ratio retained. A01/A04/A05/A07 are 365×672, with a nominal 333×640 hull. A06 is 387×672 because its 355×640 hull is wider. The friend's A03 is deliberately enlarged only for geometry comparison; its original and the matched 262px comparison are also shown.

All conversions depict the complete assembled ship. Existing visible turrets remain baked static art. The game scaffold has **no functional weapon slots**, avoiding doubled weapons. A separate hull-only asset is not claimed. All weapon pivots and engine exits are inferred suggestions, with ±2 final-pixel annotation uncertainty.

## Available arms and actual results

| Arm | Status | Output and evidence |
|---|---|---|
| M0 existing-image route | COMPLETE | A01 gray, A02 flat, A03 finished friend; A04 masked material finish. One tone revision reduced overbright armor; first output retained in `outputs/idris/raw/M0-first.png`. |
| M1 programmatic 2D | PARTIAL | A05 is an actual new semantic plane reconstruction using canonical alpha, polygon plates, directional bevels, contact shading, ring components, service boxes and simple turret marks. It loses too much machinery and center-deck structure. Source RGB is not reused. Editable [geometry](../assets/idris/geometry.json), [SVG](../assets/idris/planes.svg), preset and renderer retained. First output retained. |
| M2 genuine source mesh | BLOCKED | No supplied genuine mesh or material maps; Blender also undiscovered. A PNG in a model-named folder is not a mesh. No invented replacement was rendered under this label. |
| M3 shallow reconstruction | BLOCKED | No `blender` executable in PATH/common probe paths and no `bpy`. An unexecuted Blender entry point is provided, but no Blender scene or render is claimed. Its first semantic model would still need full silhouette and component verification. |
| M4 guided generation | COMPLETE experiment; acceptance FAIL | One actual built-in image_gen edit. [Raw 924×1702 return](../outputs/idris/raw/M4-attempt-01.png), normalized A06, [full prompt](../assets/idris/generation-prompt.txt), hashes and [record](../outputs/idris/M4-record.json) retained. 34.175s provider latency. Model ID and cost were not returned; mask/strength/seed controls were not exposed. No retry was needed to establish the observed structural limitation. |
| M5 controlled hybrid | COMPLETE experiment; no demonstrated win | A07 uses A04 plus darker annotated machinery and narrow selected bevels. **No stage is generative.** It addresses M0's weak local separation, but its difference is small at 50%/25%. It adds another stage without a clear visual advantage over A04. Base/first/final PNGs retained. |

A08/A09 are prior supplied studies. They have attractive rendering but different geometry and problematic alpha. They are contextual observations, not measured runs of M4.

## Structural gates

Thresholds were defined before ranking: alpha-mask IoU ≥0.985; aspect deviation ≤1.5%; annotated pivot error ≤3 final px with ±2px source uncertainty; margins ≥14px; interior alpha ≥254 in at least 98% of eroded hull pixels; alpha ≤8 at four known genuine openings. Engine pod count is two small plus two large, with one prominent rear ring. Orientation and internal structure also receive explicit visual checks.

| ID | Source mask IoU | Structural result | Main limitation |
|---|---:|---|---|
| A01 | 1.000 | PASS image gates | Untreated gray; low material distinction |
| A02 | 0.945 | FAIL canonical geometry | Independent drawn interpretation |
| A03 | 0.755 | FAIL canonical geometry | Strong authored small-scale art, but different approved interpretation; no criticism of its original design |
| A04 | 1.000 | PASS image gates | Inferred masks; insufficiently crisp depth hierarchy at small size |
| A05 | 1.000 | FAIL components | Canonical alpha was the construction mask, so IoU does not prove internal reconstruction |
| A06 | 0.929 | FAIL aspect/silhouette/alpha/landmarks/components | About 6.6% wider hull; pod/support/deck changes; mainly 253/255 interior alpha |
| A07 | 1.000 | PASS image gates | Extra stage brings little visible gain |
| A08 | 0.726 | FAIL | Design drift and filled sample openings/alpha contamination |
| A09 | 0.725 | FAIL | Design drift and filled sample openings/alpha contamination |

No source alpha was forced onto the generated output. A06 was evaluated after only its own alpha-bounds crop, uniform long-edge normalization and transparent padding. The raw return is preserved. The 253/255 body alpha is a minor opacity defect that could be corrected; that would not repair interior geometry. Four sampled opening centers survive in A06, which demonstrates why sample holes and silhouette alone cannot replace component review.

Source-controlled candidates have zero landmark movement by construction; this is not independent machine detection. Generated landmarks were visually annotated on the original return with ±6 raw-pixel uncertainty (about 2.3 final pixels), then projected to the same frame. [Validation JSON](../outputs/idris/validation.json) records each deviation. The finished friend and flat reference need separately approved geometry if selected as new authorities.

Seven meaningful software checks pass: source/canonical round trip; bow/left-right handedness; four real transparent samples; linear-premultiplied filtering without colored fringes over black/white; small synthetic opening preservation; required export fields/no duplicate turrets; canonical/game transform round trip. These do not establish game compatibility.

## Provisional visual ratings

Ratings are this agent's visual assessment, not feedback from either developer. Scale: 1 weak/unsuitable; 2 major defects; 3 serviceable starting point; 4 strong; 5 close to target for the criterion. Structural failure cannot be overridden by an average. There is no entropy, edge-density, contrast or sharpness beauty metric.

| ID | Fidelity | Forms | Depth | Materials | Cohort fit | Detail restraint |
|---|---:|---:|---:|---:|---:|---:|
| A01 | 5 | 3 | 3 | 1 | 2 | 4 |
| A02 | 3 | 3 | 1 | 3 | 2 | 4 |
| A03 | 2 | 5 | 4 | 4 | 5 | 4 |
| A04 | 5 | 3 | 3 | 4 | 3 | 4 |
| A05 | 2 | 2 | 2 | 3 | 1 | 3 |
| A06 | 3 | 4 | 4 | 5 | 4 | 4 |
| A07 | 5 | 3 | 3 | 4 | 3 | 4 |
| A08 | 2 | 4 | 4 | 5 | 3 | 3 |
| A09 | 2 | 4 | 4 | 5 | 3 | 3 |

Reviewed evidence includes the actual PNGs A01–A09, [200px contact](../outputs/idris/contact-200.png), [50%](../outputs/idris/contact-50percent.png) and [25%](../outputs/idris/contact-25percent.png) display tests, [gray/silhouette overview](../outputs/idris/diagnostic-contact.png), individual four-background sheets, nearest-neighbor aft crops and red/cyan edge overlays under `outputs/idris/diagnostics/`.

The exact PNGs were opened with the image viewer. An attempt to open the HTML report in the in-app browser was rejected because that browser disallows the `file:` protocol. No browser workaround was attempted. HTML links and assets were checked statically; browser-rendered report QA is NOT RUN. The report can be opened locally by the user with the README command.

A01 keeps quiet armor surfaces and source relief, but the gray masses merge. A02 communicates region colors and vents, but has flat planes. A03 has the best small-scale authored readability and a good balance of quiet plates and dark seams; do not judge its 640px interpolation as native blur. A04 retains all gray-source structures while separating warm deck, cool armor and darker aft machinery. Its deck remains low in medium-scale contrast and some inferred region boundaries are broad approximations. A05 reads as a coarse diagram with bevels rather than finished machinery; extra resolution cannot fix that. A06's lit edges, metallic planes and service-box clusters are useful targets for art direction, but it thickens the pods and redesigns supports and deck details. A07 slightly deepens recesses; its small-scale benefit is not convincing. A08/A09 have handsome surface work, but the larger stern/ring treatment and other geometry differ, and their stored alpha/background need repair.

Lighting calibration is provisional visual matching to installed Eagle/Apogee, with Doom as a machinery check. M0 retains baked source lighting: it does not perform physically valid relighting. Geometrically paired mask regions share a single canonical light calculation in M1; shaded halves were never mirrored. Materials, key/fill, exposure, look, seed and detail dimensions are editable in the preset. No Blender view-transform comparison was possible.

## Resolution and color finding

[Resolution contact](../outputs/idris/resolution-contact.png) compares actual 1×/2×/4× M1 procedural production, all reduced to the same final 365×672 canvas. Geometry and feature widths are held in final pixels. The 2× source softens stair-stepped bevels and circular outlines. The 4× source offers little added value for these broad plates. Because M1 is not a leading art method, this result supports sampling behavior only, not a claim about final production quality. Its source alpha starts from the canonical raster, so silhouette sampling is not an independent high-resolution reconstruction.

[Filter contact](../outputs/idris/filter-contact.png) compares BOX area, bicubic and Lanczos reduction of the same original gray raster. Bicubic is a sensible default here; Lanczos gives slightly crisper tiny seams, without a demonstrated improvement worth preferring it globally. No global sharpen was added. M0 has only the supplied raster's native resolution (~3.2× the final long edge); enlarging it to manufacture a 4× experiment would not be a new render and was not done. M4 returned one uncontrolled resolution and was not misrepresented as a resolution sweep.

The custom filter decodes sRGB, premultiplies once, filters color and alpha independently as float channels, divides safely, re-encodes sRGB and writes straight-alpha PNG. Pillow's built-in RGBA conversion is not applied to already premultiplied data. Fully transparent export RGB is cleared. No grayscale-as-depth modeling is used.

## Game scaffold and honest integration status

[Export folder](../outputs/idris/export/idris_lab) contains an isolated development mod, A04 texture, actual-schema `.ship`, CSV based on the installed Eagle row, empty unarmed variant and a mission alongside a native Eagle. [Export evidence](../outputs/idris/export/export-status.json) records hashes for the inspected native examples. Installed `Version.class` contains 0.98a-RC8/RC8p strings; `mod_info` targets the observed 0.98a family. No old editor binary was installed or treated as current.

The coordinate transform is explicit: source pixel center → clockwise rotation → alpha-bounds crop → half-pixel-aware scaling → 16px padding → game `(forward X, left Y)`. Native `.ship` center is treated as from the bottom-left. For this provisional 1 draw-unit/pixel scaffold: `gameX = 672 - 336 - imageY`; `gameY = 182.5 - imageX`. [Native-coordinate evidence](../outputs/idris/native-coordinate-evidence.png) projects real Eagle mount and exhaust coordinates onto its own image and visually aligns. [Idris debug overlay](../outputs/idris/debug-overlay.png) and [numbered key](../outputs/idris/debug-overlay-key.json) cover bow, left/right pair, weapon suggestions and four exits.

The hull uses one conservative convex bounds suggestion. It intentionally encloses negative spaces; transparent holes are not claimed as collision holes. Draw dimensions 365×672 are development placeholders, not physically calibrated scale. Stats are development placeholders derived from a known working native schema, not balancing. Functional weapon art, pivot rotation/layering, center of mass and combat collisions remain unverified.

**Actual load test: NOT RUN.** The installation was available for read-only inspection, but native interactive control/capture is unavailable in this session. Launching an unobserved game does not establish a test. No existing mod list, launcher, save, installation file, or NearFuture task was changed. [Smoke-test instructions](SMOKE_TEST.md) and [isolated launcher](../scripts/launch-isolated.ps1) are supplied. The launcher has been syntax-checked only, and has not been executed.

## Effort, repeatability and decision

Actual per-stage processing durations are recorded, including image generation latency. Reusable setup time, per-ship annotation time, original artist time, actual human cleanup time and integration correction time are **NOT MEASURED**. Cost is **UNKNOWN**. [Effort record](../outputs/idris/effort.json) distinguishes setup from ship-specific work and iterations. A low processing time must not be interpreted as high accepted-ships/hour: no candidate completed the game acceptance step.

No distinct second Star Citizen ship was supplied. Fleet generalization is **UNTESTED**. A recolor, second Idris interpretation, native Starsector sprite or synthetic fixture would not count. To test next: supply a substantially different ship as a clean perpendicular RGBA render (or genuine mesh plus textures), with bow direction, source/permission notes, and preferably a separate finished target. Keep `presets/faction.json` fixed, annotate its major regions/landmarks, run the same output contract and gates, measure annotation and correction time, then run the isolated load test. Log exceptions before changing the shared preset.

The evidence supports a **bounded annotation and finishing recipe for this already-rendered input**, provisionally. It does not establish nearly automatic conversion. Keep A04 as the geometry-safe working candidate and A06 as an explicit style study. The next human art decision is to approve the authoritative interpretation and localized value/shading corrections; the next technical acceptance step is the isolated game test. Do not bulk generate a fleet yet. Normalization, source inventory, deterministic finishing after annotation, contact sheets, gates and export scaffolds can already be batched; semantic annotation and acceptance cannot be assumed automatic. Real source meshes should be evaluated separately through M2 when available.

## Reading and access evidence

The brief's [Baumgart Part 1](https://fractalsoftworks.com/2014/05/16/let-me-draw-you-a-starsector-ship/), [Part 2](https://fractalsoftworks.com/2014/05/22/let-me-draw-you-a-starsector-ship-part-2/), [December 2013 archive](https://fractalsoftworks.com/2013/12/), and [historical practitioner thread](https://fractalsoftworks.com/forum/index.php?topic=7469.0) could not be fetched by this session's web tool (402/access failure). Their specific content was not falsely claimed as directly read. The execution brief supplied historical context; this run's decisions primarily follow the inspected native art and outputs.

[Michael Zahniser's original Endless Sky article](https://endless-sky.github.io/2016/09/08/designing-ship-sprites.html) was read. It supports iterative rendering, selective detail, bevels, lighting and restrained finishing as a separate-game workflow; its game-specific sizing conventions were not imported. [Ship-Editor README](https://github.com/Ontheheavens/Ship-Editor) was read for data-role context; installed native hulls and mission sources establish this scaffold's actual fields. [Pillow concepts](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) was consulted for alpha modes. The Blender manual camera/pass/CLI URLs also returned access failures; no installed Blender was available, so `scripts/blender_entry.py` remains explicitly unexecuted and requires installed-version verification before use.

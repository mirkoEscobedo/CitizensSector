# Isolated game smoke test — NOT RUN

This is the remaining interactive test. The prepared files are a scaffold, not evidence of a successful game load.

1. From `ship-sprite-lab`, run `./.venv/Scripts/python.exe -m sprite_lab export --ship idris --candidate A04`.
2. Review `outputs/idris/export/idris_lab`, `debug-overlay.png` and `debug-overlay-key.json`. The assembled image contains turrets; the empty weapon slot list is intentional.
3. Run `./scripts/launch-isolated.ps1 -GameHome 'H:\Games\Starsector'`. It reads the existing minimal launcher, passes arguments directly to Java, and overrides mod/save/log/screenshot paths to this lab's outputs. It does not rewrite the installation launcher or normal enabled-mod list. Java/native/renderer compatibility and the script's actual startup remain untested. If this modified installation's launcher needs other flags, change a lab-local copy only.
4. At the title screen, confirm that only the private lab mod is enabled. Record the displayed game version. Select Missions → Idris LAB art inspection. If it fails, retain `outputs/idris/game-run/logs` and record the first relevant error; do not edit unrelated installed mods to make it pass.
5. Check the bow and handedness, center/origin, four exhaust exits, length/width relative to the reference Eagle, clockwise/counterclockwise rotation, default and close zoom, normal projectiles/exhaust effects and dark/light backgrounds. The provisional texture-to-draw scale is 1:1; approve or adjust draw dimensions explicitly once, with updated point transforms.
6. Capture screenshots in the lab screenshot directory at documented resolution/UI scale. Record zoom as observed rather than equating browser 50%/25% previews with game zoom. Save loading evidence, full hull, engine alignment, rotation, and normal combat effects.
7. Functional weapon alignment remains a separate test: first create a hull-only version with weapon pixels intentionally removed while preserving static mounts. Then use the inspected native `.ship` schema and known working weapons to test pivots, angles and layering. Never add a functional turret on top of the assembled texture's baked turret. Mark untested weapons individually.
8. Inspect collisions and shield position. The current convex enclosure covers gaps by design and is only a conservative suggestion. Adjust supported bounds from game evidence; do not treat every image opening as a collision hole.
9. Exit the lab game. No normal saves or mod configuration should have been changed. Fill in load status, corrections, observed version, capture paths, developer ratings and actual time. Only then reassess production acceptance.

If launch isolation is uncertain, use a separate user-managed test installation and place only this scaffold there. Nothing requires changing the ongoing NearFuture development environment.

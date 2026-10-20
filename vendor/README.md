# Retained workspace-template package

Copied byte-for-byte from [`mirkoEscobedo/NearFuture` at `0a531d7e150f0a94dc961abcb7118e81001245be`](https://github.com/mirkoEscobedo/NearFuture/blob/0a531d7e150f0a94dc961abcb7118e81001245be/vendor/workspace-template-win32-x64-0.9.0-alpha.0.tgz). Only this tooling archive was adopted; no NearFuture runtime, Rust commands, backlog or branch policy was copied.

- Package: `workspace-template-win32-x64@0.9.0-alpha.0`, retained unsigned development build, unpublished.
- Archive SHA-256: `95c61b973fd68204289f257fae957589a921d4ff4331f552c11b72015d1d38f5`.
- npm integrity (also in CitizensSector's own lockfile): `sha512-AjOlfFH9Zghq3I1RrF5zvTf0ySSiYKd92dm3YzHwNA4swndMSzqNmpinLsAz598eTwX4lX0JvZIyw6e5sVyP5w==`.
- Installed executable SHA-256: `00e272fdf9a406fc15619c1c7fecec36c39ebea04a184c5d9f725a3ce83213d0` (914944 bytes).
- Source/release commit: `9b76e0312d83ff30538f97b6ceb05432580799e2`.
- Embedded asset manifest SHA-256: `7b26e29938f10a7214b77b1325a736edfa85fec4d229e5b114e1b4615f129d8f`.
- Release manifest SHA-256: `35b949caa9e35a45870dfb8dedb9b54c4e840670949f0633eac55cc5ad5d4361`.

The archive retains upstream `LICENSE`, `THIRD_PARTY_NOTICES.md`, SBOM and exact `workspace-template.provenance.json`. License/notices are also adjacent here for review. After install they are in `node_modules/workspace-template-win32-x64/`. The MIT license covers this tool, not supplied ship images or game data. A build with a different hash is an upgrade even if its version string matches.

Adoption used this installed executable after inspecting `help`, `instructions`, README and schema:

```powershell
$tool = '.\node_modules\workspace-template-win32-x64\bin\workspace-template.exe'
if (-not (Test-Path -LiteralPath $tool)) { throw 'Run setup first' }
& $tool adopt plan . --plan-out .onboarding-cache/adopt-plan.json
# Review operations/conflicts before applying the sealed plan:
& $tool adopt apply . --apply-plan .onboarding-cache/adopt-plan.json
```

The applied plan created the managed AGENTS/ignore blocks and thin project state. CitizensSector's local guidance and structured command override were added afterward. Generic skills remain package-owned; source builds, sibling checkouts and npm publication are unnecessary.

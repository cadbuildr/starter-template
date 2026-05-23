# starter-template

Starting point for a new CAD project with [CADbuildr](https://cadbuildr.com).

A tiny Python package with three example parts — a `CadbuildrPlate`, a
`Spacer`, and the `CadbuildrSign` assembly that bolts them together — plus
a [Vite + React-Three-Fiber demo](github-io/) that renders the assembly
live through the CADbuildr SDK.

➡️ **Live demo**: https://cadbuildr.github.io/starter-template/

## Get started

The fastest path is the desktop **CADbuildr prototype app** — it shells
the in-browser workbench and runs your Python with the system
interpreter, so you get hot-reload + a real CAD viewer.

```bash
# 1. fork or clone
git clone https://github.com/cadbuildr/starter-template.git
cd starter-template

# 2. install foundation
uv sync
```

Then open `starter-template/` in the **CADbuildr prototype** (File → Open
folder), press **Play** on `starter/office_sign_assy.py`, and the
assembly renders in the viewer. Edit the file, hit Play again, watch it
reshape.

### Don't have the prototype yet?

You can also run any example as a plain Python script — it'll print the
DAG and call `show(...)`. To see the geometry in 3D you'll need either
the prototype or the public viewer at
[hub.cadbuildr.com/viewer](https://hub.cadbuildr.com/viewer).

```bash
uv run python starter/office_sign_assy.py
```

## What's in here

```
├── starter/                Python package
│   ├── cadbuildr_plate_part.py    a circular plate with the CADbuildr logo + 3 holes
│   ├── spacer_part.py             a cylindrical spacer with a centre hole
│   └── office_sign_assy.py        Assembly: 1 plate + 3 spacers
├── github-io/              Vite + R3F demo site (deploys to GitHub Pages)
├── pyproject.toml          Python package manifest
└── logo.png                used by the prototype's project picker
```

## Make it your own

1. **Rename the package.** Change `starter/` to your package name; mirror
   it in `pyproject.toml` (`[project].name`, `[tool.hatch.build.targets.wheel].packages`).
2. **Write your Parts.** A Part is a Python class that adds operations
   (sketches, extrusions, fillets, etc.) to itself. See
   [`spacer_part.py`](starter/spacer_part.py) for a small example.
3. **Assemble them.** An Assembly adds Parts (or other Assemblies) with
   transforms. See [`office_sign_assy.py`](starter/office_sign_assy.py).
4. **Ship your own demo site.** Copy `github-io/`, change the package
   imports + the wheel filename in `src/starterLocal.ts`, set
   `VITE_APP_BASE_PATH` to your repo path, and let the
   [GitHub Pages workflow](.github/workflows/deploy-pages.yml) do the rest.

## Deploy your own GitHub Pages demo (optional)

The site uses the [CADbuildr SDK browser flow](https://docs.cadbuildr.com/sdk/auth) — a
short-lived session token is minted client-side using only the
**publishable half** of a partner key (the secret stays on hub).

1. Mint an SDK key at https://hub.cadbuildr.com/settings:
   - **Allowed origins**: `https://<your-github-username>.github.io`
   - **Allowed projects**: `starter-template`
2. In your repo's *Settings → Secrets and variables → Actions*, add a
   secret named **`CADBUILDR_SDK_KEY_ID`** with the public `<keyId>` half
   of your key (e.g. `624fe53d82c9fa7c`, not the full `cbsdk_*` string).
3. Enable Pages with build source = "GitHub Actions" and push.

The workflow rebuilds the Python wheel, stages it into
`github-io/public/local-starter/`, then builds and deploys the Vite site.

## License

MIT — fork freely.

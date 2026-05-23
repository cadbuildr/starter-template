# starter-template github-io site

The Vite + React-Three-Fiber landing page at
https://cadbuildr.github.io/starter-template/.

## Stack

- **Vite + React 19** — landing page shell, onboarding steps
- **Pyodide** — runs the Python `starter` package in-browser
- **[@cadbuildr/cad-pyodide-runtime](https://www.npmjs.com/package/@cadbuildr/cad-pyodide-runtime)** — bootstraps Pyodide + installs the wheel from `public/local-starter/`
- **[@cadbuildr/sdk-react](https://www.npmjs.com/package/@cadbuildr/sdk-react)** — sends the DAG to the CADbuildr kernel-api, returns a mesh, renders it in R3F

## Local dev

```sh
npm install
npm run sync-starter-wheel   # one-time: builds ../dist/*.whl and copies into public/local-starter/
npm run dev                  # opens http://localhost:3009
```

## Configuration

`.env.local` (gitignored):

```ini
# Publishable keyId — mint at https://hub.cadbuildr.com/settings
VITE_CADBUILDR_SDK_KEY_ID=<your keyId>

# Optional: dev hub override
# VITE_CADBUILDR_HUB_BASE_URL=https://hub-yg72zqen7a-uw.a.run.app
# Optional: dev kernel-api override
# VITE_KERNEL_API_BASE_URL=https://kernel-api-yg72zqen7a-uw.a.run.app
```

## Production build

```sh
VITE_APP_BASE_PATH=/starter-template/ \
VITE_CADBUILDR_SDK_KEY_ID=<your keyId> \
npm run build
```

Outputs `dist/`. The repo's [GitHub Pages workflow](../.github/workflows/deploy-pages.yml)
runs that build (reading the keyId from a `CADBUILDR_SDK_KEY_ID` secret)
and deploys `dist/` to Pages.

import React from "react";
import ReactDOM from "react-dom/client";
import {
  Download,
  ExternalLink,
  GitFork,
  Github,
  Play,
  Sparkles,
} from "lucide-react";

import { type KernelDag } from "@cadbuildr/cad-kernel-r3f";
import {
  initializeCadPyodideRuntime,
  runCadPythonCode,
  type PyodideLike,
} from "@cadbuildr/cad-pyodide-runtime";
import { CadbuildrProvider, CadbuildrViewer } from "@cadbuildr/sdk-react";

import { resolveKernelApiBaseUrl } from "./kernelApiEnv";
import { LOCAL_STARTER_URL_SEGMENT, LOCAL_STARTER_WHEEL_FILE } from "./starterLocal";
import "./styles.css";

const FOUNDATION_IMPORT_PATH = "cadbuildr.foundation";
const FOUNDATION_DAG_UTILS_PATH = "cadbuildr.foundation.dag_utils";
const FOUNDATION_PACKAGE_NAME = "cadbuildr-foundation";
const FOUNDATION_VERSION = "^0.2.8";
const STARTER_IMPORT_PATH = "starter";
const SCENE_BG = "#0e1216";

const REPO_HTTPS = "https://github.com/cadbuildr/starter-template";
// CADbuildr Prototype download page (web app's /downloads route on cadbuildr.com).
const PROTOTYPE_DOWNLOAD = "https://cadbuildr.com/downloads";

function resolveStarterWheelUrl(): string {
  const explicit = (import.meta.env.VITE_STARTER_PACKAGE_WHEEL_URL as string | undefined)?.trim();
  if (explicit) return explicit;
  const base = import.meta.env.BASE_URL ?? "/";
  const normalized = base.endsWith("/") ? base : `${base}/`;
  return `${normalized}${LOCAL_STARTER_URL_SEGMENT}/${LOCAL_STARTER_WHEEL_FILE}`;
}

const PYTHON_RENDER_SOURCE = `
from cadbuildr.foundation import show
from starter.office_sign_assy import CadbuildrSign

show(CadbuildrSign())
`.trim();

function buildFoundationCompatibilityScript(foundationImportPath: string): string {
  return `
from importlib import import_module
import sys
import types

foundation = import_module(${JSON.stringify(foundationImportPath)})
_submodules = ("gen", "gen.models", "gen.runtime", "dag_utils", "utils", "helpers", "constants")
for _prefix in ("cad_package", "cadbuildr"):
    legacy_alias = _prefix + ".foundation"
    sys.modules[legacy_alias] = foundation
    _root = sys.modules.get(_prefix)
    if _root is None:
        _root = types.ModuleType(_prefix)
        _root.__path__ = []
        sys.modules[_prefix] = _root
    setattr(_root, "foundation", foundation)
    for _suffix in _submodules:
        try:
            _mod = import_module(${JSON.stringify(foundationImportPath)} + "." + _suffix)
        except ModuleNotFoundError:
            continue
        sys.modules[legacy_alias + "." + _suffix] = _mod
`.trim();
}

function buildFoundationShowRebindScript(foundationImportPath: string): string {
  return `
import builtins
from importlib import import_module

_root = import_module(${JSON.stringify(foundationImportPath)})
_dag_utils = import_module(${JSON.stringify(foundationImportPath)} + ".dag_utils")
_hook = builtins.show
_root.show = _hook
_dag_utils.show = _hook
`.trim();
}

function buildStarterInstallScript(opts: { wheelUrl: string; importPath: string }): string {
  return `
import importlib
import micropip

wheel_url = ${JSON.stringify(opts.wheelUrl ?? "")}
import_path = ${JSON.stringify(opts.importPath)}

try:
    importlib.import_module(import_path)
    _needs_install = False
except Exception:
    _needs_install = True

install_errors = []
if _needs_install and wheel_url:
    try:
        await micropip.install(wheel_url, deps=False)
    except Exception as error:
        install_errors.append(f"wheel install failed ({wheel_url}): {error}")

try:
    importlib.import_module(import_path)
except Exception as error:
    detail = "\\n".join(install_errors) if install_errors else "No install attempt was made."
    raise RuntimeError(
        f"Could not import {import_path!r} after install attempts.\\n{detail}\\nLast import error: {error}"
    )
`.trim();
}

function App(): React.ReactElement {
  const [runtimeReady, setRuntimeReady] = React.useState(false);
  const [dag, setDag] = React.useState<KernelDag | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const pyodideRef = React.useRef<PyodideLike | null>(null);

  const kernelApiBaseUrl = React.useMemo(() => resolveKernelApiBaseUrl(), []);
  const sdkKeyId = React.useMemo(
    () => (import.meta.env.VITE_CADBUILDR_SDK_KEY_ID as string | undefined)?.trim() || undefined,
    [],
  );
  const hubBaseUrl = React.useMemo(
    () => (import.meta.env.VITE_CADBUILDR_HUB_BASE_URL as string | undefined)?.trim() || undefined,
    [],
  );

  React.useEffect(() => {
    let cancelled = false;
    async function bootstrap() {
      try {
        setError(null);
        const pyodide = await initializeCadPyodideRuntime({
          packages: {
            foundation: FOUNDATION_VERSION,
            foundationPackageName: FOUNDATION_PACKAGE_NAME,
          },
          foundationImportPath: FOUNDATION_IMPORT_PATH,
          foundationDagUtilsPath: FOUNDATION_DAG_UTILS_PATH,
        });
        if (cancelled) return;
        await pyodide.runPythonAsync(buildFoundationCompatibilityScript(FOUNDATION_IMPORT_PATH));
        await pyodide.runPythonAsync(buildFoundationShowRebindScript(FOUNDATION_IMPORT_PATH));
        await pyodide.runPythonAsync(
          buildStarterInstallScript({
            wheelUrl: resolveStarterWheelUrl(),
            importPath: STARTER_IMPORT_PATH,
          }),
        );
        if (cancelled) return;
        pyodideRef.current = pyodide;
        setRuntimeReady(true);
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : String(err));
      }
    }
    void bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  React.useEffect(() => {
    if (!runtimeReady || !pyodideRef.current) return;
    let cancelled = false;
    (async () => {
      try {
        setError(null);
        const result = await runCadPythonCode(
          pyodideRef.current as PyodideLike,
          PYTHON_RENDER_SOURCE,
          {
            foundationImportPath: FOUNDATION_IMPORT_PATH,
            foundationDagUtilsPath: FOUNDATION_DAG_UTILS_PATH,
          },
        );
        if (cancelled) return;
        setDag((result.dag as KernelDag | null) ?? null);
      } catch (err) {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : String(err));
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [runtimeReady]);

  return (
    <div className="page">
      <header className="topbar">
        <span className="brand">
          <span className="dot" /> cadbuildr starter template
        </span>
        <span className="links">
          <a href="https://cadbuildr.com" target="_blank" rel="noreferrer">
            cadbuildr.com <ExternalLink size={12} style={{ verticalAlign: "-1px" }} />
          </a>
          <a href={REPO_HTTPS} target="_blank" rel="noreferrer">
            <Github size={14} style={{ verticalAlign: "-2px", marginRight: 4 }} />
            Source
          </a>
        </span>
      </header>

      <section className="hero">
        <h1>
          Your CAD project, <span className="emph">in a fork.</span>
        </h1>
        <p className="lead">
          This is the starter template — a tiny Python package with three example parts
          (a plate, a spacer, and the assembled office sign you see on the right). Fork
          it, open it in CADbuildr Prototype, and you're building.
        </p>
        <div className="badges">
          <span className="badge">cadbuildr-foundation</span>
          <span className="badge gray">Pyodide → kernel-api → R3F</span>
          <span className="badge gray">@cadbuildr/sdk-react</span>
        </div>
      </section>

      <section className="workspace">
        <div className="steps panel">
          <h2>Start in under a minute</h2>
          <ol>
            <li>
              <strong>
                <GitFork size={14} style={{ verticalAlign: "-2px", marginRight: 6 }} />
                Fork or clone this repo
              </strong>
              <p>Click <strong>Fork</strong> on the <a href={REPO_HTTPS} target="_blank" rel="noreferrer">GitHub page</a>, or:</p>
              <div className="snippet">
                git clone {REPO_HTTPS}.git
                <br />
                cd starter-template
              </div>
            </li>
            <li>
              <strong>
                <Download size={14} style={{ verticalAlign: "-2px", marginRight: 6 }} />
                Open it in CADbuildr Prototype
              </strong>
              <p>
                CADbuildr Prototype is the desktop app — it shells the in-browser
                workbench and runs your Python with the system interpreter, so you get
                hot-reload + a real CAD viewer. File → Open folder → pick the cloned
                <code> starter-template/</code>.
              </p>
              <a className="cta" href={PROTOTYPE_DOWNLOAD} target="_blank" rel="noreferrer">
                Get CADbuildr Prototype <ExternalLink size={14} />
              </a>
            </li>
            <li>
              <strong>
                <Play size={14} style={{ verticalAlign: "-2px", marginRight: 6 }} />
                Press Play on an example
              </strong>
              <p>
                Open <code>starter/office_sign_assy.py</code> and hit the Play button —
                CADbuildr Prototype renders the assembly in the viewer. Tweak parameters,
                hit Play again, watch it reshape.
              </p>
            </li>
            <li>
              <strong>
                <Sparkles size={14} style={{ verticalAlign: "-2px", marginRight: 6 }} />
                Make it yours
              </strong>
              <p>
                Rename <code>starter/</code> to your package name, write new Parts and
                Assemblies, and publish your own GitHub Pages demo by copying the
                <code> github-io/</code> folder.
              </p>
            </li>
          </ol>
        </div>

        <div className="panel viewer-panel">
          <div className="viewer-header">
            <span>example: <code>CadbuildrSign()</code></span>
            <span>cadbuildr-foundation</span>
          </div>
          {!sdkKeyId ? (
            <div className="viewer-status error" style={{ flexDirection: "column", gap: 8 }}>
              <strong>No SDK key configured.</strong>
              <span style={{ maxWidth: 380, textAlign: "center", color: "var(--cb-text-soft)" }}>
                Set <code>VITE_CADBUILDR_SDK_KEY_ID</code> (or the GitHub Actions
                secret <code>CADBUILDR_SDK_KEY_ID</code>) to mint a session token.
                Get a key from{" "}
                <a href="https://hub.cadbuildr.com/settings" target="_blank" rel="noreferrer">
                  hub Settings
                </a>.
              </span>
            </div>
          ) : error ? (
            <div className="viewer-status error">{error}</div>
          ) : !runtimeReady || !dag ? (
            <div className="viewer-status">
              <span className="spinner" />
              {runtimeReady ? "Rendering…" : "Booting in-browser Python…"}
            </div>
          ) : null}

          {sdkKeyId ? (
            <CadbuildrProvider
              baseUrl={kernelApiBaseUrl}
              hubBaseUrl={hubBaseUrl}
              keyId={sdkKeyId}
              projectKey="starter-template"
            >
              <CadbuildrViewer
                dag={dag}
                background={SCENE_BG}
                cameraPosition={[260, 220, 320]}
                meshPosition={[0, 0, 0]}
                showHelpers={false}
                onError={(meshError) => setError(meshError.message)}
              />
            </CadbuildrProvider>
          ) : null}
        </div>
      </section>

      <footer className="foot">
        <a className="powered-by" href="https://cadbuildr.com" target="_blank" rel="noreferrer">
          <span>Powered by</span>
          <img src="cadbuildr-logo.svg" alt="CADbuildr" />
          <span className="cb">CADbuildr</span>
        </a>
        <span>MIT — fork freely.</span>
      </footer>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);

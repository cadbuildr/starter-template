import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vite";

import { LOCAL_STARTER_URL_SEGMENT, LOCAL_STARTER_WHEEL_FILE } from "./src/starterLocal";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Dev-only: stream the wheel from `../dist/` (run `uv build` in the starter package dir). */
function serveLocalStarterWheelFromDist(): Plugin {
  return {
    name: "serve-local-starter-wheel-from-dist",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const pathname = req.url?.split("?")[0] ?? "";
        const tail = `/${LOCAL_STARTER_URL_SEGMENT}/${LOCAL_STARTER_WHEEL_FILE}`;
        if (!pathname.endsWith(tail)) {
          next();
          return;
        }
        const wheelPath = path.resolve(__dirname, "..", "dist", LOCAL_STARTER_WHEEL_FILE);
        if (!fs.existsSync(wheelPath)) {
          res.statusCode = 404;
          res.setHeader("Content-Type", "text/plain; charset=utf-8");
          res.end(
            `Missing starter wheel at ${wheelPath}.\nRun: uv build in the Python package directory (parent of github-io/)`
          );
          return;
        }
        res.setHeader("Content-Type", "application/octet-stream");
        fs.createReadStream(wheelPath).pipe(res);
      });
    },
  };
}

export default defineConfig({
  base: (process.env.VITE_APP_BASE_PATH as string | undefined) ?? "/",
  plugins: [react(), serveLocalStarterWheelFromDist()],
  server: {
    host: "0.0.0.0",
    port: 3009,
  },
  build: {
    outDir: "dist",
  },
});

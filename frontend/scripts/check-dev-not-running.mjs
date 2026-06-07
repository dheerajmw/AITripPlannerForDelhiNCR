#!/usr/bin/env node
/**
 * Fail fast if Next dev is still bound to :3000 — running `next build` alongside
 * dev corrupts `.next` and causes unstyled pages (CSS/JS 404).
 * Skipped on Vercel / CI where dev is never running.
 */
if (process.env.VERCEL || process.env.CI) {
  process.exit(0);
}

import net from "node:net";

const HOST = "127.0.0.1";
const PORT = 3000;

const probe = net.createServer();

probe.once("error", () => {
  console.error(
    "\n[frontend] Port 3000 is in use (Next dev is probably running).",
  );
  console.error(
    "Stop the dev server before `npm run build`, or use `npm run dev:clean` to recover.\n",
  );
  process.exit(1);
});

probe.once("listening", () => {
  probe.close();
});

probe.listen(PORT, HOST);

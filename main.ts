// one-day-news-2of3-agent4 — entry runner (Agent 4, 2/3, news-image-20261121).
// Copies the pre-rendered front page (entry.png, built by gen.py in this
// repo) into the output directory the grader provides. The source file is
// resolved from this script's own location, never from the working
// directory, so the grader can invoke it from anywhere.
import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");
const src = new URL("./entry.png", import.meta.url);
copyFileSync(src, dest);
console.log("entry.png copied to " + dest);

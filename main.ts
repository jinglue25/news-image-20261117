// Copy the pre-rendered entry.png into $MAKEFUN_OUTPUT_DIR (default /output).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const source = fileURLToPath(new URL("./entry.png", import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

if (!existsSync(source)) {
  console.error("Missing entry.png. Run python3 draw.py first.");
  process.exit(1);
}

try {
  mkdirSync(outputDir, { recursive: true });
  copyFileSync(source, join(outputDir, "entry.png"));
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Unable to copy entry.png to ${outputDir}: ${message}`);
  process.exit(1);
}

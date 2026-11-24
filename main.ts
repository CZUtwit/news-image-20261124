// news-image-20261124 entry (Node 22, standard library only).
// The image is the entry.png beside this file: one picture summing up the
// world news of Tuesday 24 November 2026, drawn by tools/make_image.py.
// The program copies it to /output/entry.png. It runs with no network and
// writes the same bytes on every run.
//
// Run it outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
if (!existsSync(dest) || statSync(dest).size === 0) {
  throw new Error('entry.png was not written');
}

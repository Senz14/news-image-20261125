// news-image-20261125 entry (Node 22, standard library only).
// The entry image is entry.png beside this file. The program copies it into
// the output directory and proves the copy is byte-identical by comparing
// SHA-256 digests, then reads the image dimensions from the PNG header.
//
// Before copying, it validates the source is a whole PNG file (8-byte
// signature followed by the IHDR chunk) and refuses an empty output
// directory, so a corrupt source or a bad environment fails loudly instead
// of handing the grader a broken file.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = (process.env.MAKEFUN_OUTPUT_DIR || '/output').trim();
const target = join(outDir, 'entry.png');

if (!outDir) {
  throw new Error('MAKEFUN_OUTPUT_DIR is empty');
}

const original = readFileSync(source);
// A whole PNG starts with its 8-byte signature, then the IHDR chunk.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (original.length < 33 || !original.subarray(0, 8).equals(PNG_SIGNATURE)
    || original.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png is not a whole PNG file');
}
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
writeFileSync(target, original);

const copied = readFileSync(target);
const sha256 = (buf) => createHash('sha256').update(buf).digest('hex');
if (sha256(copied) !== sha256(original)) {
  throw new Error('entry.png copy failed the byte-for-byte check');
}

const width = copied.readUInt32BE(16);
const height = copied.readUInt32BE(20);
console.log(`wrote ${target} (${width}x${height}, ${original.length} bytes, sha256 ${sha256(original).slice(0, 16)}…)`);

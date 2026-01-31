#!/usr/bin/env node
/**
 * Fast Large File Generator
 * Generates N lines of text to a file — bypasses Qwen context limits.
 * Usage: node generate-large-file.js [lines=10000] [output=./large.txt] [prefix="line "]
 */

const fs = require('fs').promises;
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  const lineCount = parseInt(args[0]) || 10000;
  const outputPath = args[1] || './large.txt';
  const prefix = args[2] || 'line ';

  console.log(`Generating ${lineCount} lines to: ${path.resolve(outputPath)}`);

  const stream = fs.createWriteStream(outputPath, { encoding: 'utf8' });
  
  for (let i = 1; i <= lineCount; i++) {
    stream.write(`${prefix}${i}\n`);
    // Flush every 1000 lines to avoid memory buildup
    if (i % 1000 === 0) await new Promise(resolve => stream.write('', resolve));
  }

  stream.end();
  await new Promise((resolve) => stream.on('finish', resolve));
  console.log('✅ Done.');
}

main().catch(console.error);
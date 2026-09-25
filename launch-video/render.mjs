// Renders index.html frame-by-frame with headless Chromium and pipes the frames into ffmpeg.
//
//   node render.mjs --preview 1.2,5,9.5 [--out previews]   → PNG stills at given times
//   node render.mjs --video out.mp4 [--fps 60] [--workers 4] [--audio music.wav]
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => {
  if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]);
  return acc;
}, []));
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const W = 1920, H = 1080;
const chromePath = process.env.CHROME_PATH; // optional override

async function openPage() {
  const browser = await chromium.launch({ executablePath: chromePath, args: ['--force-color-profile=srgb', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') console.error('[page]', m.text()); });
  await page.goto('file://' + resolve(here, 'index.html'));
  await page.evaluate(() => window.ready);
  return { browser, page };
}

async function renderRange(from, to, fps, outFile) {
  const { browser, page } = await openPage();
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', outFile], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = from; f < to; f++) {
    await page.evaluate(t => window.render(t), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - from) % 120 === 0) console.log(`${outFile}: frame ${f - from}/${to - from}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
}

if (args.preview) {
  const out = resolve(here, args.out || 'previews');
  mkdirSync(out, { recursive: true });
  const { browser, page } = await openPage();
  for (const t of String(args.preview).split(',').map(Number)) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: join(out, `t${t.toFixed(2)}.png`) });
  }
  await browser.close();
} else if (args.segment) {
  const [from, to] = args.segment.split(':').map(Number);
  await renderRange(from, to, Number(args.fps || 60), args.file);
} else if (args.video) {
  const fps = Number(args.fps || 60), workers = Number(args.workers || 4);
  const { browser, page } = await openPage();
  const duration = await page.evaluate(() => window.DURATION);
  await browser.close();
  const total = Math.round(duration * fps), per = Math.ceil(total / workers);
  const tmp = resolve(here, '.segments'); rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp);
  const segs = [];
  await Promise.all([...Array(workers).keys()].map(i => {
    const from = i * per, to = Math.min(total, from + per), file = join(tmp, `seg${i}.mp4`);
    segs.push(file);
    return new Promise((res, rej) => {
      const p = spawn(process.execPath, [fileURLToPath(import.meta.url), '--segment', `${from}:${to}`, '--fps', String(fps), '--file', file], { stdio: 'inherit' });
      p.on('close', c => c === 0 ? res() : rej(new Error('segment failed ' + i)));
    });
  }));
  writeFileSync(join(tmp, 'list.txt'), segs.sort().map(s => `file '${s}'`).join('\n'));
  const outArgs = ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', join(tmp, 'list.txt')];
  if (args.audio) outArgs.push('-i', resolve(args.audio), '-c:a', 'aac', '-b:a', '256k', '-shortest');
  outArgs.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', resolve(args.video));
  execFileSync(FFMPEG, outArgs, { stdio: 'inherit' });
  rmSync(tmp, { recursive: true, force: true });
  console.log('wrote', args.video);
}

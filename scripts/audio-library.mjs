#!/usr/bin/env node
// Writes the list of Scriptorium books that have audio, as audio-library.md and
// audio-library.html in the Scriptorium data folder. Re-run after new audio:
//   node scripts/audio-library.mjs [dataDir]
import { readdirSync, readFileSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { execFileSync } from "node:child_process";

const dataDir = process.argv[2] ?? "C:/Users/Infplane/Scriptorium";
const booksDir = join(dataDir, "books");

const field = (md, key) => {
  const m = md.match(new RegExp(`^${key}:\\s*(.*)$`, "m"));
  return m ? m[1].trim().replace(/^["']|["']$/g, "") : "";
};
const seconds = (file) => {
  try {
    return Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file]).toString().trim()) || 0;
  } catch { return 0; }
};
const hms = (s) => { const h = Math.floor(s / 3600), m = Math.round((s % 3600) / 60); return h ? `${h} h ${m} min` : `${m} min`; };
const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const withAudio = [], without = [];
for (const slug of readdirSync(booksDir).sort()) {
  const bookMd = join(booksDir, slug, "book.md");
  if (!existsSync(bookMd)) continue;
  const md = readFileSync(bookMd, "utf8");
  const book = { slug, title: field(md, "title") || slug, format: field(md, "format"), stage: field(md, "stage"), score: field(md, "score") };
  if (book.stage !== "published") continue;
  const audioDir = join(booksDir, slug, "out", "audio");
  const m3u = existsSync(audioDir) ? readdirSync(audioDir).find((f) => f.endsWith(".m3u")) : undefined;
  const tracks = m3u
    ? readFileSync(join(audioDir, m3u), "utf8").split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith("#"))
    : existsSync(audioDir) ? readdirSync(audioDir).filter((f) => f.endsWith(".mp3")).sort() : [];
  if (!tracks.length) { without.push(book); continue; }
  book.m3u = m3u;
  book.tracks = tracks.map((f) => ({ file: f, sec: seconds(join(audioDir, f)) }));
  book.sec = book.tracks.reduce((a, t) => a + t.sec, 0);
  withAudio.push(book);
}

const total = withAudio.reduce((a, b) => a + b.sec, 0);
const rel = (b, f) => `books/${b.slug}/out/audio/${f}`;
const now = new Date();
const stamp = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16).replace("T", " ");

// Markdown
let md = `# Audio library\n\nGenerated ${stamp} by creative-hub/scripts/audio-library.mjs. ${withAudio.length} published books with audio, ${hms(total)} in all.\n\n| Book | Format | Tracks | Length | Playlist |\n|---|---|---|---|---|\n`;
for (const b of withAudio) md += `| ${b.title} | ${b.format} | ${b.tracks.length} | ${hms(b.sec)} | ${b.m3u ? rel(b, b.m3u) : "-"} |\n`;
md += `\n## Published books without audio (${without.length})\n\n| Book | Format |\n|---|---|\n`;
for (const b of without) md += `| ${b.title} (${b.slug}) | ${b.format} |\n`;
writeFileSync(join(dataDir, "audio-library.md"), md);

// HTML (open it from the data folder; links are relative)
let html = `<!doctype html><html lang="en"><meta charset="utf-8"><title>Audio library</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{color-scheme:light dark;--fg:#1d1d1f;--muted:#6e6e73;--line:#d2d2d7;--bg:#fbfbfa}
@media(prefers-color-scheme:dark){:root{--fg:#f2f2f2;--muted:#a1a1a6;--line:#3a3a3c;--bg:#161617}}
body{font:16px/1.5 system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;color:var(--fg);background:var(--bg)}
h1{margin:0}.sub{color:var(--muted);margin:.2rem 0 1.5rem}
details{border-top:1px solid var(--line);padding:.6rem 0}summary{cursor:pointer;display:flex;gap:1rem;align-items:baseline}
summary b{flex:1}summary span{color:var(--muted);font-size:.9rem;white-space:nowrap}
ol{padding-left:1.5rem}li{margin:.3rem 0}li audio{width:100%;height:32px}
input{width:100%;padding:.5rem;font:inherit;margin-bottom:1rem;border:1px solid var(--line);border-radius:6px;background:transparent;color:inherit}
table{border-collapse:collapse;width:100%}td{border-top:1px solid var(--line);padding:.3rem .5rem;color:var(--muted)}
</style>
<h1>Audio library</h1>
<p class="sub">${withAudio.length} books with audio, ${hms(total)} in all. Generated ${stamp}.</p>
<input id="q" placeholder="Filter by title or format" oninput="for(const d of document.querySelectorAll('details'))d.hidden=!d.dataset.k.includes(this.value.toLowerCase())">
`;
for (const b of withAudio) {
  html += `<details data-k="${esc((b.title + " " + b.format).toLowerCase())}"><summary><b>${esc(b.title)}</b><span>${esc(b.format)}</span><span>${b.tracks.length} tracks · ${hms(b.sec)}</span></summary>`;
  if (b.m3u) html += `<p><a href="${rel(b, b.m3u)}">Playlist (.m3u)</a></p>`;
  html += "<ol>";
  for (const t of b.tracks) html += `<li>${esc(t.file)} <span style="color:var(--muted)">${hms(t.sec)}</span><br><audio controls preload="none" src="${rel(b, t.file)}"></audio></li>`;
  html += "</ol></details>\n";
}
html += `<h2>Published books without audio (${without.length})</h2><table>`;
for (const b of without) html += `<tr><td>${esc(b.title)}</td><td>${esc(b.format)}</td></tr>`;
html += "</table></html>\n";
writeFileSync(join(dataDir, "audio-library.html"), html);

console.log(`${withAudio.length} with audio (${hms(total)}), ${without.length} without; wrote audio-library.md and audio-library.html in ${dataDir}`);

#!/usr/bin/env node
// Probes the running Strata server with the requests the hub's tools send (HUB-26). No dependencies.
//   node scripts/strata-probe.mjs [baseUrl]      default http://127.0.0.1:8080
// Prints PASS / FAIL / INFO per request and exits 1 when any required check fails. Save the output by hand to runs/.

const base = (process.argv[2] || process.env.STRATA_URL || 'http://127.0.0.1:8080').replace(/\/+$/, '');
const key = process.env.STRATA_API_KEY;
let failed = 0;

const report = (state, name, detail = '') => {
  if (state === 'FAIL') failed++;
  console.log(`${state.padEnd(4)}  ${name}${detail ? ` - ${detail}` : ''}`);
};

async function http(path, init = {}, timeoutMs = 120000) {
  const headers = { 'content-type': 'application/json', ...(key ? { authorization: `Bearer ${key}` } : {}) };
  return fetch(base + path, { ...init, headers, signal: AbortSignal.timeout(timeoutMs) });
}

async function getJson(path) {
  const r = await http(path, {}, 10000);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

// POST a streamed chat completion; returns { content, reasoning, usage, toolCalls, model }.
async function chat(extra) {
  const body = {
    model: 'default',
    stream: true,
    stream_options: { include_usage: true },
    max_tokens: 600,
    ...extra,
  };
  const r = await http('/v1/chat/completions', { method: 'POST', body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${(await r.text()).slice(0, 300)}`);
  const out = { content: '', reasoning: '', usage: null, toolCalls: '', model: '' };
  const dec = new TextDecoder();
  let buf = '';
  for await (const chunk of r.body) {
    buf += dec.decode(chunk, { stream: true });
    let i;
    while ((i = buf.indexOf('\n')) >= 0) {
      const line = buf.slice(0, i).trim();
      buf = buf.slice(i + 1);
      if (!line.startsWith('data:')) continue;
      const data = line.slice(5).trim();
      if (!data || data === '[DONE]') continue;
      let j;
      try { j = JSON.parse(data); } catch { continue; }
      if (j.model) out.model = j.model;
      if (j.usage) out.usage = j.usage;
      const d = j.choices?.[0]?.delta;
      if (!d) continue;
      if (d.content) out.content += d.content;
      if (d.reasoning_content) out.reasoning += d.reasoning_content;
      if (d.reasoning) out.reasoning += d.reasoning;
      for (const t of d.tool_calls || []) out.toolCalls += (t.function?.name || '') + (t.function?.arguments || '');
    }
  }
  return out;
}

async function check(name, fn, required = true) {
  try {
    const [ok, detail] = await fn();
    report(ok ? 'PASS' : required ? 'FAIL' : 'INFO', name, detail);
  } catch (e) {
    report(required ? 'FAIL' : 'INFO', name, e?.message || String(e));
  }
}

const short = (s, n = 60) => JSON.stringify(s.length > n ? s.slice(0, n) + '...' : s);

console.log(`Strata probe against ${base}`);

let healthOk = false;
await check('GET /health', async () => {
  const h = await getJson('/health');
  healthOk = true;
  return [h.loaded !== false, `model=${h.model ?? '?'} loaded=${h.loaded}`];
});
if (!healthOk) {
  console.log('Strata is not answering. Start it with: pwsh -File scripts\\hub.ps1 start strata [variant]');
  process.exit(1);
}

await check('GET /v1/status', async () => {
  const s = await getJson('/v1/status');
  const serving = s.concurrency?.serving;
  return [Boolean(s.model) && serving !== undefined, `model=${s.model} concurrency.serving=${serving}`];
});

await check('GET /v1/models', async () => {
  const m = await getJson('/v1/models');
  const first = (m.data || []).find((x) => !x.alias_of);
  const n = first?.meta?.n_ctx;
  return [Boolean(first), `id=${first?.id ?? 'none (model unloaded?)'}${n ? ` n_ctx=${n}` : ''}`];
});

const ask = { messages: [{ role: 'user', content: 'Reply with one short sentence about the sea.' }] };

await check('(a) stream, include_usage, reasoning_effort none', async () => {
  const o = await chat({ ...ask, reasoning_effort: 'none' });
  const ok = o.content.trim().length > 0 && o.reasoning.trim().length === 0;
  return [ok, `answer=${short(o.content)} reasoning_chars=${o.reasoning.length} usage=${o.usage ? 'yes' : 'no'}`];
});

await check('(b) stream, reasoning_effort low', async () => {
  const o = await chat({ ...ask, reasoning_effort: 'low', max_tokens: 1500 });
  return [(o.content + o.reasoning).trim().length > 0, `answer=${short(o.content)} reasoning_chars=${o.reasoning.length}`];
});

await check('(c) JSON-shaped answer without response_format', async () => {
  const o = await chat({
    reasoning_effort: 'none',
    messages: [{ role: 'user', content: 'Return only a JSON object {"colour": "...", "count": N} describing three red apples. No other text.' }],
  });
  const text = o.content.replace(/^\s*```(?:json)?\s*|\s*```\s*$/g, '').trim();
  let parsed = null;
  try { parsed = JSON.parse(text); } catch { /* reported below */ }
  return [parsed !== null && typeof parsed === 'object', `answer=${short(o.content)}`];
});

await check('(d) tool call, one function, reasoning_effort none', async () => {
  const o = await chat({
    reasoning_effort: 'none',
    messages: [{ role: 'user', content: 'Draw a red square with the draw_rect tool at x 1, y 2, size 3.' }],
    tools: [{
      type: 'function',
      function: {
        name: 'draw_rect',
        description: 'Draw a filled square.',
        parameters: {
          type: 'object',
          properties: { x: { type: 'number' }, y: { type: 'number' }, size: { type: 'number' }, colour: { type: 'string' } },
          required: ['x', 'y', 'size'],
        },
      },
    }],
  });
  return [o.toolCalls.includes('draw_rect'), `tool_calls=${short(o.toolCalls, 80)}`];
});

// Informational: whether the profile may set json_schema: true.
await check('(e) response_format json_schema (informational)', async () => {
  const o = await chat({
    reasoning_effort: 'none',
    messages: [{ role: 'user', content: 'Three red apples.' }],
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'fruit',
        strict: true,
        schema: {
          type: 'object',
          properties: { colour: { type: 'string' }, count: { type: 'integer' } },
          required: ['colour', 'count'],
          additionalProperties: false,
        },
      },
    },
  });
  let parsed = null;
  try { parsed = JSON.parse(o.content); } catch { /* informational */ }
  return [parsed !== null && typeof parsed.count === 'number', `answer=${short(o.content)}`];
}, false);

console.log(failed ? `\n${failed} required check(s) FAILED` : '\nAll required checks passed');
process.exit(failed ? 1 : 0);

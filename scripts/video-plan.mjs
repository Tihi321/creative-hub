#!/usr/bin/env node
// The planner of the hub's make-video skill (HUB-11): the parts of a video production that must be exact.
// It reads the output of Scriptorium's get_screenplay and writes the shot plan, the cost estimate, the budget left and the
// flow_assemble timeline into runs/<slug>/video/. No dependencies; Node 24.
//
//   fnm exec --using=24 node scripts/video-plan.mjs <cmd> <run dir> [flags]
//
//   plan <dir> [--budget N] [--model omni-720p|omni-360p|veo-lite|veo-fast|veo-quality] [--aspect 16:9|9:16] [--balance N] [--force]
//        reads <dir>/screenplay.json, writes <dir>/plan.json and prints the dry run (nothing is spent)
//   estimate <dir>             prints the dry run again from plan.json (after hand edits)
//   keyframes <dir>            the flow_generate scenes for the free keyframes (one image per shot)
//   voices <dir>               the flow_narrate calls for every spoken line
//   next <dir> [--retake ID] [--cap N]   the next video shot to make, with its max_credits, or "budget reached"
//   record <dir> <shot id> <json>        stores a result (keyframe, clip, voices) and updates `spent`; id music:m1 for a music cue
//   timeline <dir> [--animatic]          writes <dir>/assemble.json, the flow_assemble arguments

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

// ---- prices -------------------------------------------------------------------------------------------------------------
// Flow credits for one video clip. `seen` = read from Flow's own quote or a measured balance (flow-music-mcp CLAUDE.md, FMM-09),
// `guessed` = worked out pro rata. Update this table when flow-music-mcp measures more.
export const PRICES = {
  'omni-360p': { label: 'Omni 1.1 Flash 360p', menu: 'Omni 1.1 Flash', resolution: '360p', durations: [4, 6, 8, 10], seen: { 4: 4 }, perSecond: 1 },
  'omni-720p': { label: 'Omni 1.1 Flash 720p', menu: 'Omni 1.1 Flash', resolution: '720p', durations: [4, 6, 8, 10], seen: { 4: 7, 8: 12 }, perSecond: 1.25 },
  'veo-lite': { label: 'Veo 3.1 Lite', menu: 'Veo 3.1 - Lite', fixed: 8, seen: { 8: 10 } },
  'veo-fast': { label: 'Veo 3.1 Fast', menu: 'Veo 3.1 - Fast', fixed: 8, seen: { 8: 20 } },
  'veo-quality': { label: 'Veo 3.1 Quality', menu: 'Veo 3.1 - Quality', fixed: 8, seen: { 8: 100 } }
}
// Images (Nano Banana), Gemini and Windows voices and the assembly cost nothing.

export const SHOT_LENGTHS = [4, 6, 8, 10]
export const TITLE_SECONDS = 3
export const WORDS_PER_SECOND = 2.5
export const LINE_LEAD = 0.3 // a line starts this long after its shot starts
export const LINE_GAP = 0.25 // between two lines of one shot
export const RESERVE = 0.25 // the retake reserve of the dry run
export const CAP_FACTOR = 1.25 // max_credits = estimate x this, at most
export const DEFAULT_BUDGET = 150
export const DEFAULT_CAP = 50 // FLOW_MUSIC_MCP_MAX_CREDITS when unset
export const CLIP_VOLUME = 0.3

/** The clip length asked from Flow for a shot of `seconds` (Veo clips are always 8 s). */
export function clipSeconds(model, seconds) {
  const p = PRICES[model]
  if (!p) throw new Error(`unknown model "${model}" (one of ${Object.keys(PRICES).join(', ')})`)
  return p.fixed ?? seconds
}

/** { credits, status } for one clip of `seconds` with `model`: `seen` when Flow quoted that length, else `guessed`. */
export function price(model, seconds) {
  const p = PRICES[model]
  if (!p) throw new Error(`unknown model "${model}" (one of ${Object.keys(PRICES).join(', ')})`)
  const s = clipSeconds(model, seconds)
  if (p.seen[s] !== undefined) return { credits: p.seen[s], status: 'seen' }
  // pro rata from the nearest seen length (omni), rounded up
  const [from, credits] = Object.entries(p.seen).map(([k, v]) => [Number(k), v]).sort((a, b) => Math.abs(a[0] - s) - Math.abs(b[0] - s))[0]
  const per = p.perSecond ?? credits / from
  return { credits: Math.ceil(credits + (s - from) * per), status: 'guessed' }
}

// ---- seconds ------------------------------------------------------------------------------------------------------------
const wordCount = (s) => (String(s).match(/[\p{L}\p{N}'’-]+/gu) ?? []).length
const lineSeconds = (line) => line.seconds ?? Math.max(0.6, wordCount(line.text) / WORDS_PER_SECOND)

/** The seconds a shot's spoken lines need: a lead-in, each line at 2.5 words a second, a gap between lines. */
export function speechNeed(lines) {
  if (!lines.length) return 0
  return LINE_LEAD + lines.reduce((n, l) => n + wordCount(l.text) / WORDS_PER_SECOND, 0) + LINE_GAP * (lines.length - 1)
}

/** The shot length used: the writer's, raised to the next of 4, 6, 8 and 10 that holds its lines. */
export function fitSeconds(seconds, lines) {
  const want = Math.max(seconds || 0, speechNeed(lines))
  return SHOT_LENGTHS.find((s) => s >= want - 1e-9) ?? SHOT_LENGTHS.at(-1)
}

// ---- voices -------------------------------------------------------------------------------------------------------------
// Gemini voices (flow_voices): name, gender and a few words, in the order they are given out.
export const VOICES = [
  { name: 'Charon', gender: 'm', tags: ['informative', 'narrator', 'calm', 'deep', 'old', 'elderly'] },
  { name: 'Aoede', gender: 'f', tags: ['breezy', 'light', 'young', 'cheerful'] },
  { name: 'Gacrux', gender: 'f', tags: ['mature', 'old', 'elderly', 'warm', 'grandmother', 'slow'] },
  { name: 'Puck', gender: 'm', tags: ['upbeat', 'young', 'boy', 'cheerful', 'quick', 'grinning'] },
  { name: 'Kore', gender: 'f', tags: ['firm', 'stubborn', 'brave', 'dry', 'strong'] },
  { name: 'Fenrir', gender: 'm', tags: ['excitable', 'loud', 'rough', 'quick'] },
  { name: 'Leda', gender: 'f', tags: ['youthful', 'young', 'girl', 'child', 'teen', 'worried'] },
  { name: 'Orus', gender: 'm', tags: ['firm', 'gruff', 'stern', 'low'] },
  { name: 'Algenib', gender: 'm', tags: ['gravelly', 'rough', 'old', 'gruff', 'low'] },
  { name: 'Sulafat', gender: 'f', tags: ['warm', 'kind', 'gentle'] },
  { name: 'Achird', gender: 'm', tags: ['friendly', 'warm', 'kind'] },
  { name: 'Zephyr', gender: 'f', tags: ['bright', 'clear'] },
  { name: 'Umbriel', gender: 'm', tags: ['easy', 'relaxed', 'casual'] },
  { name: 'Vindemiatrix', gender: 'f', tags: ['gentle', 'soft'] },
  { name: 'Iapetus', gender: 'm', tags: ['clear'] },
  { name: 'Erinome', gender: 'f', tags: ['clear'] }
]
export const NARRATOR_VOICE = 'Charon'

const FEMALE = /\b(she|her|woman|women|girl|mother|mum|mom|grandmother|granny|aunt|sister|daughter|wife|queen|lady|female|hers)\b/i
const MALE = /\b(he|his|him|man|men|boy|father|dad|grandfather|uncle|brother|son|husband|king|male)\b/i

/** The gender a character's looks and voice note say: 'f', 'm' or null. The first of the words that comes first wins. */
export function genderOf(text) {
  const f = FEMALE.exec(text)
  const m = MALE.exec(text)
  if (f && (!m || f.index <= m.index)) return 'f'
  if (m) return 'm'
  return null
}

/** One voice per character from the bible's voice note and looks: the right gender, the most matching words, never the same voice twice while others are left. The narrator keeps Charon. */
export function assignVoices(characters, speakers = []) {
  const used = new Set([NARRATOR_VOICE])
  const out = { Narrator: { voice: NARRATOR_VOICE, note: 'narrator' } }
  const names = [...new Set([...characters.map((c) => c.name), ...speakers])].filter((n) => n && !/^narrator$/i.test(n))
  for (const name of names) {
    const c = characters.find((x) => x.name === name) ?? { name, looks: '', voice: '' }
    const note = `${c.voice ?? ''}`
    const gender = genderOf(note) ?? genderOf(c.looks ?? '') ?? 'm'
    const words = `${note} ${c.looks ?? ''}`.toLowerCase()
    const score = (v) => (v.gender === gender ? 100 : 0) + v.tags.filter((t) => words.includes(t)).length * 10 - (used.has(v.name) ? 1000 : 0)
    const best = [...VOICES].map((v, i) => ({ v, i, s: score(v) })).sort((a, b) => b.s - a.s || a.i - b.i)[0].v
    used.add(best.name)
    out[name] = { voice: best.name, note: note || c.looks || '' }
  }
  return out
}

// ---- the plan -----------------------------------------------------------------------------------------------------------
const cap = (s) => String(s).replace(/\s+/g, ' ').trim()
const sentence = (s) => cap(s).replace(/[.!?]*$/, '.')

function keyframePrompt(film, scene, shot, looks) {
  const place = film.places.find((p) => p.name.toLowerCase() === String(scene.place).toLowerCase())
  const who = shot.cast.map((c) => `${c.name} (${cap(c.look || looks.get(c.name) || '')})`.replace(/ \(\)/, ''))
  const bits = [
    `${cap(film.style || '')}`.replace(/^$/, ''),
    shot.title ? `Title card with the words "${shot.title}", ${cap(scene.background || '')}` : `${shot.framing} shot${shot.move && shot.move !== 'static' ? `, ${shot.move}` : ''}: ${cap(shot.action)}`,
    place ? `Place: ${scene.place}, ${cap(scene.time)}. ${cap(place.looks)}` : scene.place ? `Place: ${scene.place}, ${cap(scene.time)}.` : '',
    who.length ? `In frame: ${who.join('; ')}.` : '',
    shot.title ? 'The title is the only text.' : 'No text, no captions, no watermark.'
  ]
  return bits.filter(Boolean).map((b) => (/[.!?"]$/.test(b) ? b : `${b}.`)).join(' ')
}

function videoPrompt(shot) {
  const sound = shot.sfx.length ? `ambient sound only: ${shot.sfx.join(', ')}` : 'ambient sound only'
  return `${sentence(shot.action)} Camera: ${shot.framing}${shot.move && shot.move !== 'static' ? `, ${shot.move}` : ', static'}. No speech, ${sound}.`
}

/** The plan of a film from a get_screenplay result: pure, no files. Returns { plan, warnings }. */
export function buildPlan(film, opts = {}) {
  const model = opts.model ?? 'omni-720p'
  if (!PRICES[model]) throw new Error(`unknown model "${model}" (one of ${Object.keys(PRICES).join(', ')})`)
  const aspect = opts.aspect ?? film.aspect ?? '16:9'
  if (!['16:9', '9:16'].includes(aspect)) throw new Error(`aspect must be 16:9 or 9:16, not ${aspect}`)
  const warnings = []
  const looks = new Map(film.characters.map((c) => [c.name, c.looks]))
  const speakers = film.chapters.flatMap((c) => c.scenes.flatMap((s) => s.shots.flatMap((sh) => sh.lines.map((l) => l.speaker))))
  const voices = assignVoices(film.characters, speakers)
  const shots = []
  for (const ch of film.chapters) {
    for (const scene of ch.scenes) {
      for (const sh of scene.shots) {
        const isTitle = !!sh.title
        const seconds = isTitle ? TITLE_SECONDS : fitSeconds(sh.seconds, sh.lines)
        const clip = isTitle ? 0 : clipSeconds(model, seconds)
        const play = isTitle ? TITLE_SECONDS : Math.min(seconds, clip)
        if (!isTitle && speechNeed(sh.lines) > Math.min(10, play) + 1e-9) warnings.push(`${sh.id}: dialogue is longer than its shot (${speechNeed(sh.lines).toFixed(1)} s of speech in ${play} s): the lines are sped up or cut`)
        if (!isTitle && seconds > clip) warnings.push(`${sh.id}: ${PRICES[model].label} clips are ${clip} s: the shot of ${seconds} s is cut to ${clip} s`)
        if (sh.cast.length > 3) warnings.push(`${sh.id}: ${sh.cast.length} people in a shot: only the first 3 are used as references`)
        if (sh.continuous) warnings.push(`${sh.id}: continuous shot is made as a normal keyframe shot (D11)`)
        const est = isTitle ? { credits: 0, status: 'seen' } : price(model, seconds)
        shots.push({
          id: sh.id,
          scene: scene.id,
          place: scene.place,
          kind: isTitle ? 'title' : 'video',
          seconds: play,
          writerSeconds: sh.seconds,
          clipSeconds: clip,
          framing: sh.framing,
          move: sh.move,
          continuous: !!sh.continuous,
          action: sh.action,
          cast: sh.cast,
          refs: sh.cast.map((c) => c.name).slice(0, 3),
          sfx: sh.sfx,
          title: sh.title,
          lines: sh.lines.map((l) => ({ speaker: l.speaker, delivery: l.delivery, text: l.text, kind: l.kind })),
          keyframePrompt: keyframePrompt(film, scene, sh, looks),
          videoPrompt: isTitle ? '' : videoPrompt(sh),
          estimate: est,
          result: {}
        })
      }
    }
  }
  const runtime = shots.reduce((n, s) => n + s.seconds, 0)
  if (film.runtimeRange && (runtime < film.runtimeRange[0] || runtime > film.runtimeRange[1])) warnings.push(`runtime ${runtime} s is outside the format's range ${film.runtimeRange[0]} to ${film.runtimeRange[1]} s`)
  const plan = {
    slug: film.slug,
    title: film.title,
    format: film.format,
    aspect,
    style: film.style ?? '',
    model,
    budget: { credits: opts.budget ?? DEFAULT_BUDGET, spent: 0 },
    ...(opts.balance !== undefined ? { balance: opts.balance } : {}),
    runtimeSeconds: runtime,
    characters: film.characters,
    places: film.places,
    voices,
    shots,
    music: film.music.map((m) => ({ ...m, file: null, credits: 0 })),
    warnings
  }
  return { plan, warnings }
}

// ---- estimate -----------------------------------------------------------------------------------------------------------
/** The money of a plan: the video credits, the retake reserve, what is spent and left. */
export function totals(plan) {
  const videos = plan.shots.filter((s) => s.kind === 'video')
  const credits = videos.reduce((n, s) => n + s.estimate.credits, 0)
  const reserve = Math.ceil(credits * RESERVE)
  const spent = spentOf(plan)
  return { shots: plan.shots.length, videoShots: videos.length, credits, reserve, withReserve: credits + reserve, spent, left: plan.budget.credits - spent, guessed: videos.filter((s) => s.estimate.status === 'guessed').length }
}

/** Credits spent so far: every recorded clip and music take (recomputed, so recording twice never counts twice). */
export function spentOf(plan) {
  const clips = plan.shots.reduce((n, s) => n + (s.result.clips ?? []).reduce((m, c) => m + (c.credits ?? 0), 0), 0)
  const music = plan.music.reduce((n, m) => n + (m.credits ?? 0), 0)
  return clips + music
}

/** The dry run as text. */
export function dryRun(plan) {
  const t = totals(plan)
  const m = PRICES[plan.model]
  const lines = [
    `${plan.title} (${plan.slug}): ${plan.format}, ${plan.aspect}, ${plan.runtimeSeconds} s, ${t.shots} shots (${t.videoShots} video clips) with ${m.label}`,
    ''
  ]
  for (const s of plan.shots) {
    const speech = s.lines.length ? `, ${s.lines.length} line(s)` : ''
    lines.push(`  ${s.id}  ${String(s.seconds).padStart(2)} s  ${s.kind === 'title' ? 'title card' : `${s.framing}, ${s.move}`}${speech}  ${s.kind === 'title' ? 'free' : `${s.estimate.credits} credits (${s.estimate.status})`}`)
  }
  lines.push(
    '',
    `Video credits: ${t.credits}${t.guessed ? ` (${t.guessed} clip(s) priced pro rata, not quoted by Flow)` : ''}`,
    `Retake reserve (${RESERVE * 100}%): ${t.reserve}  ->  ${t.withReserve} with the reserve`,
    `Budget: ${plan.budget.credits}, spent ${t.spent}, left ${t.left}. ${t.withReserve <= plan.budget.credits ? 'Fits with the reserve.' : t.credits <= plan.budget.credits ? 'Fits, but without the full reserve.' : 'DOES NOT FIT: shorten the film, use a cheaper model or raise the budget.'}`,
    plan.balance !== undefined ? `Last known balance: ${plan.balance} credits` : 'Last known balance: unknown (flow_status shows it)',
    `Music: ${plan.music.length} cue(s)${plan.music.length ? ` (${plan.music.map((x) => x.id).join(', ')}), each song costs credits and is asked first` : ''}. Images, voices and the assembly are free.`
  )
  if (plan.warnings.length) lines.push('', 'Warnings:', ...plan.warnings.map((w) => `  - ${w}`))
  return lines.join('\n')
}

// ---- next ---------------------------------------------------------------------------------------------------------------
/** The next video shot to make, with the flow_generate scene and its max_credits (D10): min(ceil(estimate x 1.25), budget left, the per-call cap). */
export function nextShot(plan, opts = {}) {
  const callCap = opts.cap ?? DEFAULT_CAP
  const left = plan.budget.credits - spentOf(plan)
  let shot
  if (opts.retake) {
    shot = plan.shots.find((s) => s.id === opts.retake)
    if (!shot) throw new Error(`no shot ${opts.retake}`)
    if ((shot.result.clips ?? []).length >= 2) return { done: false, refused: `${shot.id} already has a retake: one retake per shot at most` }
  } else shot = plan.shots.find((s) => s.kind === 'video' && !(s.result.clips ?? []).length)
  if (!shot) return { done: true }
  const max = Math.min(Math.ceil(shot.estimate.credits * CAP_FACTOR), left, callCap)
  if (max < shot.estimate.credits) return { budgetReached: true, shot: shot.id, estimate: shot.estimate.credits, left, message: `budget reached: ${shot.id} needs about ${shot.estimate.credits} credits, ${left} left of ${plan.budget.credits}${callCap < shot.estimate.credits ? ` (per-call cap ${callCap})` : ''}. Stop and ask the user.` }
  const m = PRICES[plan.model]
  const kf = shot.result.keyframe
  const scene = {
    prompt: shot.videoPrompt,
    type: 'video',
    model: m.menu,
    aspect_ratio: plan.aspect,
    ...(m.fixed ? {} : { duration: shot.clipSeconds, resolution: m.resolution }),
    max_credits: max,
    ...(kf?.media_id ? { first_frame: `asset:${kf.media_id}` } : {})
  }
  return { shot: shot.id, seconds: shot.seconds, estimate: shot.estimate, max_credits: max, left, ...(kf?.media_id ? {} : { missing: ['keyframe (record the keyframe media id first)'] }), flow_generate_scene: scene }
}

// ---- keyframes and voices -----------------------------------------------------------------------------------------------
/** The flow_generate scenes for the keyframes (images are free): one per shot, the shot's characters as references. */
export function keyframeScenes(plan) {
  return plan.shots.map((s) => ({
    shot: s.id,
    prompt: s.keyframePrompt,
    type: 'image',
    aspect_ratio: plan.aspect,
    ...(s.refs.length && !s.title ? { reference_images: s.refs.map((n) => `asset:${n}`) } : {}),
    max_credits: 0
  }))
}

/** The flow_narrate calls for every spoken line (free: Gemini). */
export function voiceCalls(plan) {
  return plan.shots.flatMap((s) =>
    s.lines.map((l, i) => {
      const v = plan.voices[l.speaker] ?? plan.voices[l.speaker?.replace(/\b\w/g, (c) => c.toUpperCase())] ?? { voice: NARRATOR_VOICE }
      const how = [l.kind === 'voice-over' ? 'as a voice-over narrator' : '', l.delivery ? `say it ${l.delivery}` : ''].filter(Boolean).join(', ')
      return { shot: s.id, line: i, name: `${s.id}-l${i + 1}`, engine: 'gemini', voice: v.voice, format: 'wav', text: l.text, ...(how ? { style: how } : {}) }
    })
  )
}

// ---- record -------------------------------------------------------------------------------------------------------------
/** Stores a result. `music:<id>` records a music cue ({file, credits}). Recording the same clip file twice changes nothing. */
export function recordResult(plan, id, data) {
  if (id.startsWith('music:')) {
    const cue = plan.music.find((m) => m.id === id.slice(6))
    if (!cue) throw new Error(`no music cue ${id.slice(6)}`)
    if (data.file !== undefined) cue.file = data.file
    if (data.credits !== undefined) cue.credits = data.credits
  } else {
    const shot = plan.shots.find((s) => s.id === id)
    if (!shot) throw new Error(`no shot ${id}`)
    if (data.keyframe) shot.result.keyframe = { ...shot.result.keyframe, ...data.keyframe }
    if (data.clip) {
      const clips = (shot.result.clips ??= [])
      const at = clips.findIndex((c) => c.file === data.clip.file)
      if (at >= 0) clips[at] = { ...clips[at], ...data.clip }
      else clips.push({ file: data.clip.file, credits: data.clip.credits ?? 0 })
      if (clips.length > 2) throw new Error(`${id}: more than one retake (${clips.length} clips)`)
    }
    if (data.voices) shot.result.voices = data.voices.map((v) => (typeof v === 'string' ? { file: v } : v))
  }
  plan.budget.spent = spentOf(plan)
  return plan
}

// ---- timeline -----------------------------------------------------------------------------------------------------------
const round = (n) => Math.round(n * 1000) / 1000

/** The seconds of an audio file by ffprobe, or null when ffprobe or the file is not there. */
export function probeSeconds(file) {
  if (!file || !existsSync(file)) return null
  const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', file], { encoding: 'utf8' })
  const n = Number(r.stdout?.trim())
  return r.status === 0 && Number.isFinite(n) && n > 0 ? n : null
}

/**
 * The flow_assemble arguments: clips in order (the keyframe stills for an animatic, the trimmed video clips otherwise, title cards as stills),
 * voice_lines (a line starts 0.3 s into its shot, the next 0.25 s after the last one ends), music_cues from the cues' shot ranges, clip volume 0.3, ducking.
 * `probe(file)` gives the length of a voice file (default ffprobe); without it a line lasts words / 2.5 s.
 */
export function buildTimeline(plan, opts = {}) {
  const animatic = !!opts.animatic
  const probe = opts.probe ?? probeSeconds
  const warnings = []
  const clips = []
  const voice_lines = []
  const starts = new Map()
  let t = 0
  for (const s of plan.shots) {
    starts.set(s.id, { at: t, end: t + s.seconds })
    const kf = s.result.keyframe?.file
    const clip = (s.result.clips ?? []).at(-1)?.file
    if (s.kind === 'title' || animatic) {
      if (!kf) throw new Error(`${s.id}: no keyframe file recorded (record the keyframe first)`)
      clips.push({ image: path.resolve(kf), seconds: s.seconds, ...(s.kind === 'title' ? {} : { zoom: true }) })
    } else if (clip) clips.push({ file: path.resolve(clip), from: 0, to: s.seconds })
    else if (kf) {
      warnings.push(`${s.id}: no video clip yet: its keyframe is held instead`)
      clips.push({ image: path.resolve(kf), seconds: s.seconds, zoom: true })
    } else throw new Error(`${s.id}: neither a clip nor a keyframe is recorded`)
    let at = t + LINE_LEAD
    s.lines.forEach((l, i) => {
      const rec = (s.result.voices ?? [])[i]
      if (!rec?.file) {
        warnings.push(`${s.id}: line ${i + 1} (${l.speaker}) has no voice file: left out`)
        return
      }
      const seconds = rec.seconds ?? probe(rec.file) ?? lineSeconds(l)
      voice_lines.push({ file: path.resolve(rec.file), at: round(at), max_seconds: round(Math.max(0.2, t + s.seconds - at - 0.1)) })
      at += seconds + LINE_GAP
      if (at - LINE_GAP > t + s.seconds + 0.5) warnings.push(`${s.id}: its lines end ${round(at - LINE_GAP - t - s.seconds)} s after the shot (they are sped up to fit, at most 1.25x)`)
    })
    t += s.seconds
  }
  const music_cues = []
  for (const m of plan.music) {
    if (!m.file) continue
    const from = starts.get(m.from)
    const to = starts.get(m.to)
    if (!from || !to) {
      warnings.push(`music ${m.id}: unknown shot range ${m.from} to ${m.to}`)
      continue
    }
    music_cues.push({ file: path.resolve(m.file), at: round(from.at), until: round(to.end) })
  }
  const args = {
    out: path.resolve(opts.dir ?? '.', 'out'),
    clips,
    ...(music_cues.length ? { music_cues } : {}),
    ...(voice_lines.length ? { voice_lines } : {}),
    clip_volume: CLIP_VOLUME,
    duck: true,
    output_name: animatic ? 'animatic' : 'final'
  }
  return { args, warnings, runtimeSeconds: round(t) }
}

// ---- files and the command line -----------------------------------------------------------------------------------------
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'))
const writeJson = (file, data) => writeFileSync(file, JSON.stringify(data, null, 2) + '\n')
const planFile = (dir) => path.join(dir, 'plan.json')
const loadPlan = (dir) => {
  if (!existsSync(planFile(dir))) throw new Error(`no plan.json in ${dir}: run "plan" first`)
  return readJson(planFile(dir))
}

function flags(argv) {
  const out = { _: [] }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith('--')) {
      const k = a.slice(2)
      if (['animatic', 'force'].includes(k)) out[k] = true
      else out[k] = argv[++i]
    } else out._.push(a)
  }
  return out
}

export function main(argv, log = console.log) {
  const f = flags(argv)
  const [cmd, dir, ...rest] = f._
  if (!cmd || !dir) {
    log('usage: node scripts/video-plan.mjs <plan|estimate|keyframes|voices|next|record|timeline> <run dir> [flags]  (see the top of this file)')
    return 2
  }
  if (cmd === 'plan') {
    const src = path.join(dir, 'screenplay.json')
    if (!existsSync(src)) throw new Error(`no screenplay.json in ${dir}: save the get_screenplay result there first`)
    if (existsSync(planFile(dir)) && !f.force) throw new Error(`${planFile(dir)} exists: "plan --force" replaces it and forgets every recorded result`)
    const { plan } = buildPlan(readJson(src), {
      budget: f.budget !== undefined ? Number(f.budget) : undefined,
      model: f.model,
      aspect: f.aspect,
      balance: f.balance !== undefined ? Number(f.balance) : undefined
    })
    mkdirSync(dir, { recursive: true })
    writeJson(planFile(dir), plan)
    log(dryRun(plan))
  } else if (cmd === 'estimate') log(dryRun(loadPlan(dir)))
  else if (cmd === 'keyframes') log(JSON.stringify(keyframeScenes(loadPlan(dir)), null, 2))
  else if (cmd === 'voices') log(JSON.stringify(voiceCalls(loadPlan(dir)), null, 2))
  else if (cmd === 'next') {
    const r = nextShot(loadPlan(dir), { retake: f.retake, cap: f.cap !== undefined ? Number(f.cap) : Number(process.env.FLOW_MUSIC_MCP_MAX_CREDITS) || undefined })
    log(r.done ? 'done: every video shot has a clip' : r.message ?? JSON.stringify(r, null, 2))
  } else if (cmd === 'record') {
    const [id, json] = rest
    if (!id || !json) throw new Error('usage: record <dir> <shot id> <json>  (the json may be @file.json)')
    const plan = recordResult(loadPlan(dir), id, json.startsWith('@') ? readJson(json.slice(1)) : JSON.parse(json))
    writeJson(planFile(dir), plan)
    const t = totals(plan)
    log(`recorded ${id}: spent ${t.spent} of ${plan.budget.credits}, left ${t.left}`)
  } else if (cmd === 'timeline') {
    const r = buildTimeline(loadPlan(dir), { animatic: f.animatic, dir })
    writeJson(path.join(dir, 'assemble.json'), r.args)
    log(`${path.join(dir, 'assemble.json')}: ${r.args.clips.length} clips, ${r.runtimeSeconds} s, ${r.args.voice_lines?.length ?? 0} voice lines, ${r.args.music_cues?.length ?? 0} music cues (${r.args.output_name})`)
    for (const w of r.warnings) log(`  warning: ${w}`)
  } else throw new Error(`unknown command "${cmd}"`)
  return 0
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.exitCode = main(process.argv.slice(2))
  } catch (err) {
    console.error(`video-plan: ${err.message}`)
    process.exitCode = 1
  }
}

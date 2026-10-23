// node --test scripts/
import test from 'node:test'
import assert from 'node:assert/strict'
import { mkdtempSync, readFileSync, writeFileSync, copyFileSync, rmSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PRICES, assignVoices, buildPlan, buildTimeline, dryRun, fitSeconds, keyframeScenes, main, nextShot, price, recordResult, spentOf, speechNeed, totals, voiceCalls } from './video-plan.mjs'

const here = path.dirname(fileURLToPath(import.meta.url))
const film = () => JSON.parse(readFileSync(path.join(here, 'fixtures', 'screenplay-harbour.json'), 'utf8'))
const words = (n) => Array.from({ length: n }, () => 'word').join(' ')

test('shot lengths: the writer length, raised to the next of 4, 6, 8, 10 that holds the lines', () => {
  assert.equal(fitSeconds(4, []), 4)
  assert.equal(fitSeconds(5, []), 6)
  assert.equal(fitSeconds(4, [{ text: words(9) }]), 4) // 0.3 + 3.6 s of speech fits
  assert.equal(fitSeconds(4, [{ text: words(10) }]), 6) // 0.3 + 4 s does not
  assert.equal(fitSeconds(4, [{ text: words(20) }]), 10)
  assert.equal(fitSeconds(4, [{ text: words(60) }]), 10) // capped; the plan warns
  assert.ok(speechNeed([{ text: words(5) }, { text: words(5) }]) > speechNeed([{ text: words(10) }]))
})

test('the estimate: seen prices for 4 s and 8 s, pro rata and marked guessed otherwise', () => {
  assert.deepEqual(price('omni-360p', 4), { credits: 4, status: 'seen' })
  assert.deepEqual(price('omni-720p', 4), { credits: 7, status: 'seen' })
  assert.deepEqual(price('omni-720p', 8), { credits: 12, status: 'seen' })
  assert.deepEqual(price('omni-360p', 6), { credits: 6, status: 'guessed' })
  assert.deepEqual(price('omni-720p', 6), { credits: 10, status: 'seen' })
  assert.deepEqual(price('omni-720p', 10), { credits: 15, status: 'seen' })
  assert.deepEqual(price('veo-lite', 4), { credits: 10, status: 'seen' }) // Veo clips are 8 s whatever is asked
  assert.equal(price('veo-fast', 8).credits, 20)
  assert.equal(price('veo-quality', 8).credits, 100)
  assert.throws(() => price('nope', 4), /unknown model/)
})

test('the plan of the harbour fixture: shots, title card, totals, retake reserve, warnings', () => {
  const { plan } = buildPlan(film(), { model: 'omni-360p', budget: 150 })
  assert.deepEqual(plan.shots.map((s) => [s.id, s.kind, s.seconds]), [
    ['ch01.s01.sh01', 'video', 6],
    ['ch01.s01.sh02', 'video', 6], // 10 words and a lead-in need 4.3 s: raised from 4 to 6
    ['ch01.s01.sh03', 'video', 6],
    ['ch01.s01.sh04', 'title', 3]
  ])
  assert.deepEqual(plan.shots.map((s) => s.estimate.credits), [6, 6, 6, 0])
  const t = totals(plan)
  assert.equal(t.credits, 18)
  assert.equal(t.reserve, 5) // 25% of 18, rounded up
  assert.equal(t.withReserve, 23)
  assert.equal(plan.runtimeSeconds, 21)
  assert.equal(plan.budget.spent, 0)
  // 720p costs more
  assert.equal(totals(buildPlan(film(), { model: 'omni-720p' }).plan).credits, 10 + 10 + 10)
  // the runtime of 19 s is outside the 60 to 180 s range: a warning
  assert.ok(plan.warnings.some((w) => /runtime 21 s is outside/.test(w)))
  assert.match(dryRun(plan), /Video credits: 18/)
  assert.match(dryRun(plan), /Fits with the reserve/)
  assert.match(dryRun(buildPlan(film(), { budget: 5 }).plan), /DOES NOT FIT/)
})

test('a shot whose lines do not fit is raised, a long one is warned about, more than 3 people are cut to 3 references, continuous is noted', () => {
  const f = film()
  const shot = f.chapters[0].scenes[0].shots[1]
  shot.lines = [{ speaker: 'Mara', delivery: '', text: words(70), kind: 'dialogue' }]
  shot.cast = ['A', 'B', 'C', 'Mara'].map((name) => ({ name, look: 'x' }))
  shot.continuous = true
  const { plan, warnings } = buildPlan(f, { model: 'omni-360p' })
  const s = plan.shots[1]
  assert.equal(s.seconds, 10)
  assert.deepEqual(s.refs, ['A', 'B', 'C'])
  assert.ok(warnings.some((w) => /sh02: dialogue is longer than its shot/.test(w)))
  assert.ok(warnings.some((w) => /sh02: 4 people in a shot/.test(w)))
  assert.ok(warnings.some((w) => /sh02: continuous shot is made as a normal/.test(w)))
  // Veo clips are 8 s: a 10 s shot is cut
  assert.ok(buildPlan(f, { model: 'veo-lite' }).warnings.some((w) => /sh02: Veo 3.1 Lite clips are 8 s/.test(w)))
})

test('prompts: keyframe has style, place, cast looks and no text; video has no speech and the sfx', () => {
  const { plan } = buildPlan(film())
  const s = plan.shots[1]
  assert.match(s.keyframePrompt, /Moody, rain-soaked/)
  assert.match(s.keyframePrompt, /The harbour wall, dusk/)
  assert.match(s.keyframePrompt, /Mara \(soaked yellow raincoat, worried\)/)
  assert.match(s.keyframePrompt, /No text, no captions/)
  assert.match(s.videoPrompt, /No speech, ambient sound only: wind, rain on oilskin\./)
  assert.match(plan.shots[3].keyframePrompt, /Title card with the words "The End"/)
  const kf = keyframeScenes(plan)
  assert.deepEqual(kf[2].reference_images, ['asset:Mara', 'asset:Tomas'])
  assert.equal(kf[0].reference_images, undefined)
  assert.ok(kf.every((k) => k.type === 'image' && k.max_credits === 0 && k.aspect_ratio === '16:9'))
})

test('voices: the narrator keeps Charon, a girl and a boy get different voices of their gender', () => {
  const v = assignVoices(film().characters, ['Narrator', 'Mara', 'Tomas'])
  assert.equal(v.Narrator.voice, 'Charon')
    assert.notEqual(v.Mara.voice, v.Tomas.voice)
  assert.ok(['Aoede', 'Gacrux', 'Kore', 'Leda', 'Sulafat', 'Zephyr', 'Vindemiatrix', 'Erinome'].includes(v.Mara.voice), v.Mara.voice)
  assert.ok(['Puck', 'Fenrir', 'Orus', 'Algenib', 'Achird', 'Umbriel', 'Iapetus'].includes(v.Tomas.voice), v.Tomas.voice)
  const { plan } = buildPlan(film())
  const calls = voiceCalls(plan)
  assert.equal(calls.length, 4)
  assert.deepEqual(calls[0], { shot: 'ch01.s01.sh01', line: 0, name: 'ch01.s01.sh01-l1', engine: 'gemini', voice: 'Charon', format: 'wav', text: 'Every evening, Mara waited for the last boat.', style: 'as a voice-over narrator' })
  assert.equal(calls[1].voice, plan.voices.Mara.voice)
  assert.equal(calls[1].style, 'say it worried')
})

test('next: the first shot without a clip, max_credits = min(ceil(estimate x 1.25), budget left, cap), and budget reached when it does not fit', () => {
  const { plan } = buildPlan(film(), { model: 'omni-360p', budget: 10 })
  let n = nextShot(plan)
  assert.equal(n.shot, 'ch01.s01.sh01')
  assert.equal(n.estimate.credits, 6)
  assert.equal(n.max_credits, 8) // ceil(7.5)
  assert.deepEqual(n.missing, ['keyframe (record the keyframe media id first)'])
  assert.equal(n.flow_generate_scene.model, 'Omni 1.1 Flash')
  assert.equal(n.flow_generate_scene.duration, 6)
  assert.equal(n.flow_generate_scene.resolution, '360p')
  assert.equal(n.flow_generate_scene.first_frame, undefined)
  // the keyframe is used as the first frame
  recordResult(plan, 'ch01.s01.sh01', { keyframe: { media_id: 'abc-123', file: 'C:/k/1.png' } })
  assert.equal(nextShot(plan).flow_generate_scene.first_frame, 'asset:abc-123')
  assert.equal(nextShot(plan).missing, undefined)
  // the per-call cap and the budget left lower it
  assert.equal(nextShot(plan, { cap: 6 }).max_credits, 6)
  recordResult(plan, 'ch01.s01.sh01', { clip: { file: 'C:/c/1.mp4', credits: 6 } })
  n = nextShot(plan)
  assert.equal(n.shot, 'ch01.s01.sh02')
  assert.equal(n.budgetReached, true) // 4 credits left, the shot costs 6
  assert.match(n.message, /budget reached: ch01.s01.sh02 needs about 6 credits, 4 left of 10/)
  // with a bigger budget the cap is the budget left
  const { plan: p2 } = buildPlan(film(), { model: 'omni-360p', budget: 12 })
  recordResult(p2, 'ch01.s01.sh01', { clip: { file: 'C:/c/1.mp4', credits: 6 } })
  assert.equal(nextShot(p2).max_credits, 6) // ceil(7.5) = 8, but 6 left
  // Veo has no duration and resolution
  const veo = nextShot(buildPlan(film(), { model: 'veo-lite' }).plan).flow_generate_scene
  assert.equal(veo.model, 'Veo 3.1 - Lite')
  assert.equal(veo.duration, undefined)
  assert.equal(veo.resolution, undefined)
})

test('next: done when every video shot has a clip; one retake per shot at most', () => {
  const { plan } = buildPlan(film(), { model: 'omni-360p', budget: 150 })
  for (const [i, s] of plan.shots.filter((x) => x.kind === 'video').entries()) recordResult(plan, s.id, { clip: { file: `C:/c/${i}.mp4`, credits: s.estimate.credits } })
  assert.deepEqual(nextShot(plan), { done: true })
  const retake = nextShot(plan, { retake: 'ch01.s01.sh02' })
  assert.equal(retake.shot, 'ch01.s01.sh02')
  recordResult(plan, 'ch01.s01.sh02', { clip: { file: 'C:/c/2b.mp4', credits: 4 } })
  assert.match(nextShot(plan, { retake: 'ch01.s01.sh02' }).refused, /one retake per shot/)
  assert.throws(() => recordResult(plan, 'ch01.s01.sh02', { clip: { file: 'C:/c/2c.mp4', credits: 4 } }), /more than one retake/)
})

test('record: adds to spent, and the same shot and file twice counts once', () => {
  const { plan } = buildPlan(film(), { model: 'omni-360p' })
  recordResult(plan, 'ch01.s01.sh01', { clip: { file: 'C:/c/1.mp4', credits: 6 } })
  assert.equal(plan.budget.spent, 6)
  recordResult(plan, 'ch01.s01.sh01', { clip: { file: 'C:/c/1.mp4', credits: 6 } })
  assert.equal(plan.budget.spent, 6)
  recordResult(plan, 'ch01.s01.sh02', { clip: { file: 'C:/c/2.mp4', credits: 5 } })
  assert.equal(plan.budget.spent, 11)
  recordResult(plan, 'music:m1', { file: 'C:/m/m1.wav', credits: 5 })
  assert.equal(spentOf(plan), 11) // Flow Music credits are a separate balance
  assert.equal(plan.budget.spent, 11)
  assert.equal(plan.budget.musicSpent, 5)
  assert.equal(totals(plan).musicLeft, 5)
  assert.match(dryRun(plan), /Flow Music budget: 10, spent 5, left 5/)
  assert.equal(plan.music[0].file, 'C:/m/m1.wav')
  assert.throws(() => recordResult(plan, 'ch09.s09.sh09', {}), /no shot/)
  assert.throws(() => recordResult(plan, 'music:m9', {}), /no music cue/)
})

/** A plan with a keyframe, a clip and voice files for every shot. */
function madePlan() {
  const { plan } = buildPlan(film(), { model: 'omni-360p' })
  for (const s of plan.shots) {
    recordResult(plan, s.id, { keyframe: { media_id: `m-${s.id}`, file: `/k/${s.id}.png` } })
    if (s.kind === 'video') recordResult(plan, s.id, { clip: { file: `/c/${s.id}.mp4`, credits: s.estimate.credits } })
    if (s.lines.length) recordResult(plan, s.id, { voices: s.lines.map((_, i) => ({ file: `/v/${s.id}-${i}.wav`, seconds: i === 0 && s.id.endsWith('sh03') ? 1.5 : 2 })) })
  }
  recordResult(plan, 'music:m1', { file: '/m/m1.wav', credits: 0 })
  return plan
}

test('timeline (final): trimmed clips, the title card as a still, voice times, music times, ducking', () => {
  const { args, warnings, runtimeSeconds } = buildTimeline(madePlan(), { dir: '/run' })
  assert.equal(runtimeSeconds, 21)
  assert.deepEqual(warnings, [])
  assert.equal(args.output_name, 'final')
  assert.equal(args.clip_volume, 0.3)
  assert.equal(args.duck, true)
  assert.equal(args.clips.length, 4)
  assert.deepEqual(args.clips[0], { file: path.resolve('/c/ch01.s01.sh01.mp4'), from: 0, to: 6 })
  assert.deepEqual(args.clips[1], { file: path.resolve('/c/ch01.s01.sh02.mp4'), from: 0, to: 6 })
  assert.deepEqual(args.clips[3], { image: path.resolve('/k/ch01.s01.sh04.png'), seconds: 3 })
  // shots start at 0, 6, 12, 18; a line starts 0.3 s in, the next one 0.25 s after the last ends
  assert.deepEqual(args.voice_lines.map((l) => l.at), [0.3, 6.3, 12.3, 14.05])
  assert.equal(args.voice_lines[0].file, path.resolve('/v/ch01.s01.sh01-0.wav'))
  assert.equal(args.voice_lines[0].max_seconds, 5.6) // 6 - 0.3 - 0.1
  assert.equal(args.voice_lines[3].max_seconds, 3.85) // the shot ends at 18
  // the music runs from the start of shot 1 to the end of shot 3
  assert.deepEqual(args.music_cues, [{ file: path.resolve('/m/m1.wav'), at: 0, until: 18 }])
  assert.equal(args.out, path.resolve('/run', 'out'))
})

test('timeline (animatic): keyframe stills with a slow zoom instead of the clips, even when clips exist', () => {
  const { args } = buildTimeline(madePlan(), { animatic: true, dir: '/run' })
  assert.equal(args.output_name, 'animatic')
  assert.deepEqual(args.clips.map((c) => c.seconds), [6, 6, 6, 3])
  assert.deepEqual(args.clips[0], { image: path.resolve('/k/ch01.s01.sh01.png'), seconds: 6, zoom: true })
  assert.equal(args.clips[3].zoom, undefined)
  assert.ok(args.clips.every((c) => !c.file))
})

test('timeline: a missing clip falls back to its keyframe with a warning, a missing voice file is left out, no keyframe is an error, a voice is timed by its file length', () => {
  const plan = madePlan()
  plan.shots[1].result.clips = []
  plan.shots[0].result.voices = []
  const r = buildTimeline(plan, { dir: '/run' })
  assert.deepEqual(r.args.clips[1], { image: path.resolve('/k/ch01.s01.sh02.png'), seconds: 6, zoom: true })
  assert.ok(r.warnings.some((w) => /sh02: no video clip yet/.test(w)))
  assert.ok(r.warnings.some((w) => /sh01: line 1 \(Narrator\) has no voice file/.test(w)))
  assert.equal(r.args.voice_lines.length, 3)
  plan.shots[2].result.keyframe = undefined
  plan.shots[2].result.clips = []
  assert.throws(() => buildTimeline(plan, { dir: '/run' }), /sh03: neither a clip nor a keyframe/)
  assert.throws(() => buildTimeline(buildPlan(film()).plan, { animatic: true }), /no keyframe file recorded/)
  // a line without a recorded length is probed, else timed by its words
  const p2 = madePlan()
  p2.shots[2].result.voices = [{ file: '/v/a.wav' }, { file: '/v/b.wav' }]
  const probed = buildTimeline(p2, { dir: '/run', probe: (f) => (f.endsWith('a.wav') ? 1 : null) })
  assert.deepEqual(probed.args.voice_lines.slice(2).map((l) => l.at), [12.3, 13.55]) // 12.3 + 1 + 0.25
  // a music cue with no file yet is not in the timeline
  p2.music[0].file = null
  assert.equal(buildTimeline(p2, { dir: '/run' }).args.music_cues, undefined)
})

test('the command line: plan writes plan.json and prints the dry run, record and timeline work on the files', () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'video-plan-'))
  try {
    copyFileSync(path.join(here, 'fixtures', 'screenplay-harbour.json'), path.join(dir, 'screenplay.json'))
    const out = []
    const log = (s) => out.push(s)
    assert.equal(main(['plan', dir, '--budget', '40', '--model', 'omni-360p', '--balance', '1010'], log), 0)
    assert.match(out.join('\n'), /Last known balance: 1010/)
    const plan = JSON.parse(readFileSync(path.join(dir, 'plan.json'), 'utf8'))
    assert.equal(plan.budget.credits, 40)
    assert.throws(() => main(['plan', dir], log), /exists/)
    main(['record', dir, 'ch01.s01.sh01', JSON.stringify({ keyframe: { media_id: 'k1', file: path.join(dir, 'k1.png') }, clip: { file: path.join(dir, 'c1.mp4'), credits: 6 } })], log)
    assert.match(out.at(-1), /spent 6 of 40, left 34/)
    assert.equal(JSON.parse(readFileSync(path.join(dir, 'plan.json'), 'utf8')).budget.spent, 6)
    main(['next', dir], log)
    assert.match(out.at(-1), /ch01.s01.sh02/)
    for (const id of ['ch01.s01.sh02', 'ch01.s01.sh03', 'ch01.s01.sh04']) writeFileSync(path.join(dir, `${id}.json`), JSON.stringify({ keyframe: { media_id: id, file: path.join(dir, `${id}.png`) } }))
    for (const id of ['ch01.s01.sh02', 'ch01.s01.sh03', 'ch01.s01.sh04']) main(['record', dir, id, `@${path.join(dir, `${id}.json`)}`], log)
    main(['timeline', dir, '--animatic'], log)
    const asm = JSON.parse(readFileSync(path.join(dir, 'assemble.json'), 'utf8'))
    assert.equal(asm.output_name, 'animatic')
    assert.equal(asm.clips.length, 4)
    assert.equal(main([], log), 2)
    assert.throws(() => main(['bogus', dir], log), /unknown command/)
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }
})

test('every price in the table is marked seen or guessed by price()', () => {
  for (const [model, p] of Object.entries(PRICES)) for (const s of [4, 6, 8, 10]) assert.ok(['seen', 'guessed'].includes(price(model, s).status), `${model} ${s}`)
})

test('HUB-14: the title card asks for its text, voice-over lines get a style, insert shots carry no cast', () => {
  const f = film()
  f.style = 'Live-action film look, no text on screen.'
  const withInsert = { ...f.chapters[0].scenes[0].shots[0], id: 'ch01.s01.sh09', framing: 'insert', action: 'A yellow button on a desk.' }
  f.chapters[0].scenes[0].shots.push(withInsert, { ...withInsert, id: 'ch01.s01.sh10', action: 'Mara presses the yellow button.' })
  f.chapters[0].scenes[0].shots[0].cast = [{ name: 'Mara', look: '' }]
  f.chapters[0].scenes[0].shots[4].cast = [{ name: 'Mara', look: '' }]
  f.chapters[0].scenes[0].shots[5].cast = [{ name: 'Mara', look: '' }]
  f.chapters[0].scenes[0].shots[0].lines = [{ speaker: 'Ante', delivery: '', text: 'Old words.', kind: 'voice-over' }]
  const { plan } = buildPlan(f)
  const title = plan.shots.find((s) => s.kind === 'title')
  assert.doesNotMatch(title.keyframePrompt, /no text/i)
  assert.match(title.keyframePrompt, /Live-action film look\./)
  assert.match(title.keyframePrompt, /Title card with the words "The End" shown clearly/)
  assert.match(plan.shots[0].keyframePrompt, /no text on screen/i)
  assert.deepEqual(plan.shots[4].cast, [])
  assert.deepEqual(plan.shots[4].refs, [])
  assert.doesNotMatch(plan.shots[4].keyframePrompt, /Mara/)
  assert.deepEqual(plan.shots[5].refs, ['Mara'])
  const kf = keyframeScenes(plan)
  assert.equal(kf[4].reference_images, undefined)
  assert.equal(voiceCalls(plan)[0].style, 'as a voice-over narrator')
})

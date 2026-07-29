# Keyboard tune — `jazz.mp4` @ 16.0s–24.0s

Extracted from the final 8 seconds of the source video (total duration 24.53s).

## Files

| File | What it is |
|---|---|
| `tune_16-24.wav` | Raw extract, 44.1kHz stereo PCM |
| `tune_16-24.mp3` | Same, V2 MP3 |
| `jazz_tune_16-24.mid` | Transcribed melody, 16 notes, tempo stamped 152.2 BPM |
| `transcription_render.mp3` | The MIDI rendered with a matched tone, for checking |
| `AB_orig-L_render-R.wav` | Original in left ear, transcription in right — A/B the accuracy |

## What's actually in the audio

The source is **monophonic** — one note at a time, no chords. The timbre is a
fundamental plus a weak octave partial (~22%) and essentially nothing else:
a near-sine, flute/whistle-like keyboard patch.

It is also steeply band-limited. 85% of all energy sits in 500–1000 Hz, with
0.53% below 250 Hz and 0.05% above 6 kHz. **There is no bass and no drums in
this clip** — no cymbal/hat content at all. You are getting a bare melody line.

Tuning reference is A ≈ 440.8 Hz (+3.3 cents), so it will sit fine against
standard-tuned instruments.

## The melody

Range is **B4 – F5** — just a tritone, 16 notes.

```
  D5  C5  B4  |  E5   F5   ·rest·  |  B4   (E5) D5  ·rest·
  C5  B4  Eb5 |  C5   B4   E5  F5  |  C5
```

| # | Start (rel) | Abs. time | Note | Dur | Hz |
|--:|---:|---:|:--|---:|---:|
| 1 | 0.000 | 16.000 | D5 | 0.627 | 588.24 |
| 2 | 0.627 | 16.627 | C5 | 0.081 | 526.64 |
| 3 | 0.708 | 16.708 | B4 | 0.221 | 495.70 |
| 4 | 0.929 | 16.929 | E5 | 0.348 | 659.95 |
| 5 | 1.277 | 17.277 | F5 | 0.488 | 699.87 |
| 6 | 2.357 | 18.357 | B4 | 0.395 | 496.09 |
| 7 | 2.891 | 18.891 | E5 | 0.128 | 649.69 |
| 8 | 3.019 | 19.019 | D5 | 0.836 | 588.17 |
| 9 | 3.936 | 19.936 | C5 | 0.534 | 524.61 |
| 10 | 4.470 | 20.470 | B4 | 0.371 | 495.22 |
| 11 | 4.841 | 20.841 | **D#5/Eb5** | 0.093 | 623.76 |
| 12 | 4.992 | 20.992 | C5 | 0.151 | 526.31 |
| 13 | 5.143 | 21.143 | B4 | 0.116 | 495.58 |
| 14 | 5.259 | 21.259 | E5 | 0.128 | 661.03 |
| 15 | 5.387 | 21.387 | F5 | 0.720 | 699.89 |
| 16 | 6.107 | 22.107 | C5 | 0.580 | 524.56 |

Notes 2 and 7 are very short (81ms, 128ms) — they read as grace notes or
portamento through the interval rather than deliberate melody notes.

The clip goes quiet after 6.687s (22.69s absolute), with two faint high blips
(C6, A5) at the very end that are likely the video's tail, not part of the tune.

### Pitch set

**B – C – D – Eb – E – F**, weighted by sounding time:

```
D   25.2%  ███████████████
C   23.1%  █████████████
F   20.8%  ████████████
B   19.0%  ███████████
E   10.4%  ██████
Eb   1.6%  ▌            <- the blue note
```

Two things make this jazz-usable rather than generic:

1. **The tritone B–F** is the melody's outer frame and its most-used pair.
2. **Eb against E natural** — a single 93ms blue note rubbing the major 3rd.

### The hook

The figure **B4 → E5 → F5** (up a perfect 4th, then up a semitone) appears
twice: once at 0.708–1.277 spread over ~0.57s, then again at 5.143–5.387
compressed into ~0.24s. Same shape, half the length — a built-in diminution.
That's your motif.

## Tempo

The timing is loose — played by hand, not quantized. No grid fits cleanly
(best mean deviation ~16ms, about 12% of a subdivision), so treat this as
rubato and expect to nudge notes.

Two readings tie, and they are the same grid seen two ways (114×4 = 152×3 = 456
subdivisions/min):

- **114 BPM with straight 16ths** ← recommended, and independently confirmed by
  autocorrelation of the onset envelope (114.84 BPM)
- **152 BPM with triplet 8ths** ← what's stamped in the MIDI

That the same grid reads as both is itself a hint: the phrasing has a triplet
lilt baked in. Lean into it with swing rather than fighting it straight.

## Harmonising it

Every note lands inside **G7**, which is the tightest single-chord fit:

| Melody note | vs. G7 |
|---|---|
| B | 3rd |
| F | ♭7th |
| D | 5th |
| C | 11th |
| E | 13th |
| Eb | ♭13th |

The B–F tritone *is* the tritone of G7. That's why the tune sounds unresolved
and hangs — it's sitting on a dominant the whole time.

Three frames worth trying, easiest to most involved:

1. **Static vamp — Gm7 → C7** (2 bars each). Simple, groovy, lets the melody float.
2. **Turnaround — Dm7 → G7 → Cmaj7 → A7♭13.** Resolves the tension. Land the
   final C5 on the Cmaj7 and it clicks shut.
3. **Blues frame — C7♯9.** Reinterprets the Eb as the ♯9 and the E as the 3rd,
   which is exactly the major/minor-third rub the melody already has. Most
   characterful option.

An alternative colour: treat **F as tonic** and the B becomes a ♯11 — an
F Lydian pad under the same melody sounds dreamy rather than bluesy.

## Building the groovy jazz track

### Rhythm section (the clip gives you none of this)

- **Drums** — brushed or soft-stick kit at ~114 BPM, swung 8ths. Ride pattern
  on 2 and 4, ghost notes on the snare. Since the source has zero content above
  6 kHz, hats and ride will sit in totally clear spectrum — no masking.
- **Bass** — upright or a round electric. You have an empty field below 250 Hz;
  put a walking line there. For frame 1, walk G–Bb–C–E under Gm7→C7.
- **Comping** — Rhodes or nylon guitar in the 250–500 Hz gap. Rootless voicings
  so you don't collide with the bass. Push chords onto the "and" of 4.

### Placing the melody

- **Double it an octave down** on Rhodes or vibraphone. The original is thin and
  lives entirely in 500–1000 Hz; an octave below fills it out without EQ.
- **Harmonise the hook in 4ths** (B–E, E–A, F–Bb) for a McCoy Tyner colour, or
  in 3rds below for something sweeter.
- **Loop the 4-bar phrase** as a head, play it twice, then solo over the
  turnaround and bring it back. The two hook statements (long, then compressed)
  already give you a head that develops itself.

### Using the audio itself

- The clip is clean and monophonic, so **pitch-tracking to MIDI works well** —
  `jazz_tune_16-24.mid` is that, ready to drop on any instrument.
- To use the recording as-is, **high-pass at 300 Hz** (nothing lives below it
  anyway) and add reverb — the dry, band-limited tone sits nicely as a lo-fi
  "sampled from an old record" texture over a modern rhythm section.
- **Chop the hook** (0.708–1.277s, the B–E–F figure) into a one-shot and
  retrigger it rhythmically over the vamp.
- Because it's a near-sine, it **pitch-shifts very cleanly** — transpose it to
  build a counter-line without artefacts.

### Arrangement sketch

```
Bars 1–4    drums + bass vamp, establish the groove
Bars 5–12   head: melody as transcribed, doubled 8vb
Bars 13–20  head repeat, add Rhodes comping + the 4ths harmony on the hook
Bars 21–36  solo over Dm7–G7–Cmaj7–A7b13
Bars 37–44  head out, land on Cmaj7
```

## Method / caveats

Analysis was done with FFT spectral-peak tracking (16384-point window,
~2.7 Hz resolution, parabolic interpolation) — this is algorithmic
transcription, not transcription by ear.

An initial pass using harmonic-sum salience reported chords a couple of octaves
lower; that was an artefact of the method inventing fundamentals beneath the
real partials, and full-band energy measurement ruled it out. The numbers above
come from the direct peak-tracking pass. Check `AB_orig-L_render-R.wav` to
confirm the result against the source yourself — that's the honest test.

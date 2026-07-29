# `jazz_groove.mp3` — the track

49 seconds, 114 BPM, swung 8ths (swing point 0.62), key centre C.
Built entirely around slices of `transcription_render.mp3`.

## How the melody was used

The rendered melody was decoded and cut at the 16 known note boundaries — the
MP3 decodes sample-aligned with the original render (cross-correlation 1.0), so
the slices land exactly on the note starts with no drift.

The original performance is rubato, so each slice was re-placed on a swung
114 BPM grid. Quantized positions, in beats:

```
D5 0.0  | C5 1.25 (grace) | B4 1.5 | E5 1.75 | F5 2.5
B4 4.5  | E5 5.4 (grace)  | D5 5.75
C5 7.5  | B4 8.5 | Eb5 9.25 | C5 9.5 | B4 9.75 | E5 10.0 | F5 10.25
C5 11.5 (rings through bar 4)
```

That makes the head a clean 4-bar phrase. Every hit also gets ±4–8 ms of timing
jitter and velocity variation so it doesn't sound machine-stamped.

## Arrangement

| Bars | Section | What happens |
|---|---|---|
| 1–4 | Intro | Walking bass + brushes, Rhodes fades in from bar 3 |
| 5–8 | Head A | Melody enters, light comping |
| 9–12 | Head B | Fuller — ghost notes on the snare, ride bell accents |
| 13–16 | Hook chops | The B–E–F motif retriggered rhythmically |
| 17–20 | Head C | Head out, thinning toward the end |
| 21–22 | Ending | Final C, Dm9 spread, ride bell rings out |

## Changes

**Dm7 | G7 | Cmaj7 | A7♭13** — the turnaround from the transcription notes.

Rootless Rhodes voicings, kept below the melody so they don't collide:

```
Dm7    F3 A3 C4 E4      (b3 5 b7 9)
G7     F3 A3 B3 E4      (b7 9 3 13)
Cmaj7  E3 G3 B3 D4      (3 5 7 9)
A7b13  E3 G3 C#4 F4     (5 b7 3 b13)
```

Walking bass, one note per beat:

```
Dm7    D2  F2  A2  Ab2     -> chromatic approach to G
G7     G2  B2  D3  Db3     -> chromatic approach to C
Cmaj7  C3  B2  A2  G2      -> descending
A7b13  A2  G2  F2  E2      -> descending into D
```

## The bit that works

The **B–E–F hook fits all four chords without transposition**:

| | Dm7 | G7 | Cmaj7 | A7♭13 |
|---|---|---|---|---|
| B | 13 | 3 | 7 | 9 |
| E | 9 | 13 | 3 | 5 |
| F | ♭3 | ♭7 | 11 | ♭13 |

That's why bars 13–16 can just retrigger the motif over the whole turnaround
and it never sounds wrong. It's the most useful property of this melody.

## What I added that the source didn't have

The clip is a bare sine melody in 500–1000 Hz — no bass, no drums, no chords.
Everything else is synthesized:

- **Rhodes** — FM, 1:1 ratio, modulation index decaying over 130 ms for the bell attack, plus tremolo
- **Upright bass** — sine with decaying 2nd/3rd/4th harmonics and a filtered-noise finger pluck
- **Kick** — pitch sweep 127→45 Hz plus a 52 Hz sub layer
- **Brushed snare** — bandpassed noise, 900–8000 Hz, with a little 197/331 Hz shell tone
- **Ride** — eight inharmonic partials plus high-passed noise; classic swing pattern on 1, 2, 2&, 3, 4, 4&
- **Octave doubling** — a soft vibes-like voice an octave below the melody, which is the fill-out I recommended in the transcription notes

## Mix

Peak −0.9 dBFS, RMS −16.1 dBFS, crest factor 15.2 dB — deliberately left
dynamic rather than loudness-maximised, which is what jazz wants. No samples
near full scale.

Energy distribution: 14% at 60–120 Hz, 9% at 120–250, 15% at 250–500,
40% at 500–1000, 12% at 1–2 kHz.

The 500–1000 Hz figure is still the largest share and that's inherent — the
source melody is a pure sine living entirely in that band. It's high-passed at
300 Hz with a −3 dB dip at 700 Hz to stop it honking, and the Rhodes has a
−2.5 dB dip at 480 Hz to make room. If you want it less mid-forward, pull the
`mel` stem down 2–3 dB.

## Files

| File | |
|---|---|
| `jazz_groove.mp3` / `.wav` | The track |
| `stems/*.mp3` | 8 stems: kick, snare, ride, hat, bass, keys, mel, mel8 |
| `build_song.py` | The generator — edit and re-run to change anything |

Stems are pre-fader-position (panned, EQ'd, reverb applied) and sum to the
master, so you can rebalance without re-rendering.

## Tweaking

In `build_song.py`:

- `BPM` (114.0) and `SWING` (0.62 — set 0.5 for straight, 0.667 for hard triplet swing)
- `GAIN` / `PAN` / `WET` dicts — per-bus mix
- `VOICE` / `WALK` / `COMP` — the four-bar harmony, bass line, and comping rhythm
- `HEAD` — melody placement, as (beat, slice index) pairs
- `rng = default_rng(7)` — change the seed for different humanization

It needs `numpy`, `scipy`, `soundfile`, and `mel_decoded.wav` (decode
`transcription_render.mp3` to mono 44.1 kHz WAV alongside it).

## Caveat

This is synthesized from first principles in numpy — no sampled instruments and
no soundfont was available, so the drums and Rhodes are approximations rather
than the real thing. The arrangement, harmony and groove are solid; if you want
production-grade tone, take `jazz_tune_16-24.mid` and the chord chart above into
a DAW with proper instruments.

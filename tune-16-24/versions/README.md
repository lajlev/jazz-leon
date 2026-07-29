# Toned-down versions

Four takes on the same tune, 41 seconds each, 114 BPM swung. Same head, same
changes, same arrangement — only the lead instrument differs.

| File | Lead | Register |
|---|---|---|
| `piano.mp3` | Acoustic jazz piano | B4–F5, as transcribed |
| `guitar.mp3` | Archtop guitar | B3–F4, down an octave |
| `bass.mp3` | Upright bass, melodic | B3–F4, down an octave |
| `soft.mp3` | The original sine slices | B4–F5, as transcribed |

All loudness-matched to roughly −18 to −19 dBFS RMS, with the lead sitting a
consistent **+5.0 dB over the backing** — measured only across the stretch where
the lead is actually sounding, so silence doesn't skew it. A/B them directly.

## What got toned down

Compared to `../jazz_groove.mp3`:

- **18 bars instead of 22.** The hook-chops section is gone.
- **Two-feel bass.** Root on 1 and 3 through the intro and first head, opening
  into a walking line only from head 2. That's the single biggest calming change.
- **Two comp stabs a bar** instead of three, and quieter.
- **No ride bell**, no kick accents — just feathering on 1 and 3.
- **Brush swirls** on beat 3 rather than extra ghost notes.
- Less reverb, and the octave-doubling layer is dropped (the real instruments
  have their own body, so it isn't needed).

Structure: 4 bars intro → 3 × 4-bar heads → 2-bar ending.

## Arrangement per version

**piano** — piano trio. Piano leads and comps, walking/two-feel upright, brushes.

**guitar** — guitar leads, Rhodes comps, upright and brushes behind.

**bass** — the bass *is* the melody, so there's no walking line under it. A
two-feel root on 1 and 3 holds the bottom, and the Rhodes comping is lifted an
octave (to 349–698 Hz) to stay clear of the bass melody at 247–350 Hz.

**soft** — the original band-limited sine lead, in the calmer arrangement.

## Sound sources

Everything is synthesized in numpy; there were no sampled instruments available.

- **Piano** — 20 additive partials with string inharmonicity (B = 0.00035), higher partials decaying faster, plus a filtered-noise hammer transient
- **Guitar** — Karplus-Strong plucked string, ρ = 0.9972, low-passed at 2.6 kHz for a warm flatwound/neck-pickup tone
- **Bass** — sine core with harmonics 2–7, mild waveshaping for growl. The solo voice uses longer harmonic decays than the accompaniment voice so the melody keeps definition in a low register
- **Drums** — pitch-swept kick with a 52 Hz sub layer, bandpassed-noise brushes, ride built from seven inharmonic partials

## Balance

Energy by band (% of total):

| | 60–120 | 120–250 | 250–500 | 500–1k | 1–2k |
|---|---|---|---|---|---|
| piano | 12.2 | 6.2 | 10.7 | 49.6 | 15.2 |
| guitar | 11.5 | 7.3 | 14.9 | 39.3 | 21.3 |
| bass | 9.0 | 4.3 | 60.0 | 17.1 | 7.1 |
| soft | 12.7 | 6.1 | 12.1 | 61.9 | 4.9 |

**guitar** is the most evenly spread — the Karplus-Strong harmonics fill
1–2 kHz, which nothing else here does.

**bass** concentrates in 250–500 Hz, and that's inherent: it's the bass melody's
fundamental register and it's the lead, so it dominates by design. If it reads
boxy on your system, cut 2–3 dB around 350 Hz on the `lead` stem.

**piano** and **soft** both sit around 50–60% in 500–1000 Hz, which is simply
where the melody lives (B4–F5 = 494–698 Hz).

## Files

Each version ships as `.mp3` (V1) and `.wav`, plus a `stems_<version>/` folder
with 7 stems: kick, snare, ride, hat, bass, keys, lead. Stems are post-EQ,
post-pan, post-reverb and scaled by the same master gain, so they sum back to
the mix exactly.

`build_versions.py` regenerates all four. The `CFG` dict at the top is where the
per-version choices live:

```python
CFG={ 'piano':  dict(lead='piano',  tr=0,   ring=0.95, walk=True,  comp='piano',  lg=0.52, ctr=0),
      'guitar': dict(lead='guitar', tr=-12, ring=1.10, walk=True,  comp='rhodes', lg=0.60, ctr=0),
      'bass':   dict(lead='bass',   tr=-12, ring=0.75, walk=False, comp='rhodes', lg=0.62, ctr=12),
      'soft':   dict(lead='slice',  tr=0,   ring=0.0,  walk=True,  comp='rhodes', lg=0.40, ctr=0) }
```

`tr` transposes the lead, `ring` is how long notes sustain past the next onset,
`walk` toggles walking vs two-feel bass, `ctr` transposes the comping.

Transposition must stay in multiples of 12 — anything else changes the key.

It needs `numpy`, `scipy`, `soundfile`, and (for the `soft` version only)
`mel_decoded.wav`, which is `../transcription_render.mp3` decoded to mono
44.1 kHz WAV.

## Note

`TARGET_DB = 5.0` in the script drives the automatic lead-vs-backing balance.
Raise it if you want the lead further forward. It's applied by measuring the
actual mix and correcting, so it holds regardless of how loud the raw
instrument happens to be — the bass lead needed −6.5 dB of correction, the sine
lead needed +4.1 dB.

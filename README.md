# Malon — eight seconds on an old keyboard

My nephew was jamming on an old keyboard. My in-laws posted a video of it, and
eight seconds of it sounded genuinely like a jazz melody. I pulled those eight
seconds out, worked out what they had played, and built a band underneath it.

**→ [lajlev.github.io/jazz-malon](https://lajlev.github.io/jazz-malon/)**

## What's here

```
index.html              the site
styles.css  score.js    styling + VexFlow notation
audio/                  the four stages, as MP3
img/                    three frames from the source video
tune-16-24/
  TRANSCRIPTION.md      how the melody was extracted, note by note
  SONG.md               the first arrangement
  build_song.py         generates that arrangement
  jazz_tune_16-24.mid   the transcribed melody as MIDI
  versions/
    README.md           the toned-down versions and how they differ
    build_versions.py   generates all of them
```

## The tune

Sixteen notes, range B4–F5, pitch set **B C D E♭ E F**. The tritone B–F frames
the melody; a single 93 ms E♭ is the blue note. The hook — **B4 → E5 → F5** —
appears twice, the second time at half length, and fits all four chords of the
turnaround without transposition.

Changes: **Dm7 | G7 | Cmaj7 | A7♭13**, 114 BPM, swung.

## Reproducing the audio

The MP3s in `audio/` are committed. The WAVs, stems, the other lead versions
and the source video are gitignored — regenerate them with:

```sh
pip install numpy scipy soundfile
python tune-16-24/versions/build_versions.py
```

The backing band is synthesized from scratch in numpy — no sampled instruments.
FM Rhodes, Karplus-Strong guitar, additive piano with string inharmonicity,
pitch-swept kick, bandpassed-noise brushes.

## Credit

Composed by my nephew, who was not consulted about the chord changes.

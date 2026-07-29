/* Melody notation — 4 bars, 4/4, key of C, 114 BPM swung.
   Renders with VexFlow 4 (UMD build exposes window.Vex). */
(function () {
  'use strict';

  var INK  = '#14110f';
  var HOT  = '#d8542a';
  var TEAL = '#2e6b6b';

  // Pitch order: D5 C5 B4 E5 F5 | B4 E5 D5 C5 | B4 Eb5 C5 B4 E5 F5 | C5
  // Rhythms are quantised to a readable 16th grid; each bar totals 4 beats.
  var BARS = [
    [ { k: 'd/5', d: '4d' },
      { k: 'b/4', d: '16', grace: 'c/5' },
      { k: 'e/5', d: '8d' },
      { k: 'f/5', d: '4'  },
      { rest: true, d: '8r' } ],

    [ { rest: true, d: '8r' },
      { k: 'b/4', d: '4d' },
      { k: 'd/5', d: '4d', grace: 'e/5' },
      { k: 'c/5', d: '8'  } ],

    [ { rest: true, d: '8r' },
      { k: 'b/4',  d: '8d' },
      { k: 'eb/5', d: '16', acc: 'b', blue: true },
      { k: 'c/5',  d: '16' },
      { k: 'b/4',  d: '16' },
      { k: 'e/5',  d: '16' },
      { k: 'f/5',  d: '4d' },
      { rest: true, d: '16r' } ],

    [ { k: 'c/5', d: 'w' } ]
  ];

  function render() {
    var host = document.getElementById('score');
    if (!host) return;

    var Vex = window.Vex;
    var VF  = (Vex && Vex.Flow) ? Vex.Flow : Vex;
    if (!VF || !VF.Renderer) throw new Error('VexFlow not available');

    host.innerHTML = '';

    var total    = Math.max(host.clientWidth || 0, 300);
    var perRow   = total < 720 ? 2 : 4;
    var rows     = Math.ceil(BARS.length / perRow);
    var pad      = 10;
    var firstExtra = 42;                       // clef + time sig room
    var rowH     = 132;
    var width    = total - pad * 2;

    var renderer = new VF.Renderer(host, VF.Renderer.Backends.SVG);
    renderer.resize(total, rows * rowH + 26);
    var ctx = renderer.getContext();
    ctx.setFont('Roboto Mono', 11);

    BARS.forEach(function (bar, i) {
      var row    = Math.floor(i / perRow);
      var col    = i % perRow;
      var basicW = (width - firstExtra) / perRow;
      var w      = basicW + (col === 0 ? firstExtra : 0);
      var x      = pad + (col === 0 ? 0 : firstExtra + basicW * col);
      var y      = 12 + row * rowH;

      var stave = new VF.Stave(x, y, w);
      if (col === 0) {
        stave.addClef('treble');
        if (row === 0) stave.addTimeSignature('4/4');
      }
      if (row === 0 && col === 0) {
        stave.setText('♩ = 114  ( swung )', VF.StaveModifier.Position.ABOVE, {
          justification: VF.StaveText.LEFT, shift_y: -12
        });
      }
      stave.setStyle({ strokeStyle: INK, fillStyle: INK });
      stave.setContext(ctx).draw();

      var notes = bar.map(function (n) {
        var sn = new VF.StaveNote({
          keys: [n.rest ? 'b/4' : n.k],
          duration: n.d,
          clef: 'treble'
        });

        if (n.d.indexOf('d') > -1 && VF.Dot && VF.Dot.buildAndAttach) {
          VF.Dot.buildAndAttach([sn], { all: true });
        }
        if (n.acc) sn.addModifier(new VF.Accidental(n.acc), 0);

        if (n.grace) {
          try {
            var g = new VF.GraceNote({ keys: [n.grace], duration: '16', slash: true });
            g.setStyle({ fillStyle: TEAL, strokeStyle: TEAL });
            sn.addModifier(new VF.GraceNoteGroup([g], false).beamNotes(), 0);
          } catch (e) { /* grace notes are a nicety, not a requirement */ }
        }

        if (n.blue) {
          sn.setStyle({ fillStyle: HOT, strokeStyle: HOT });
          try {
            var a = new VF.Annotation('blue note')
              .setVerticalJustification(VF.Annotation.VerticalJustify.TOP);
            a.setStyle({ fillStyle: HOT, strokeStyle: HOT });
            sn.addModifier(a, 0);
          } catch (e) { /* annotation optional */ }
        } else if (!n.rest) {
          sn.setStyle({ fillStyle: INK, strokeStyle: INK });
        }
        return sn;
      });

      var voice = new VF.Voice({ num_beats: 4, beat_value: 4 });
      voice.setStrict(false);
      voice.addTickables(notes);

      new VF.Formatter().joinVoices([voice]).format([voice], w - (col === 0 ? 62 : 22));

      var beams = [];
      try { beams = VF.Beam.generateBeams(notes.filter(function (n) { return !n.isRest(); })); }
      catch (e) { beams = []; }

      voice.draw(ctx, stave);
      beams.forEach(function (b) {
        b.setStyle({ fillStyle: INK, strokeStyle: INK });
        b.setContext(ctx).draw();
      });
    });
  }

  function boot() {
    try {
      render();
    } catch (err) {
      var host = document.getElementById('score');
      var fb   = document.getElementById('score-fallback');
      if (host) host.style.display = 'none';
      if (fb) fb.hidden = false;
      if (window.console) console.error('[score] notation failed:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(boot, 220);
  });
})();

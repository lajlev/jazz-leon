"""Build a jazz track around the sliced melody from transcription_render.mp3."""
import numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, fftconvolve

SR   = 44100
BPM  = 114.0
BEAT = 60.0 / BPM
BAR  = 4 * BEAT
SWING = 0.62
rng = np.random.default_rng(7)

def swing(pos):
    b, f = np.floor(pos), pos - np.floor(pos)
    f = f*(SWING/0.5) if f < 0.5 else SWING + (f-0.5)*((1-SWING)/0.5)
    return (b + f) * BEAT

def hz(m): return 440.0 * 2**((m-69)/12)
def lp(x, fc, o=2): b,a = butter(o, min(fc,SR/2-1)/(SR/2), 'low');  return lfilter(b,a,x)
def hp(x, fc, o=2): b,a = butter(o, min(fc,SR/2-1)/(SR/2), 'high'); return lfilter(b,a,x)
def bp(x, f1, f2, o=2):
    b,a = butter(o, [f1/(SR/2), min(f2,SR/2-1)/(SR/2)], 'band'); return lfilter(b,a,x)
def peakdip(x, fc, q, gain_db):
    """Simple biquad peaking EQ."""
    A = 10**(gain_db/40); w0 = 2*np.pi*fc/SR; al = np.sin(w0)/(2*q)
    b = [1+al*A, -2*np.cos(w0), 1-al*A]; a = [1+al/A, -2*np.cos(w0), 1-al/A]
    return lfilter(np.array(b)/a[0], np.array(a)/a[0], x)
def env(n, a, d, r=None):
    e = np.zeros(n); ai = max(int(a*SR),1)
    e[:ai] = np.linspace(0,1,ai)
    e[ai:] = np.exp(-np.arange(n-ai)/(d*SR))
    if r:
        ri = int(r*SR)
        if ri < n: e[-ri:] *= np.linspace(1,0,ri)
    return e

# ---------------------------------------------------------------- instruments
def rhodes(f, dur, amp=0.5):
    n = int(dur*SR); t = np.arange(n)/SR
    idx = 2.6*np.exp(-t/0.13)
    y = np.sin(2*np.pi*f*t + idx*np.sin(2*np.pi*f*t))
    y += 0.18*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.25)
    y *= env(n, 0.004, max(dur*0.55,0.35), r=0.05)
    y *= 1 + 0.09*np.sin(2*np.pi*4.6*t)
    return y*amp

def vibes(f, dur, amp=0.5):
    """Soft octave-doubling voice under the melody — sine + slow tremolo."""
    n = int(dur*SR); t = np.arange(n)/SR
    y = np.sin(2*np.pi*f*t) + 0.30*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.10)
    y *= env(n, 0.006, max(dur*0.6,0.4), r=0.06)
    y *= 1 + 0.14*np.sin(2*np.pi*5.2*t)
    return y*amp

def upright(f, dur, amp=0.9):
    n = int(dur*SR); t = np.arange(n)/SR
    y  = np.sin(2*np.pi*f*t)
    y += 0.42*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.28)
    y += 0.16*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.14)
    y += 0.09*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.07)
    pluck = lp(rng.standard_normal(n), 2600)*np.exp(-t/0.012)*0.5
    y = y*env(n, 0.006, 0.45, r=0.04) + pluck
    return np.tanh(y*1.25)*amp

def kick(dur=0.50, amp=1.0):
    n = int(dur*SR); t = np.arange(n)/SR
    f = 45 + 82*np.exp(-t/0.030)
    y  = np.sin(2*np.pi*np.cumsum(f)/SR)*env(n, 0.001, 0.14)
    y += 0.45*np.sin(2*np.pi*52*t)*np.exp(-t/0.10)          # sub weight
    y += lp(rng.standard_normal(n),1800)*np.exp(-t/0.004)*0.22
    return y*amp

def brush(dur=0.30, amp=1.0, ghost=False):
    n = int(dur*SR); t = np.arange(n)/SR
    nz = bp(rng.standard_normal(n), 900, 8000)
    y  = nz*np.exp(-t/(0.035 if ghost else 0.075))
    if not ghost:
        y += (np.sin(2*np.pi*197*t)+0.6*np.sin(2*np.pi*331*t))*np.exp(-t/0.05)*0.30
    return y*amp*(0.30 if ghost else 1.0)

def ride(dur=1.5, amp=1.0, bell=False):
    n = int(dur*SR); t = np.arange(n)/SR
    y = np.zeros(n)
    for p,g in [(523,.5),(789,.42),(1187,.36),(1631,.3),(2417,.24),(3319,.20),(4703,.16),(6421,.11)]:
        y += g*np.sin(2*np.pi*p*(1+rng.uniform(-.01,.01))*t)*np.exp(-t/(0.9 if bell else 0.42))
    y += hp(rng.standard_normal(n), 5000)*np.exp(-t/0.30)*(1.1 if not bell else 0.5)
    y *= env(n, 0.0015, 1.0, r=0.05)
    return y*amp*0.35

def chick(dur=0.16, amp=1.0):
    n = int(dur*SR); t = np.arange(n)/SR
    return hp(rng.standard_normal(n), 6200)*np.exp(-t/0.022)*amp*0.7

# ---------------------------------------------------------------- melody slices
mel, _ = sf.read('mel_decoded.wav')
NOTES = [(0.000,0.627,74),(0.627,0.708,72),(0.708,0.929,71),(0.929,1.277,76),
         (1.277,1.765,77),(2.357,2.752,71),(2.891,3.019,76),(3.019,3.855,74),
         (3.936,4.470,72),(4.470,4.841,71),(4.841,4.934,75),(4.992,5.143,72),
         (5.143,5.259,71),(5.259,5.387,76),(5.387,6.107,77),(6.107,6.687,72)]
SLICES = []
for s,e,m in NOTES:
    seg = mel[int(s*SR):int(e*SR)].copy()
    f = min(int(0.004*SR), len(seg)//4)
    seg[:f] *= np.linspace(0,1,f); seg[-f:] *= np.linspace(1,0,f)
    SLICES.append(seg)

def shift(seg, semis):
    if semis == 0: return seg
    r = 2**(semis/12); n = int(len(seg)/r)
    return np.interp(np.arange(n)*r, np.arange(len(seg)), seg)

# ---------------------------------------------------------------- arrangement
BARS = 22
total = int(BARS*BAR*SR) + SR*4
mix = {k: np.zeros(total) for k in
       ['kick','snare','ride','hat','bass','keys','mel','mel8']}

def put(bus, sig, tsec, gain=1.0):
    i = max(0, int(tsec*SR))          # clamp: bar-0 jitter can go negative
    if i >= total or len(sig) == 0: return
    j = min(i+len(sig), total)
    mix[bus][i:j] += sig[:j-i]*gain

VOICE = [[53,57,60,64], [53,57,59,64], [52,55,59,62], [52,55,61,65]]
WALK  = [[38,41,45,44], [43,47,50,49], [48,47,45,43], [45,43,41,40]]
COMP  = [[0.0,1.5,3.0], [0.5,2.0,3.5], [0.0,1.5,2.5], [0.5,2.0,3.0]]

def bar_ofs(b): return b*BAR

def lay_bass(b, ci, gain=1.0):
    for k, m in enumerate(WALK[ci]):
        t = bar_ofs(b) + swing(k) + rng.normal(0,0.006)
        put('bass', upright(hz(m), BEAT*1.02), t, gain*rng.uniform(0.85,1.0))

def lay_drums(b, gain=1.0, busy=False, feather=True):
    o = bar_ofs(b)
    for k in [0,1,1.5,2,3,3.5]:
        acc = 1.0 if k in (0,2) else 0.72
        put('ride', ride(1.5, bell=(k in (0,2) and busy)),
            o+swing(k)+rng.normal(0,0.005), gain*acc*rng.uniform(0.85,1.05))
    for k in [1,3]:
        put('hat', chick(), o+swing(k)+rng.normal(0,0.004), gain*rng.uniform(0.8,1.0))
        put('snare', brush(), o+swing(k)+rng.normal(0,0.006), gain*0.55*rng.uniform(0.85,1.05))
    if busy:
        for k in rng.choice([0.5,1.5,2.5,3.5], 2, replace=False):
            put('snare', brush(ghost=True), o+swing(k), gain*0.9)
    if feather:
        for k in [0,1,2,3]:
            put('kick', kick(), o+swing(k)+rng.normal(0,0.005), gain*0.18)
    put('kick', kick(), o+swing(2.5 if b % 4 in (1,3) else 0.0), gain*0.60)

def lay_keys(b, ci, gain=1.0):
    for k in COMP[ci]:
        t = bar_ofs(b) + swing(k) + rng.normal(0,0.008)
        for j, m in enumerate(VOICE[ci]):
            put('keys', rhodes(hz(m), BEAT*1.8), t + j*0.006,
                gain*rng.uniform(0.8,1.0)*(0.95 if j else 1.0))

HEAD = [(0.00,0),(1.25,1),(1.50,2),(1.75,3),(2.50,4),(4.50,5),(5.40,6),(5.75,7),
        (7.50,8),(8.50,9),(9.25,10),(9.50,11),(9.75,12),(10.00,13),(10.25,14),(11.50,15)]

def lay_head(b0, gain=1.0, octave=True):
    for pos, idx in HEAD:
        t = bar_ofs(b0) + swing(pos) + rng.normal(0,0.004)
        put('mel', SLICES[idx], t, gain*rng.uniform(0.9,1.0))
        if octave and len(SLICES[idx]) > 0.12*SR:      # skip grace notes
            dur = len(SLICES[idx])/SR
            put('mel8', vibes(hz(NOTES[idx][2]-12), dur*1.25), t, gain*0.9)

HOOK = [12,13,14]
def lay_chops(b0, gain=1.0):
    for f in [0.0, 2.5, 4.5, 8.0, 10.0]:
        for j, idx in enumerate(HOOK):
            seg = SLICES[idx]
            if j == 2 and f not in (4.5, 10.0): seg = seg[:int(0.22*SR)]
            t = bar_ofs(b0)+swing(f+j*0.5)+rng.normal(0,0.004)
            put('mel', seg, t, gain*0.95)
            if j == 2:
                put('mel8', vibes(hz(NOTES[idx][2]-12), len(seg)/SR*1.2), t, gain*0.8)
    put('mel', shift(SLICES[7], 12), bar_ofs(b0)+swing(12.0), gain*0.70)
    put('mel', SLICES[15], bar_ofs(b0)+swing(14.0), gain*0.9)
    put('mel8', vibes(hz(60), 1.2), bar_ofs(b0)+swing(14.0), gain*0.8)

for b in range(BARS):
    ci = b % 4
    sect = ('intro' if b < 4 else 'headA' if b < 8 else 'headB' if b < 12
            else 'chops' if b < 16 else 'headC' if b < 20 else 'out')
    if sect == 'intro':
        lay_bass(b, ci, 0.9); lay_drums(b, 0.75, busy=(b >= 2))
        if b >= 2: lay_keys(b, ci, 0.35)
    elif sect == 'headA':
        lay_bass(b, ci); lay_drums(b, 0.9); lay_keys(b, ci, 0.55)
        if ci == 0: lay_head(b, 1.0)
    elif sect == 'headB':
        lay_bass(b, ci); lay_drums(b, 1.0, busy=True); lay_keys(b, ci, 0.75)
        if ci == 0: lay_head(b, 1.0)
    elif sect == 'chops':
        lay_bass(b, ci); lay_drums(b, 1.0, busy=True); lay_keys(b, ci, 0.8)
        if ci == 0: lay_chops(b, 1.0)
    elif sect == 'headC':
        lay_bass(b, ci); lay_drums(b, 0.95, busy=(ci >= 2)); lay_keys(b, ci, 0.65)
        if ci == 0: lay_head(b, 1.0)
    else:
        if b == 20:
            lay_bass(b, 0, 0.9); lay_drums(b, 0.8)
            for m in VOICE[0]: put('keys', rhodes(hz(m), 3.0), bar_ofs(b), 0.7)
            put('mel', SLICES[15], bar_ofs(b)+swing(0.0), 0.95)
            put('mel8', vibes(hz(60), 2.0), bar_ofs(b)+swing(0.0), 0.85)
        else:
            put('ride', ride(2.8, bell=True), bar_ofs(b), 0.9)
            for m in [38,53,57,60,64]:
                put('keys' if m > 40 else 'bass',
                    rhodes(hz(m),3.6) if m > 40 else upright(hz(m),3.2), bar_ofs(b), 0.75)

# ---------------------------------------------------------------- mix
def reverb(x, mix_amt=0.22, dur=1.5, pre=0.02):
    n = int(dur*SR)
    ir = rng.standard_normal(n)*np.exp(-np.arange(n)/(0.30*SR))
    ir = lp(hp(ir, 350), 6500); ir /= np.abs(ir).max()
    wet = fftconvolve(x, ir)[:len(x)]
    wet = np.concatenate([np.zeros(int(pre*SR)), wet])[:len(x)]
    return x*(1-mix_amt*0.5) + wet*mix_amt

GAIN = {'kick':1.30,'snare':0.50,'ride':0.34,'hat':0.24,'bass':1.15,
        'keys':0.26,'mel':0.34,'mel8':0.30}
PAN  = {'kick':0.5,'snare':0.45,'ride':0.63,'hat':0.38,'bass':0.5,
        'keys':0.36,'mel':0.52,'mel8':0.44}
WET  = {'kick':0.04,'snare':0.20,'ride':0.24,'hat':0.10,'bass':0.04,
        'keys':0.26,'mel':0.28,'mel8':0.30}

L = np.zeros(total); R = np.zeros(total); STEMS = {}
for k, sig in mix.items():
    s = sig*GAIN[k]
    if k == 'mel':
        s = hp(s, 300)
        s = peakdip(s, 700, 1.1, -3.0)        # tame the sine's honk
    if k == 'mel8':  s = lp(s, 3500)
    if k == 'bass':  s = lp(s, 900)
    if k == 'keys':  s = peakdip(s, 480, 1.0, -2.5)
    s = reverb(s, mix_amt=WET[k])
    p = PAN[k]
    sl, sr_ = s*np.sqrt(1-p), s*np.sqrt(p)
    L += sl; R += sr_
    STEMS[k] = np.stack([sl, sr_], 1)

st = np.stack([L, R], 1)
st = hp(st.T, 28).T                            # rumble filter
pk = np.abs(st).max()
st = st/pk*0.90                                # normalise, no crushing
over = np.abs(st) > 0.86                       # gentle soft-knee on peaks only
st[over] = np.sign(st[over])*(0.86 + 0.14*np.tanh((np.abs(st[over])-0.86)/0.14))
end = int((BARS*BAR + 3.0)*SR)
st = st[:end]
st[-int(0.6*SR):] *= np.linspace(1,0,int(0.6*SR))[:,None]
sf.write('jazz_groove.wav', st, SR)
import os
os.makedirs('stems', exist_ok=True)
for k, v in STEMS.items():
    v = v[:end]/pk*0.90
    v[-int(0.6*SR):] *= np.linspace(1,0,int(0.6*SR))[:,None]
    sf.write(f'stems/{k}.wav', v, SR)
print('stems:', ', '.join(sorted(STEMS)))
r = np.sqrt((st**2).mean())
print(f"length {len(st)/SR:.2f}s  peak={np.abs(st).max():.3f}  "
      f"RMS={20*np.log10(r):.1f} dBFS  crest={20*np.log10(np.abs(st).max()/r):.1f} dB")

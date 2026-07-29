"""Toned-down arrangement, swappable lead instrument.
   Usage: python song2.py            -> renders all four versions
"""
import numpy as np, soundfile as sf, os
from scipy.signal import butter, lfilter, fftconvolve

SR, BPM, SWING = 44100, 114.0, 0.62
BEAT = 60.0/BPM; BAR = 4*BEAT
BARS = 18

def lp(x, fc, o=2): b,a = butter(o, min(fc,SR/2-1)/(SR/2), 'low');  return lfilter(b,a,x)
def hp(x, fc, o=2): b,a = butter(o, min(fc,SR/2-1)/(SR/2), 'high'); return lfilter(b,a,x)
def bp(x, f1, f2, o=2):
    b,a = butter(o,[f1/(SR/2), min(f2,SR/2-1)/(SR/2)],'band'); return lfilter(b,a,x)
def peakdip(x, fc, q, g):
    A=10**(g/40); w0=2*np.pi*fc/SR; al=np.sin(w0)/(2*q)
    b=[1+al*A,-2*np.cos(w0),1-al*A]; a=[1+al/A,-2*np.cos(w0),1-al/A]
    return lfilter(np.array(b)/a[0], np.array(a)/a[0], x)
def hz(m): return 440.0*2**((m-69)/12)
def swing(pos):
    b,f = np.floor(pos), pos-np.floor(pos)
    f = f*(SWING/0.5) if f < 0.5 else SWING+(f-0.5)*((1-SWING)/0.5)
    return (b+f)*BEAT

# ------------------------------------------------------------------ voices
def mk(rng):
    def piano(f, dur, amp=1.0):
        n=int(dur*SR); t=np.arange(n)/SR; B=0.00035; y=np.zeros(n)
        for k in range(1, max(int(min(20,(SR/2.3)/f)),1)+1):
            fk=f*k*np.sqrt(1+B*k*k)
            ak=(1.0/k**1.18)*(1.0 if k%2 else 0.78)
            y+=ak*np.sin(2*np.pi*fk*t+rng.uniform(0,2*np.pi))*np.exp(-t/(1.15/(1+0.5*k)))
        y+=lp(rng.standard_normal(n),3200)*np.exp(-t/0.005)*0.30
        a=max(int(0.0025*SR),1); y[:a]*=np.linspace(0,1,a)
        r=min(int(0.06*SR),n//3); y[-r:]*=np.linspace(1,0,r)
        return y/(np.abs(y).max()+1e-9)*amp

    def guitar(f, dur, amp=1.0):
        n=int(dur*SR); N=max(int(round(SR/f)),3)
        buf=lp(rng.standard_normal(N),1900); buf/= (np.abs(buf).max()+1e-9)
        out=np.empty(n); b=buf.copy(); i=0; rho=0.9972; s=0.42
        for k in range(n):
            cur=b[i]; out[k]=cur
            b[i]=rho*((1-s)*cur+s*b[(i+1)%N]); i=(i+1)%N
        out=lp(out,2600)
        a=max(int(0.002*SR),1); out[:a]*=np.linspace(0,1,a)
        r=min(int(0.05*SR),n//3); out[-r:]*=np.linspace(1,0,r)
        return out/(np.abs(out).max()+1e-9)*amp

    def bassv(f, dur, amp=1.0, solo=False):
        n=int(dur*SR); t=np.arange(n)/SR
        y=np.sin(2*np.pi*f*t)
        if solo:            # solo voice: richer, longer-lived harmonics for definition
            y+=0.50*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.55)
            y+=0.30*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.40)
            y+=0.20*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.28)
            y+=0.15*np.sin(2*np.pi*5*f*t)*np.exp(-t/0.20)
            y+=0.10*np.sin(2*np.pi*6*f*t)*np.exp(-t/0.15)
            y+=0.07*np.sin(2*np.pi*7*f*t)*np.exp(-t/0.11)
            y=np.tanh(y*1.5)/1.2                     # a little growl
            y*=1+0.05*np.sin(2*np.pi*5.5*t)
        else:
            y+=0.44*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.30)
            y+=0.20*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.16)
            y+=0.10*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.08)
        y+=lp(rng.standard_normal(n),2400)*np.exp(-t/0.013)*0.45
        e=np.exp(-t/(0.85 if solo else 0.45))
        a=max(int(0.006*SR),1); e[:a]=np.linspace(0,1,a)
        r=min(int(0.05*SR),n//3); e[-r:]*=np.linspace(1,0,r)
        y=np.tanh(y*e*1.2)
        return y/(np.abs(y).max()+1e-9)*amp

    def rhodes(f, dur, amp=0.5):
        n=int(dur*SR); t=np.arange(n)/SR
        y=np.sin(2*np.pi*f*t+2.4*np.exp(-t/0.13)*np.sin(2*np.pi*f*t))
        y+=0.16*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.25)
        e=np.exp(-t/max(dur*0.5,0.35)); a=max(int(0.004*SR),1); e[:a]=np.linspace(0,1,a)
        r=min(int(0.05*SR),n//3); e[-r:]*=np.linspace(1,0,r)
        return y*e*(1+0.08*np.sin(2*np.pi*4.6*t))*amp

    def kick(dur=0.50, amp=1.0):
        n=int(dur*SR); t=np.arange(n)/SR
        f=45+82*np.exp(-t/0.030)
        e=np.exp(-t/0.14); e[0]=0
        y=np.sin(2*np.pi*np.cumsum(f)/SR)*e
        y+=0.45*np.sin(2*np.pi*52*t)*np.exp(-t/0.10)
        y+=lp(rng.standard_normal(n),1800)*np.exp(-t/0.004)*0.20
        return y*amp

    def brush(dur=0.34, amp=1.0, ghost=False, swirl=False):
        n=int(dur*SR); t=np.arange(n)/SR
        if swirl:                                   # brush sweep, not a hit
            nz=bp(rng.standard_normal(n),700,5200)
            return nz*np.sin(np.pi*t/dur)**2*amp*0.5
        nz=bp(rng.standard_normal(n),900,7000)
        y=nz*np.exp(-t/(0.035 if ghost else 0.070))
        if not ghost:
            y+=(np.sin(2*np.pi*197*t)+0.6*np.sin(2*np.pi*331*t))*np.exp(-t/0.05)*0.26
        return y*amp*(0.28 if ghost else 1.0)

    def ride(dur=1.4, amp=1.0):
        n=int(dur*SR); t=np.arange(n)/SR; y=np.zeros(n)
        for p,g in [(523,.5),(789,.42),(1187,.34),(1631,.28),(2417,.22),(3319,.16),(4703,.11)]:
            y+=g*np.sin(2*np.pi*p*(1+rng.uniform(-.01,.01))*t)*np.exp(-t/0.40)
        y+=hp(rng.standard_normal(n),5000)*np.exp(-t/0.28)*0.95
        e=np.exp(-t/1.0); e[0]=0; a=max(int(0.0015*SR),1); e[:a]=np.linspace(0,1,a)
        r=min(int(0.05*SR),n//3); e[-r:]*=np.linspace(1,0,r)
        return y*e*amp*0.32

    def chick(dur=0.16, amp=1.0):
        n=int(dur*SR); t=np.arange(n)/SR
        return hp(rng.standard_normal(n),6200)*np.exp(-t/0.022)*amp*0.65
    return piano, guitar, bassv, rhodes, kick, brush, ride, chick

# ------------------------------------------------------------------ material
NOTES=[(0.000,0.627,74),(0.627,0.708,72),(0.708,0.929,71),(0.929,1.277,76),
       (1.277,1.765,77),(2.357,2.752,71),(2.891,3.019,76),(3.019,3.855,74),
       (3.936,4.470,72),(4.470,4.841,71),(4.841,4.934,75),(4.992,5.143,72),
       (5.143,5.259,71),(5.259,5.387,76),(5.387,6.107,77),(6.107,6.687,72)]
HEAD=[(0.00,0),(1.25,1),(1.50,2),(1.75,3),(2.50,4),(4.50,5),(5.40,6),(5.75,7),
      (7.50,8),(8.50,9),(9.25,10),(9.50,11),(9.75,12),(10.00,13),(10.25,14),(11.50,15)]
VOICE=[[53,57,60,64],[53,57,59,64],[52,55,59,62],[52,55,61,65]]
WALK =[[38,41,45,44],[43,47,50,49],[48,47,45,43],[45,43,41,40]]
ROOT =[38,43,48,45]
COMP =[[0.0,2.5],[1.5,3.0],[0.0,2.5],[1.5,3.0]]        # two stabs a bar
GRACE={1,6,10}

CFG={ 'piano':  dict(lead='piano',  tr=0,   ring=0.95, walk=True,  comp='piano',  lg=0.52, ctr=0),
      'guitar': dict(lead='guitar', tr=-12, ring=1.10, walk=True,  comp='rhodes', lg=0.60, ctr=0),
      # bass lead sings at 247-350Hz, so lift the comping an octave clear of it
      'bass':   dict(lead='bass',   tr=-12, ring=0.75, walk=False, comp='rhodes', lg=0.62, ctr=12),
      'soft':   dict(lead='slice',  tr=0,   ring=0.0,  walk=True,  comp='rhodes', lg=0.40, ctr=0) }

def build(name):
    cfg=CFG[name]; rng=np.random.default_rng(11)
    piano,guitar,bassv,rhodes,kick,brush,ride,chick = mk(rng)
    total=int(BARS*BAR*SR)+SR*4
    buses=['kick','snare','ride','hat','bass','keys','lead']
    mix={k:np.zeros(total) for k in buses}
    def put(bus,sig,t,g=1.0):
        i=max(0,int(t*SR))
        if i>=total or len(sig)==0: return
        j=min(i+len(sig),total); mix[bus][i:j]+=sig[:j-i]*g

    if cfg['lead']=='slice':
        mel,_=sf.read('mel_decoded.wav'); SL=[]
        for s,e,m in NOTES:
            seg=mel[int(s*SR):int(e*SR)].copy()
            f=min(int(0.004*SR),len(seg)//4)
            seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f); SL.append(seg)

    def lead_note(m, dur, amp):
        L=cfg['lead']
        if L=='piano':  return piano(hz(m),dur,amp)
        if L=='guitar': return guitar(hz(m),dur,amp)
        if L=='bass':   return bassv(hz(m),dur,amp,solo=True)
        return None

    def lay_head(b0, g=1.0):
        for i,(pos,idx) in enumerate(HEAD):
            t=b0*BAR+swing(pos)+rng.normal(0,0.005)
            nxt=HEAD[i+1][0] if i+1<len(HEAD) else pos+4.0
            gap=(nxt-pos)*BEAT
            v=g*(0.62 if idx in GRACE else 1.0)*rng.uniform(0.88,1.0)
            if cfg['lead']=='slice':
                put('lead',SL[idx],t,v)
            else:
                dur=min(gap+cfg['ring'],3.0)
                put('lead',lead_note(NOTES[idx][2]+cfg['tr'],dur,0.9),t,v)

    def lay_bass(b,ci,g=1.0,feel='walk'):
        # 'two' = root on 1 and 3 (half-time feel); 'walk' = quarter-note line
        if feel=='walk' and cfg['walk']:
            for k,m in enumerate(WALK[ci]):
                put('bass',bassv(hz(m),BEAT*1.02),b*BAR+swing(k)+rng.normal(0,0.006),
                    g*rng.uniform(0.85,1.0))
        else:
            # when there's no walking line the root carries the whole bottom end
            gr = 1.05 if not cfg['walk'] else 0.62
            for k,m in [(0,ROOT[ci]),(2,WALK[ci][2])]:
                put('bass',bassv(hz(m),BEAT*1.9),b*BAR+swing(k)+rng.normal(0,0.006),
                    g*gr*rng.uniform(0.9,1.0))

    def lay_drums(b,g=1.0,ghost=False,swirl=True):
        o=b*BAR
        for k in [0,1,1.5,2,3,3.5]:
            acc=1.0 if k in (0,2) else 0.68
            put('ride',ride(),o+swing(k)+rng.normal(0,0.005),g*acc*rng.uniform(0.88,1.02))
        for k in [1,3]:
            put('hat',chick(),o+swing(k)+rng.normal(0,0.004),g*rng.uniform(0.8,1.0))
            put('snare',brush(),o+swing(k)+rng.normal(0,0.006),g*0.48*rng.uniform(0.88,1.02))
        if swirl:
            put('snare',brush(dur=BEAT*1.8,swirl=True),o+swing(2.0),g*0.30)
        if ghost:
            put('snare',brush(ghost=True),o+swing(float(rng.choice([1.5,3.5]))),g*0.7)
        for k in [0,2]:
            put('kick',kick(),o+swing(k)+rng.normal(0,0.005),g*0.14)   # feather only

    def lay_keys(b,ci,g=1.0):
        fn = piano if cfg['comp']=='piano' else rhodes
        for k in COMP[ci]:
            t=b*BAR+swing(k)+rng.normal(0,0.008)
            for j,m in enumerate(VOICE[ci]):
                put('keys',fn(hz(m+cfg['ctr']),BEAT*1.9,0.6),t+j*0.007,g*rng.uniform(0.82,1.0))

    for b in range(BARS):
        ci=b%4
        if b<4:                                   # intro
            lay_bass(b,ci,0.85,'two'); lay_drums(b,0.62,swirl=(b>=1))
            if b>=2: lay_keys(b,ci,0.30)
        elif b<8:                                 # head 1
            lay_bass(b,ci,0.95,'two'); lay_drums(b,0.72); lay_keys(b,ci,0.38)
            if ci==0: lay_head(b,1.0)
        elif b<12:                                # head 2
            lay_bass(b,ci,1.0,'walk'); lay_drums(b,0.82,ghost=True); lay_keys(b,ci,0.48)
            if ci==0: lay_head(b,1.0)
        elif b<16:                                # head 3, thinning
            lay_bass(b,ci,0.92,'walk'); lay_drums(b,0.70,ghost=(ci<2)); lay_keys(b,ci,0.40)
            if ci==0: lay_head(b,0.95)
        elif b==16:                               # ending
            lay_bass(b,0,0.8,'two'); lay_drums(b,0.55,swirl=True)
            fn = piano if cfg['comp']=='piano' else rhodes
            for m in VOICE[0]: put('keys',fn(hz(m+cfg['ctr']),3.2,0.6),b*BAR,0.55)
            if cfg['lead']=='slice': put('lead',SL[15],b*BAR,0.85)
            else: put('lead',lead_note(NOTES[15][2]+cfg['tr'],2.6,0.9),b*BAR,0.9)
        else:
            put('ride',ride(2.6),b*BAR,0.55)

    # -------------------------------------------------------------- mix
    def reverb(x,amt,dur=1.4):
        n=int(dur*SR)
        ir=rng.standard_normal(n)*np.exp(-np.arange(n)/(0.28*SR))
        ir=lp(hp(ir,350),6000); ir/=np.abs(ir).max()
        wet=fftconvolve(x,ir)[:len(x)]
        wet=np.concatenate([np.zeros(int(0.02*SR)),wet])[:len(x)]
        return x*(1-amt*0.5)+wet*amt
    G={'kick':1.20,'snare':0.42,'ride':0.26,'hat':0.18,'bass':1.05,'keys':0.24,'lead':cfg['lg']}
    P={'kick':0.5,'snare':0.45,'ride':0.62,'hat':0.40,'bass':0.5,'keys':0.36,'lead':0.52}
    W={'kick':0.04,'snare':0.18,'ride':0.20,'hat':0.08,'bass':0.04,'keys':0.22,'lead':0.24}
    stems={}
    for k,sig in mix.items():
        s=sig*G[k]
        if k=='lead' and cfg['lead']=='slice': s=peakdip(hp(s,300),700,1.1,-3.0)
        if k=='lead' and cfg['lead']=='bass':  s=lp(s,5000)
        if k=='bass': s=lp(s,900)
        if k=='keys': s=peakdip(s,480,1.0,-2.0)
        s=hp(reverb(s,W[k]),28)                       # linear, so stems still sum
        p=P[k]
        stems[k]=np.stack([s*np.sqrt(1-p), s*np.sqrt(p)],1)

    # --- balance lead vs backing, measured ONLY where the lead is sounding
    TARGET_DB=5.0
    lm=np.abs(stems['lead']).mean(1); act=lm>lm.max()*0.01      # -40 dB gate
    back=sum(v for k,v in stems.items() if k!='lead')
    lr=np.sqrt((stems['lead'][act]**2).mean()); br=np.sqrt((back[act]**2).mean())
    corr=float(np.clip(10**(TARGET_DB/20)*br/lr, 0.2, 5.0))
    stems['lead']=stems['lead']*corr

    st=sum(stems.values())
    end=int((BARS*BAR+3.0)*SR); st=st[:end]
    fade=np.linspace(1,0,int(0.7*SR))[:,None]; st[-len(fade):]*=fade
    g=10**(-18/20)/np.sqrt((st**2).mean()); st=st*g            # loudness match
    if np.abs(st).max()>0.89:
        sc=0.89/np.abs(st).max(); st*=sc; g*=sc
    ov=np.abs(st)>0.84
    st[ov]=np.sign(st[ov])*(0.84+0.16*np.tanh((np.abs(st[ov])-0.84)/0.16))
    sf.write(f'groove_{name}.wav',st,SR)
    r=np.sqrt((st**2).mean()); a=act[:end]
    lr2=np.sqrt((stems['lead'][:end][a]**2).mean())
    br2=np.sqrt((back[:end][a]**2).mean())
    print(f"{name:7} {len(st)/SR:5.2f}s peak={np.abs(st).max():.3f} "
          f"RMS={20*np.log10(r):6.1f}dBFS crest={20*np.log10(np.abs(st).max()/r):5.1f}dB "
          f"lead={20*np.log10(lr2/br2):+5.1f}dB (corr {20*np.log10(corr):+5.1f}dB)")
    return stems, end, g

if __name__=='__main__':
    for nm in ['piano','guitar','bass','soft']:
        stems,end,g=build(nm)
        os.makedirs(f'stems_{nm}',exist_ok=True)
        for k,v in stems.items():
            v=v[:end]*g
            v[-int(0.7*SR):]*=np.linspace(1,0,int(0.7*SR))[:,None]
            sf.write(f'stems_{nm}/{k}.wav',v,SR)

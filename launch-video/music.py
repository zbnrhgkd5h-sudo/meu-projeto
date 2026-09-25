"""Synthesises the soundtrack for the launch film (120 BPM, 48 s) → music.wav.

Everything is generated from oscillators and noise with numpy, so the track is
royalty-free and every hit lines up exactly with the timeline in index.html.
"""
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
DUR = 48.0
BPM = 120
BEAT = 60 / BPM
BAR = BEAT * 4
N = int(SR * DUR)
rng = np.random.default_rng(7)

L = np.zeros(N)
R = np.zeros(N)
duck = np.ones(N)  # sidechain envelope driven by the kick


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100), 'low', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def add(sig, t, gain=1.0, pan=0.0, bus='main'):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    gl, gr = gain * np.sqrt((1 - pan) / 2), gain * np.sqrt((1 + pan) / 2)
    if bus == 'duck':
        sig = sig * duck[i:i + len(sig)]
    L[i:i + len(sig)] += sig * gl
    R[i:i + len(sig)] += sig * gr


def env(n, a=0.005, d=0.2, curve=4.0):
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / max(a, 1e-4)) * np.exp(-np.maximum(0, tt - a) * curve / max(d, 1e-4))
    return e


# ---------------------------------------------------------------- instruments
def kick(dur=0.45, punch=1.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 45 + 110 * np.exp(-tt * 30) * punch
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt * 7)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-tt * 250) * 0.3
    return np.tanh((body + click) * 1.6)


def clap():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 6000)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        e += (tt >= off) * np.exp(-np.maximum(0, tt - off) * (90 if k < 2 else 16))
    return noise * e * 0.6


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR)
    tt = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500) * np.exp(-tt * (18 if open_ else 80)) * 0.35


def saw(freq, n, detune=0.0):
    tt = np.arange(n) / SR
    ph = (tt * freq * (1 + detune)) % 1.0
    return 2 * ph - 1


def pad(notes, dur, cutoff=1800):
    n = int(dur * SR)
    out = np.zeros(n)
    for m in notes:
        f = midi(m)
        for dt in (-0.006, 0.0, 0.007):
            out += saw(f, n, dt)
    out = lp(out / (len(notes) * 3), cutoff, 2)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.25) * np.minimum(1, (dur - tt) / 0.3).clip(0, 1)
    return out * e


def pluck(m, dur=0.35, bright=4500):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = midi(m)
    x = saw(f, n) + 0.5 * np.sign(np.sin(2 * np.pi * f * 2 * tt))
    x = lp(x, bright) * np.exp(-tt * 9)
    return x * np.minimum(1, tt / 0.003)


def bass(m, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = midi(m)
    x = np.sin(2 * np.pi * f * tt) + 0.35 * lp(saw(f, n), 600)
    return x * np.minimum(1, tt / 0.01) * np.exp(-tt * 2.5) * np.clip((dur - tt) / 0.03, 0, 1)


def whoosh(dur=0.9, peak=0.75, rev=False):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # sweep a band-pass by processing in chunks
    out = np.zeros(n)
    chunk = 1024
    for s in range(0, n, chunk):
        p = s / n
        fc = 300 + 7000 * (p if not rev else 1 - p) ** 2
        seg = noise[s:s + chunk]
        out[s:s + chunk] = bp(seg, max(80, fc * 0.5), min(18000, fc * 1.6), 1)
    shape = np.where(tt < dur * peak, (tt / (dur * peak)) ** 2, np.exp(-(tt - dur * peak) * 9))
    return out * shape * 0.8


def riser(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    p = tt / dur
    f = 200 * 2 ** (p * 3)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    noise = hp(rng.standard_normal(n), 2000) * 0.5
    return (tone + noise * p) * p ** 2


def impact(dur=2.5):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 30 + 70 * np.exp(-tt * 12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    crash = hp(rng.standard_normal(n), 4000) * np.exp(-tt * 3.0) * 0.35
    return np.tanh(boom * 1.8) + crash


def tick():
    n = int(0.03 * SR)
    tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), 2000, 7000) * np.exp(-tt * 300) * 0.5


def blip(m=84):
    n = int(0.18 * SR)
    tt = np.arange(n) / SR
    f = midi(m) * (1 + 0.5 * np.exp(-tt * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 25) * 0.4


# ---------------------------------------------------------------- arrangement
# I–V–vi–IV in C, one chord per bar.
CHORDS = [
    (48, [60, 64, 67, 74]),  # C  add9
    (43, [59, 62, 67, 69]),  # G  (B D G A)
    (45, [60, 64, 69, 71]),  # Am add9
    (41, [60, 65, 69, 76]),  # F  maj7-ish
]
ARP = [0, 1, 2, 3, 2, 1, 3, 2]


def chord_at(t):
    return CHORDS[int(t // BAR) % 4]


# kick pattern first (also builds the sidechain envelope)
kicks = []
t = 0.0
while t < DUR:
    full = (8 <= t < 39) or (40.5 <= t < 43)
    half = 4 <= t < 8 and (round(t / BEAT) % 2 == 0)
    if full or half:
        kicks.append(t)
    t += BEAT
for kt in kicks:
    i = int(kt * SR)
    n = int(0.3 * SR)
    seg = 1 - 0.65 * np.exp(-np.arange(n) / SR * 11)
    duck[i:i + n] = np.minimum(duck[i:i + n], seg[: len(duck[i:i + n])])

# pad: whole track, darker in the intro, open from the logo reveal
for b in range(int(DUR / BAR)):
    t0 = b * BAR
    root, notes = CHORDS[b % 4]
    cutoff = 700 if t0 < 4 else (1400 if t0 < 8 else 2400)
    if t0 >= 43:
        cutoff = 1600
    g = 0.22 if t0 < 44 else 0.2
    add(pad(notes, BAR + 0.3, cutoff), t0, g, -0.25, 'duck')
    add(pad([x + 12 for x in notes[:2]], BAR + 0.3, cutoff), t0, g * 0.35, 0.3, 'duck')

# final sustained chord under the CTA
add(pad([48, 55, 60, 64, 67, 74], 3.2, 2000), 45.6, 0.3, 0.0)

# arp: 16ths from the logo reveal onward, dropping out in the proof breakdown
t = 4.0
step = 0
while t < 46:
    if not (39 <= t < 40.5):
        root, notes = chord_at(t)
        m = notes[ARP[step % 8]] + 12
        g = 0.09 if t < 8 else 0.12
        add(pluck(m, 0.3, 3000 if t < 8 else 5200), t, g, 0.45 if step % 2 else -0.45, 'duck')
    t += BEAT / 4
    step += 1

# bass: 8ths on the chord root during the groove
t = 8.0
while t < 43:
    if not (39 <= t < 40.5):
        root, _ = chord_at(t)
        add(bass(root - 12 + (12 if int(t / (BEAT / 2)) % 4 == 3 else 0), BEAT / 2 * 0.9), t, 0.32, 0.0, 'duck')
    t += BEAT / 2

# drums
for kt in kicks:
    add(kick(), kt, 0.9)
t = 8.0
while t < 43:
    beat_i = round(t / BEAT)
    if not (39 <= t < 40.5):
        if beat_i % 2 == 1:
            add(clap(), t, 0.55, 0.05)
        add(hat(), t + BEAT / 2, 0.5, 0.3)
        if beat_i % 4 == 3:
            add(hat(True), t + BEAT / 2, 0.35, -0.3)
    t += BEAT
# intro: ticking hats + low hits on each word
for k in range(16):
    add(hat(), 0.0 + k * BEAT / 2, 0.25 + 0.1 * (k % 2), 0.4 if k % 2 else -0.4)
for wt in (1.15, 2.15):
    add(kick(0.8, 0.5), wt, 0.7)
    add(blip(72), wt, 0.25)
add(kick(0.9, 0.6), 3.05, 0.8)

# risers, impacts and transition whooshes
add(riser(1.9), 2.1, 0.55)
add(impact(3.0), 4.0, 0.95)
add(riser(1.4), 39.1, 0.5)
# snare roll into the proof drop
for k in range(12):
    add(clap(), 39.5 + k * (1.0 / 12), 0.15 + k * 0.03, 0.0)
add(impact(2.0), 40.5, 0.75)
add(impact(3.5), 43.0, 0.7)
for tt in (8, 13, 18, 23, 30, 35, 39):
    add(whoosh(0.8, 0.8), tt - 0.62, 0.55, -0.2)

# UI foley: power failures, pops for cards/pills/tags, final click
def power_down(dur=0.9):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = 120 * np.exp(-tt * 3.5) + 25
    hum = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 3) / SR)
    zap = hp(rng.standard_normal(n), 1500) * np.exp(-tt * 18) * 0.6
    return (hum * np.exp(-tt * 2.5) + zap) * 0.8


def alarm(n_beeps=3):
    out = np.zeros(int(0.6 * n_beeps * SR))
    for k in range(n_beeps):
        m = int(0.18 * SR)
        tt = np.arange(m) / SR
        b = np.sign(np.sin(2 * np.pi * 1320 * tt)) * np.minimum(1, (0.18 - tt) / 0.01) * 0.25
        i = int(k * 0.3 * SR)
        out[i:i + m] += lp(b, 5000)
    return out


add(power_down(1.0), 0.5, 0.8)
add(alarm(2), 1.0, 0.25, 0.2)
add(power_down(0.8), 25.0, 0.8)
add(alarm(3), 25.1, 0.3, -0.2)
for tt in (8.35, 8.51, 8.67, 8.83, 8.99, 9.6, 9.88, 10.16, 10.44, 14.2, 14.7, 15.2, 15.5, 15.8, 16.1, 16.4,
           27.5, 27.9, 28.3, 28.6, 30.8, 31.2, 31.9, 32.35, 32.8, 44.1):
    add(blip(88 + int(tt * 10) % 5), tt, 0.28, rng.uniform(-0.5, 0.5))
for k, tt in enumerate((19.1, 19.8, 20.5, 21.2, 21.9)):
    add(whoosh(0.5, 0.6), tt - 0.2, 0.25, 0.5 if k % 2 else -0.5)
add(tick(), 45.55, 1.0)
add(blip(91), 45.6, 0.35)

# ---------------------------------------------------------------- master
mix = np.stack([L, R], axis=1)
# gentle fade-out across the last second
fade = np.ones(N)
fs = int(46.8 * SR)
fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
mix *= fade[:, None]
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
mix /= np.max(np.abs(mix)) / 0.89
pcm = (mix * 32767).astype(np.int16)
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote music.wav', pcm.shape)

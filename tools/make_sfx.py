"""Placeholder sound effects, synthesized. Run: python3 tools/make_sfx.py (writes assets/sfx/*.wav)"""
import os, wave
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sfx")
os.makedirs(OUT, exist_ok=True)
SR = 22050
rng = np.random.default_rng(7)

def t(sec): return np.arange(int(SR * sec)) / SR
def env(n, a=0.002, r=0.1):
    x = np.arange(n) / SR
    return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / max(r, 1e-4))
def lp(x, k=0.2):
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y
def save(name, x, vol=0.6):
    x = np.clip(x / (np.max(np.abs(x)) + 1e-9) * vol, -1, 1)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def click(f=2400, dur=0.06, r=0.012):
    n = int(SR * dur); x = t(dur)
    return (np.sin(2 * np.pi * f * x) * 0.5 + rng.normal(0, 0.6, n)) * env(n, 0.0005, r)

save("click", click())
save("tick", click(3200, 0.04, 0.006), 0.35)
c = np.concatenate([click(1600, 0.05), np.zeros(int(SR * 0.05)), click(900, 0.12, 0.04)])
save("unlock", c)
n = int(SR * 0.35); s = lp(rng.normal(0, 1, n), 0.08) * env(n, 0.03, 0.12) + 0.3 * np.sin(2 * np.pi * 90 * t(0.35)) * env(n, 0.01, 0.1)
save("slide", s, 0.5)
n = int(SR * 0.5); x = t(0.5)
save("thunk", (np.sin(2 * np.pi * 70 * x) + 0.5 * lp(rng.normal(0, 1, n), 0.05)) * env(n, 0.002, 0.09), 0.7)
n = int(SR * 0.4); save("paper", lp(rng.normal(0, 1, n), 0.5) * env(n, 0.02, 0.08) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t(0.4))), 0.4)
n = int(SR * 0.7); m = rng.normal(0, 1, n) * env(n, 0.001, 0.05) + lp(rng.normal(0, 1, n), 0.3) * env(n, 0.05, 0.3) * 0.6
save("match", m, 0.5)
n = int(SR * 0.25); save("pickup", (np.sin(2 * np.pi * (600 + 900 * t(0.25)) * t(0.25))) * env(n, 0.005, 0.07), 0.35)
n = int(SR * 0.3); save("turn", lp(rng.normal(0, 1, n), 0.04) * np.sin(np.pi * np.arange(n) / n), 0.35)
n = int(SR * 1.4); x = t(1.4); creak = np.sin(2 * np.pi * (180 + 60 * np.sin(2 * np.pi * 3 * x)) * x) * np.sin(np.pi * np.arange(n) / n)
save("door", creak * (0.5 + 0.5 * (rng.random(n) > 0.6)), 0.5)
n = int(SR * 0.2); save("nope", np.sign(np.sin(2 * np.pi * 140 * t(0.2))) * env(n, 0.002, 0.06), 0.25)
# whisper: band-limited noise with a slow vowel-like wobble
n = int(SR * 1.8); w = lp(rng.normal(0, 1, n), 0.35) - lp(rng.normal(0, 1, n), 0.05)
save("whisper", w * (0.5 + 0.5 * np.sin(2 * np.pi * 4.5 * t(1.8))) * np.sin(np.pi * np.arange(n) / n), 0.4)
# lens: a glassy shimmer
n = int(SR * 0.6); x = t(0.6)
save("lens", sum(np.sin(2 * np.pi * f * x) for f in (880, 1320, 1975)) * env(n, 0.02, 0.2), 0.3)
# discovery chime
n = int(SR * 1.2); x = t(1.2)
save("reveal", sum(np.sin(2 * np.pi * f * x) * env(n, 0.005, 0.4 + i * 0.2) for i, f in enumerate((392, 523, 659))), 0.4)
# ambient drone loop (8 s, loops cleanly: whole cycles only)
L = 8.0; x = t(L)
dr = np.sin(2 * np.pi * 55 * x) * 0.5 + np.sin(2 * np.pi * 82.5 * x) * 0.25 + np.sin(2 * np.pi * 110 * x) * 0.15 * (0.5 + 0.5 * np.sin(2 * np.pi * x / L))
wind = lp(rng.normal(0, 1, len(x)), 0.02); wind = wind * (0.5 + 0.5 * np.sin(2 * np.pi * 2 * x / L))
fade = np.minimum(1, np.minimum(np.arange(len(x)), len(x) - np.arange(len(x))) / (SR * 0.25))
save("drone", (dr + wind * 0.8) * (0.85 + 0.15 * fade), 0.35)
# seal 2: water rushing, a glassy lamp hum, a distant foghorn, a flame catching, a ship's timber creak
n = int(SR * 1.6); x = t(1.6)
wv = lp(rng.normal(0, 1, n), 0.06) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.3 * x)) + 0.4 * lp(rng.normal(0, 1, n), 0.3) * (rng.random(n) > 0.97)
save("water", wv * np.sin(np.pi * np.arange(n) / n), 0.5)
n = int(SR * 1.5); x = t(1.5)
save("hum", (np.sin(2 * np.pi * 110 * x) + 0.5 * np.sin(2 * np.pi * 220.5 * x) + 0.2 * np.sin(2 * np.pi * 331 * x)) * env(n, 0.3, 1.2), 0.35)
n = int(SR * 2.6); x = t(2.6)
hn = np.sign(np.sin(2 * np.pi * 73 * x)) * 0.4 + np.sin(2 * np.pi * 73 * x) + 0.6 * np.sin(2 * np.pi * 110 * x)
save("horn", lp(hn, 0.08) * np.minimum(1, x / 0.4) * np.minimum(1, (2.6 - x) / 0.9), 0.45)
n = int(SR * 0.9); save("flame", lp(rng.normal(0, 1, n), 0.15) * env(n, 0.04, 0.35) + rng.normal(0, 1, n) * env(n, 0.001, 0.03) * 0.5, 0.45)
n = int(SR * 1.1); x = t(1.1)
save("creak", np.sin(2 * np.pi * (90 + 40 * x) * x) * (rng.random(n) > 0.5) * np.sin(np.pi * np.arange(n) / n), 0.4)
print("sfx written to", os.path.abspath(OUT))

"""Seal 9 art: the drowned stair (room 17) and the inside of the cabinet (room 18).
Rule: 16 texels per world unit. Run: python3 tools/make_seal9_art.py  (writes assets/rooms/)
"""
from artkit import *

SLIME = [(10, 26, 22), (18, 42, 34), (28, 60, 48), (42, 82, 64), (60, 108, 84)]
CYC   = [(30, 36, 34), (44, 52, 48), (60, 70, 64), (78, 90, 82), (100, 112, 104)]
CABIN = [(20, 12, 10), (32, 20, 16), (46, 30, 22), (62, 42, 30), (80, 56, 40)]
GLOW, EYE, PALE = (120, 255, 220), (220, 200, 90), (200, 220, 210)
WW, WH = 240, 352

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

# ================= room 17: the drowned stair =================
def cyclopean(seed):
    img = grain(WW, WH, CYC, seed); d = ImageDraw.Draw(img); rnd = random.Random(seed)
    y = 0
    while y < WH:   # huge blocks, none of them square
        h = rnd.randrange(30, 70); x = rnd.randrange(-40, 0)
        while x < WW:
            w = rnd.randrange(40, 110); sk = rnd.randrange(-10, 11)
            d.polygon([(x, y), (x + w, y + sk), (x + w + sk, y + h + sk), (x + sk, y + h)], outline=CYC[0])
            x += w
        y += h
    for i in range(60):
        x, y = rnd.randrange(WW), rnd.randrange(WH); d.line([x, y, x + rnd.randrange(-3, 4), y + rnd.randrange(6, 20)], fill=SLIME[rnd.randrange(1, 4)])
    return img
for k, s in zip("nesw", (301, 302, 303, 304)): save(cyclopean(s), "r17_wall_" + k)
f = cyclopean(305).crop((0, 0, 240, 240)); save(f, "r17_floor")
c = cyclopean(306).crop((0, 0, 240, 240)); save(c, "r17_ceiling")
def cdoor(open_):
    img = face(80, 80, CYC, 307, 4); d = ImageDraw.Draw(img)
    if open_: d.polygon([(10, 6), (74, 14), (68, 74), (6, 66)], fill=(4, 10, 10))
    else:
        d.polygon([(10, 6), (74, 14), (68, 74), (6, 66)], fill=CYC[2], outline=CYC[0])
        d.ellipse([30, 30, 48, 48], outline=SLIME[3]); d.line([39, 24, 39, 54], fill=SLIME[3])
    return img
save(cdoor(False), "ceil_door"); save(cdoor(True), "ceil_door_open")
# the gravity slab: a 5 x 5 maze cut in its face, a pale marble, and a sink hole
SLAB = {"cols": 5, "rows": 5, "walls": [[1, 0], [3, 1], [1, 2], [2, 2], [4, 3], [0, 4], [2, 4]], "goal": [4, 4]}
def slab_face():
    img = face(96, 96, CYC, 308, 3); d = ImageDraw.Draw(img)
    x0, y0, cs = 8, 8, 16
    d.rectangle([x0 - 1, y0 - 1, x0 + cs * 5, y0 + cs * 5], fill=CYC[0])
    for r in range(5):
        for c in range(5):
            if [c, r] in SLAB["walls"]: d.rectangle([x0 + c * cs, y0 + r * cs, x0 + c * cs + cs - 1, y0 + r * cs + cs - 1], fill=CYC[3], outline=CYC[4])
            else: d.rectangle([x0 + c * cs + 1, y0 + r * cs + 1, x0 + c * cs + cs - 2, y0 + r * cs + cs - 2], fill=CYC[1])
    gx, gy = SLAB["goal"]; d.ellipse([x0 + gx * cs + 3, y0 + gy * cs + 3, x0 + gx * cs + 12, y0 + gy * cs + 12], fill=(0, 0, 0))
    return img
save(slab_face(), "slab_top")
for k, s in (("side", 309), ("front", 310)): save(face(96, 32, CYC, s, 2), "slab_" + k)
save(face(96, 96, CYC, 311, 2), "slab_bottom")
m = new(12, 12); d = ImageDraw.Draw(m); d.ellipse([1, 1, 10, 10], fill=PALE, outline=CYC[0]); d.point((4, 4), fill=(255, 255, 255)); save(m, "marble")
def dust(dirn):
    img = new(96, 32); d = ImageDraw.Draw(img); rnd = random.Random(312)
    for i in range(40):
        x, y = rnd.randrange(4, 92), rnd.randrange(4, 28); L = rnd.randrange(4, 10)
        dx = {"n": 0, "s": 0, "e": L, "w": -L}[dirn]; dy = {"n": -L // 3, "s": L // 3, "e": 0, "w": 0}[dirn]
        d.line([x, y, x + dx, y + dy], fill=(150, 160, 150))
    return img
for k in "nesw": save(dust(k), "dust_" + k)
sl = cyclopean(313).crop((60, 100, 124, 196)); d = ImageDraw.Draw(sl); d.rectangle([0, 0, 63, 95], outline=CYC[0]); save(sl, "wall_slab")
ni = new(64, 96, (4, 8, 8)); d = ImageDraw.Draw(ni); d.rectangle([0, 0, 63, 95], outline=GLOW)
d.polygon([(32, 30), (40, 46), (32, 62), (24, 46)], outline=GLOW); d.line([32, 34, 32, 58], fill=GLOW); save(ni, "niche_dream")
k = new(24, 24); d = ImageDraw.Draw(k); d.polygon([(12, 1), (22, 12), (12, 23), (2, 12)], fill=(90, 110, 100), outline=GLOW); d.line([12, 4, 12, 20], fill=GLOW); [d.line([12, 8 + i * 4, 12 + (4 - i), 6 + i * 4], fill=GLOW) for i in range(3)]; save(k, "item_elder_sign")
st = new(96, 160); d = ImageDraw.Draw(st)
for i in range(9): d.polygon([(10 + i * 3, 150 - i * 16), (86 - i * 5, 146 - i * 17), (86 - i * 5, 156 - i * 17), (10 + i * 3, 160 - i * 16)], fill=CYC[2 + i % 2], outline=CYC[0])
save(st, "wrong_stair")

# ================= room 18: inside the cabinet =================
def cab_wall(seed):
    img = grain(WW, WH, CABIN, seed); d = ImageDraw.Draw(img)
    for x in range(0, WW, 40): d.line([x, 0, x, WH], fill=CABIN[0])
    for i in range(9):
        cx, cy = 30 + (i % 3) * 90, 40 + (i // 3) * 40
        if cx < WW: d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=BRASS[1])
    return img
for k, s in zip("nesw", (321, 322, 323, 324)): save(cab_wall(s), "r18_wall_" + k)
save(grain(240, 240, CABIN, 325), "r18_floor"); save(grain(240, 240, CABIN, 326), "r18_ceiling")
ls = new(96, 32); d = ImageDraw.Draw(ls); d.rectangle([0, 0, 95, 31], fill=CABIN[0], outline=BRASS[2]); text(ls, 34, 12, "LENS", BRASS[3]); d.rectangle([24, 8, 26, 22], fill=BRASS[3]); d.rectangle([69, 8, 71, 22], fill=BRASS[3]); save(ls, "lens_socket")
ls2 = new(96, 32); d = ImageDraw.Draw(ls2); d.rectangle([0, 0, 95, 31], fill=CABIN[0], outline=GLOW); text(ls2, 34, 12, "LENS", GLOW); d.rectangle([24, 8, 26, 22], fill=GLOW); d.rectangle([69, 8, 71, 22], fill=GLOW); save(ls2, "lens_socket_full")
tp = face(144, 64, CABIN, 327, 3); d = ImageDraw.Draw(tp)
for i in range(8):
    x = 10 + i * 16; d.rectangle([x, 8, x + 9, 40], fill=CABIN[0])
    if i in (0, 1, 2, 7): d.ellipse([x + 2, 48, x + 7, 53], fill=BRASS[3])   # the engraving: which pins must be up
    else: d.ellipse([x + 2, 48, x + 7, 53], outline=BRASS[1])
save(tp, "tumbler_panel")
for up in (0, 1):
    t = new(12, 32); d = ImageDraw.Draw(t); y = 0 if up else 14; d.rectangle([2, y, 9, y + 17], fill=BRASS[2], outline=BRASS[0]); save(t, "tumbler_%d" % up)
kp = new(16, 16); d = ImageDraw.Draw(kp); d.ellipse([0, 0, 15, 15], fill=BRASS[2], outline=BRASS[0]); d.rectangle([6, 3, 9, 12], fill=CABIN[0]); save(kp, "tumbler_key")
mo = new(64, 48); d = ImageDraw.Draw(mo); d.ellipse([4, 10, 59, 40], fill=(40, 6, 10), outline=(120, 30, 40))
for x in range(10, 56, 6): d.polygon([(x, 14), (x + 4, 14), (x + 2, 22)], fill=PALE)
save(mo, "whisper_mouth")
mo2 = mo.copy(); d = ImageDraw.Draw(mo2); d.ellipse([20, 18, 43, 32], fill=(255, 200, 80)); save(mo2, "whisper_fed")
for L in "abcde":
    t = new(24, 24); d = ImageDraw.Draw(t); d.polygon([(8, 2), (16, 2), (14, 21), (10, 21)], fill=BRASS[3], outline=BRASS[0]); d.point((12, 6), fill=CABIN[0]); save(t, "item_tooth_" + L); save(t, "tooth_" + L)
nd = face(64, 96, CABIN, 328, 3); d = ImageDraw.Draw(nd); d.ellipse([20, 36, 43, 59], fill=(0, 0, 0), outline=EYE); d.ellipse([28, 44, 35, 51], fill=EYE); save(nd, "ninth_door")
nd2 = new(64, 96, (0, 0, 0)); d = ImageDraw.Draw(nd2); rnd = random.Random(329)
for i in range(60): d.point((rnd.randrange(64), rnd.randrange(96)), fill=(255, 255, 255))
save(nd2, "ninth_door_open")
pb = new(16, 16); d = ImageDraw.Draw(pb); d.rectangle([0, 0, 15, 15], fill=CABIN[1], outline=CABIN[0]); save(pb, "tooth_bin")
print("seal 9 art written to", os.path.abspath(OUT))

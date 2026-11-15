"""Seal 5 art: the Antarctic survey hut (room 9) and the ice shaft under it (room 10).
Rule: 16 texels per world unit. Run: python3 tools/make_seal5_art.py  (writes assets/rooms/)
Our own expedition and creatures (the Antarctic stories are not public domain).
"""
from artkit import *

ICE   = [(30, 60, 84), (52, 96, 124), (90, 140, 168), (150, 196, 216), (210, 236, 244)]
FROST = [(176, 200, 210), (214, 230, 236), (240, 248, 250)]
HUTW  = [(48, 36, 28), (72, 54, 40), (96, 72, 52), (122, 94, 68), (150, 118, 86)]
IRON  = [(20, 22, 26), (36, 38, 44), (54, 58, 66), (80, 86, 96), (112, 118, 128)]
FIRE  = [(140, 40, 10), (220, 110, 20), (255, 200, 80)]
PAPER = [(150, 140, 116), (200, 190, 164), (232, 224, 200)]
STAR  = [(40, 46, 40), (66, 74, 64), (96, 106, 92), (130, 142, 124), (170, 182, 160)]
GLOW  = (120, 255, 220)
RED2, BLU2, GRN2 = (170, 40, 40), (50, 80, 170), (50, 140, 70)

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def frost_edge(img, depth=10, seed=0):
    px = img.load(); rnd = random.Random(seed); w, h = img.size
    for y in range(h):
        for x in range(w):
            e = min(x, y, w - 1 - x, h - 1 - y)
            if e < depth and rnd.random() < (depth - e) / depth * 0.8:
                px[x, y] = FROST[rnd.randrange(3)] + (255,)

WW, WH = 240, 352
def hut_wall(seed):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            c = HUTW[2] if (y // 18) % 2 else HUTW[3]
            if y % 18 == 0: c = HUTW[0]
            elif rnd.random() < 0.03: c = HUTW[1]
            px[x, y] = c + (255,)
    frost_edge(img, 26, seed)
    return img
for k, s in zip("nesw", (121, 122, 123, 124)):
    save(hut_wall(s), "r9_wall_" + k)
f = face(240, 240, HUTW, 125, 0); frost_edge(f, 20, 126); save(f, "r9_floor")
c = hut_wall(127).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c)
for x in range(10, 230, 14): d.polygon([(x, 0), (x + 6, 0), (x + 3, 10 + (x * 7) % 26)], fill=FROST[2])
save(c, "r9_ceiling")
def stove(lit):
    img = face(64, 96, IRON, 128, 2); d = ImageDraw.Draw(img)
    d.rectangle([12, 40, 51, 70], fill=IRON[0], outline=IRON[3])
    if lit:
        for i in range(20): r_ = random.Random(i + lit * 50); d.point((r_.randrange(14, 50), r_.randrange(48, 69)), fill=FIRE[r_.randrange(3)])
        d.rectangle([14, 62, 49, 68], fill=FIRE[lit - 1 if lit <= 3 else 2])
    d.rectangle([28, 0, 35, 12], fill=IRON[2])
    return img
for h in range(4): save(stove(h), "hstove_%d" % h)
save(face(32, 96, IRON, 129), "iron_side_32x96")
def hwin(heat):
    img = new(64, 64, HUTW[1]); d = ImageDraw.Draw(img); d.rectangle([4, 4, 59, 59], fill=(220, 230, 240))
    d.rectangle([4, 40, 59, 59], fill=(240, 246, 250)); d.line([4, 40, 59, 38], fill=(200, 214, 224))
    for x, col, num in ((14, RED2, "3"), (32, BLU2, "8"), (50, GRN2, "1")):
        d.line([x, 24, x, 46], fill=HUTW[0]); d.rectangle([x + 1, 24, x + 6, 28], fill=col)
        if heat >= 2: text(img, x - 4, 34, num, INK)
    if heat == 0:
        frost_edge(img, 40, 130)
    elif heat == 1:
        frost_edge(img, 12, 131)
    d.rectangle([30, 4, 33, 59], fill=HUTW[1])
    return img
for h in range(4): save(hwin(min(h, 2)), "hwin_%d" % h)
def therm(h):
    img = new(12, 48); d = ImageDraw.Draw(img); d.rectangle([3, 0, 8, 47], fill=PAPER[2], outline=IRON[0]); d.ellipse([2, 40, 9, 47], fill=RED2)
    d.rectangle([5, 36 - h * 10, 6, 42], fill=RED2)
    for k in range(4): d.line([8, 36 - k * 10, 9, 36 - k * 10], fill=INK)
    return img
for h in range(4): save(therm(h), "htherm_%d" % h)
dk = face(112, 64, HUTW, 132, 2); save(dk, "hdesk_front"); save(face(112, 40, HUTW, 133), "hut_top_112x40"); save(face(40, 64, HUTW, 134), "hut_side_40x64")
lg = new(40, 24); d = ImageDraw.Draw(lg); d.polygon([(0, 22), (19, 18), (19, 2), (0, 6)], fill=PAPER[2], outline=HUTW[0]); d.polygon([(39, 22), (20, 18), (20, 2), (39, 6)], fill=PAPER[2], outline=HUTW[0])
for y in range(8, 18, 2): d.line([3, y, 16, y - 2], fill=INK); d.line([23, y - 2, 36, y], fill=INK)
save(lg, "survey_log")
bk = new(112, 48); d = ImageDraw.Draw(bk); d.rectangle([0, 10, 111, 30], fill=(110, 30, 30), outline=HUTW[0]); d.rectangle([0, 30, 111, 36], fill=HUTW[2])
for x in (2, 106): d.rectangle([x, 30, x + 3, 47], fill=HUTW[1])
save(bk, "bunk")
hd = face(72, 144, HUTW, 135, 3); frost_edge(hd, 30, 136); save(hd, "hut_door")
bench = face(96, 32, HUTW, 137, 2); save(bench, "bench_front"); save(face(96, 32, HUTW, 138), "hut_top_96x32"); save(face(32, 32, HUTW, 139), "hut_side_32x32")
def hatch(heat):
    img = face(80, 80, HUTW, 140, 3); d = ImageDraw.Draw(img); d.rectangle([30, 34, 49, 45], fill=IRON[2])
    if heat < 3:
        px = img.load(); rnd = random.Random(141)
        for y in range(80):
            for x in range(80):
                if (x + y) % 2 == 0 and rnd.random() < 0.9: px[x, y] = ICE[3 + (x * y) % 2] + (255,)
    return img
save(hatch(0), "ice_hatch"); save(hatch(3), "ice_hatch_thawed")
ho = new(80, 80, (8, 12, 20)); d = ImageDraw.Draw(ho); d.rectangle([0, 0, 79, 79], outline=HUTW[0])
for i in range(5): d.rectangle([20, 10 + i * 14, 59, 13 + i * 14], fill=HUTW[2])
save(ho, "ice_hatch_open")
lp_ = new(32, 48); d = ImageDraw.Draw(lp_); d.line([16, 0, 16, 12], fill=IRON[3]); d.polygon([(6, 12), (26, 12), (22, 34), (10, 34)], fill=IRON[2]); d.ellipse([11, 18, 21, 30], fill=FIRE[1]); save(lp_, "hut_lamp")
# specimen case: 6 x 4 x 4, cold glass and brass, three coloured dials and a latch
def case_face(w, h, seed, front=False):
    img = face(w, h, ICE, seed, 3); d = ImageDraw.Draw(img); frost_edge(img, 8, seed)
    if front:
        d.rectangle([10, 8, w - 11, 30], fill=ICE[1], outline=BRASS[1])
        for x in range(14, w - 14, 6): d.line([x, 10, x + 8, 28], fill=ICE[3])
    return img
save(case_face(96, 64, 142, True), "spec_front")
save(case_face(96, 64, 143), "spec_back"); save(case_face(64, 64, 144), "spec_side"); save(case_face(96, 64, 145), "spec_top")
save(new(96, 64, (14, 26, 36)), "spec_liner")
for col, nm in ((RED2, "r"), (BLU2, "b"), (GRN2, "g")):
    for k in range(10):
        dd = new(16, 16); d = ImageDraw.Draw(dd); d.ellipse([0, 0, 15, 15], fill=col); d.ellipse([2, 2, 13, 13], fill=PAPER[2]); text(dd, 5, 3, str(k), INK, 2); save(dd, "cdial_%s_%d" % (nm, k))
cl = new(16, 8); d = ImageDraw.Draw(cl); d.rectangle([0, 1, 15, 6], fill=BRASS[2], outline=BRASS[0]); save(cl, "spec_latch")

# ================= room 10: the ice shaft =================
def ice_wall(seed, shapes=0):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            v = math.sin(x * 0.05 + y * 0.02 + seed) + math.sin(y * 0.09 - x * 0.03)
            c = ICE[2] if v > 0.6 else ICE[1] if v > -0.6 else ICE[0]
            if rnd.random() < 0.01: c = ICE[3]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    for i in range(shapes):
        cx, cy = rnd.randrange(30, 210), rnd.randrange(40, 300)
        d.ellipse([cx - 10, cy - 18, cx + 10, cy + 18], outline=ICE[0]); d.line([cx, cy + 18, cx - 8, cy + 34], fill=ICE[0]); d.line([cx, cy + 18, cx + 8, cy + 34], fill=ICE[0])
    return img
for k, s in zip("nesw", (151, 152, 153, 154)):
    save(ice_wall(s, 2 if k == "n" else 0), "r10_wall_" + k)
f = ice_wall(155).crop((0, 0, 240, 240)); d = ImageDraw.Draw(f); d.ellipse([60, 60, 179, 179], fill=ICE[0], outline=ICE[3]); save(f, "r10_floor")
c = ice_wall(156).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c); d.ellipse([90, 90, 149, 149], fill=(220, 236, 244)); save(c, "r10_ceiling")
for k in range(7):
    ln = 40 + k * 6
    ch = new(16, 112); d = ImageDraw.Draw(ch)
    d.polygon([(2, 0), (13, 0), (8, ln)], fill=ICE[3], outline=ICE[2]); d.line([5, 2, 7, ln - 10], fill=FROST[2])
    pl = new(16, 16); dp = ImageDraw.Draw(pl); dp.rectangle([0, 0, 15, 15], fill=ICE[0], outline=FROST[2]); text(pl, 5, 3, str(k + 1), FROST[2], 2); save(pl, "chime_no_%d" % k)
    save(ch, "chime_%d" % k)
fz = new(48, 96); d = ImageDraw.Draw(fz)
d.rectangle([0, 0, 47, 95], fill=ICE[2]); d.ellipse([14, 8, 33, 28], fill=(90, 80, 70)); d.rectangle([10, 28, 37, 80], fill=(60, 40, 30)); d.rectangle([12, 80, 35, 95], fill=(40, 30, 24))
d.rectangle([28, 44, 40, 54], fill=PAPER[1]); frost_edge(fz, 6, 157); save(fz, "frozen_man")
fn = new(48, 96); d = ImageDraw.Draw(fn); text(fn, 2, 38, "WREN", GLOW); d.rectangle([24, 44, 44, 56], outline=GLOW); save(fn, "frozen_note")
lad = new(48, 160); d = ImageDraw.Draw(lad)
for x in (6, 40): d.line([x, 0, x, 159], fill=HUTW[3], width=2)
for y in range(8, 160, 16): d.line([6, y, 40, y], fill=HUTW[2], width=2)
save(lad, "rope_ladder")
sc = new(64, 48, PAPER[2]); d = ImageDraw.Draw(sc); d.rectangle([0, 0, 63, 47], outline=PAPER[0])
for y in (10, 18, 26, 34): d.line([2, y, 61, y], fill=INK)
for i, n_ in enumerate([3, 1, 5, 2]):
    x = 6 + i * 11; y = 34 - (n_ - 1) * 4; d.ellipse([x, y - 2, x + 4, y + 2], fill=INK); text(sc, x, 40, str(n_), INK)
d.polygon([(48, 0), (63, 0), (63, 47), (52, 47), (56, 30), (50, 14)], fill=(0, 0, 0, 0))
save(sc, "score")
def star_face(seed, k=None):
    img = face(96, 96, STAR, seed, 3); d = ImageDraw.Draw(img)
    return img
for k, s in (("back", 158), ("side", 159), ("top", 160)): save(star_face(s), "plug_" + k)
pf = star_face(161); d = ImageDraw.Draw(pf); d.ellipse([44, 82, 51, 89], fill=INK); save(pf, "plug_front")
save(new(96, 96, (16, 20, 18)), "plug_liner")
def star5(rot):
    img = new(64, 64); d = ImageDraw.Draw(img)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5 + rot * 2 * math.pi / 5
        r = 30 if i % 2 == 0 else 13
        pts.append((31.5 + r * math.cos(a), 31.5 + r * math.sin(a)))
    d.polygon(pts, fill=STAR[3], outline=STAR[0])
    a = -math.pi / 2 + rot * 2 * math.pi / 5; d.ellipse([31.5 + 22 * math.cos(a) - 2, 31.5 + 22 * math.sin(a) - 2, 31.5 + 22 * math.cos(a) + 2, 31.5 + 22 * math.sin(a) + 2], fill=RED2)
    d.ellipse([27, 27, 36, 36], fill=STAR[1])
    return img
for k in range(5): save(star5(k), "star5_%d" % k)
pin = new(64, 64); d = ImageDraw.Draw(pin)
a = -math.pi / 2 + 3 * 2 * math.pi / 5   # the inner pin points at the fourth position
d.line([31.5, 31.5, 31.5 + 28 * math.cos(a), 31.5 + 28 * math.sin(a)], fill=GLOW, width=2); d.ellipse([28, 28, 35, 35], outline=GLOW)
save(pin, "plug_pin")
fh = new(12, 12); d = ImageDraw.Draw(fh); d.ellipse([0, 0, 11, 11], fill=STAR[1]); d.ellipse([3, 3, 8, 8], fill=INK); save(fh, "flute_hole")
for k, s in (("front", 162), ("back", 163), ("side", 164), ("top", 165)):
    img = face(96, 96, ICE, s, 3)
    if k == "front":
        d = ImageDraw.Draw(img)
        for x in (24, 48, 72): d.ellipse([x - 6, 42, x + 6, 54], fill=INK, outline=ICE[4])
    save(img, "cham_" + k)
save(new(96, 96, (10, 20, 30)), "cham_liner")
th = new(16, 16); d = ImageDraw.Draw(th); d.ellipse([0, 0, 15, 15], fill=ICE[3], outline=ICE[0]); d.ellipse([4, 4, 11, 11], fill=INK); save(th, "tone_hole")
th = new(16, 16); d = ImageDraw.Draw(th); d.ellipse([0, 0, 15, 15], fill=GLOW); d.ellipse([4, 4, 11, 11], fill=INK); save(th, "tone_hole_lit")

def icon(): return new(24, 24)
k = icon(); d = ImageDraw.Draw(k); d.rectangle([4, 6, 19, 19], fill=ICE[3], outline=ICE[1]); frost_edge(k, 5, 170); save(k, "item_frozen_tin")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([4, 6, 19, 19], fill=SILVER[2], outline=SILVER[0]); d.line([4, 9, 19, 9], fill=SILVER[0]); save(k, "item_thawed_tin")
k = icon(); d = ImageDraw.Draw(k); d.line([3, 20, 20, 3], fill=PAPER[2], width=3); [d.point((7 + i * 3, 16 - i * 3), fill=INK) for i in range(4)]; save(k, "item_bone_flute")
k = icon(); d = ImageDraw.Draw(k); d.polygon([(12, 1), (21, 8), (18, 21), (6, 21), (3, 8)], fill=(150, 196, 216), outline=(90, 200, 180)); stamp(k, 6, 6, sym_mask("star"), (40, 60, 80)); save(k, "item_seal_stone5")
ex = new(96, 72, (30, 24, 20)); ex.paste(sc.resize((96, 72), Image.NEAREST), (0, 0), sc.resize((96, 72), Image.NEAREST)); save(ex, "examine_bone_flute")
print("seal 5 art written to", os.path.abspath(OUT))

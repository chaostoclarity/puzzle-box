"""Seal 2 art: Thorne's study (hub), the Kingsport lamp room (room 3), the wreck's cabin (room 4).
Rule: 16 texels per world unit. Run: python3 tools/make_seal2_art.py  (writes assets/rooms/)
Placeholder art so the rooms can be built and played before final art. Sizes are the contract.
"""
from artkit import *

SEA   = [(6, 14, 22), (10, 24, 36), (16, 38, 54), (26, 58, 76), (44, 86, 104)]
LAMP  = [(120, 70, 10), (200, 130, 30), (250, 200, 80), (255, 240, 170)]
RUST  = [(50, 24, 14), (86, 40, 20), (124, 62, 30), (160, 96, 52)]
SALT  = [(70, 72, 74), (120, 124, 124), (176, 180, 176), (214, 216, 208)]
IRON  = [(20, 22, 26), (36, 38, 44), (54, 58, 66), (80, 86, 96), (112, 118, 128)]
WET   = [(18, 14, 12), (30, 22, 18), (44, 32, 24), (58, 44, 32), (76, 60, 44)]
WATER = [(34, 96, 118), (58, 140, 160), (160, 220, 224)]
ENAMEL = [(10, 14, 34), (18, 26, 58), (30, 42, 86), (60, 80, 140)]
EYE   = [(210, 196, 120), (120, 104, 50)]
GLOW  = (120, 255, 220)
W16 = 16

def wood_face(w, h, seed, pal=WOOD, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def u(n): return int(round(n * W16))

def rect(img, box, fill=None, outline=None):
    ImageDraw.Draw(img).rectangle(box, fill=fill, outline=outline)

def rivets(img, pal, step=12, inset=4):
    d = ImageDraw.Draw(img)
    for x in range(inset, img.width - inset + 1, step):
        for y in (inset, img.height - 1 - inset):
            d.point((x, y), fill=pal[-1]); d.point((x + 1, y + 1), fill=pal[0])

def metal(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

# ---------------- walls ----------------
WW, WH = 240, 352

def brick_wall(seed, pal, base_pal):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            row = y // 8
            off = 8 if row % 2 else 0
            c = pal[2]
            if y % 8 == 0 or (x + off) % 16 == 0: c = pal[1]
            elif rnd.random() < 0.04: c = pal[3]
            elif rnd.random() < 0.02: c = pal[0]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, WW, 15], fill=IRON[1]); d.line([0, 15, WW, 15], fill=IRON[3])
    for x in range(0, WW, 60): d.rectangle([x, 0, x + 5, WH], fill=IRON[1]); d.line([x + 1, 0, x + 1, WH], fill=IRON[3])
    d.rectangle([0, WH - 24, WW, WH], fill=base_pal[1]); d.line([0, WH - 24, WW, WH - 24], fill=base_pal[3])
    return img

def plank_wall(seed, tilt=0.08):
    """Wet ship's planks, drawn a little off level: the wreck lies on the reef at an angle."""
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            yy = y + x * tilt
            k = int(yy // 20)
            v = math.sin((x * 0.11 + k * 3.1) + 1.7 * math.sin(yy * 0.07 + k))
            c = WET[2] if v > 0.2 else WET[1]
            if yy % 20 < 1: c = WET[0]
            elif rnd.random() < 0.015: c = WET[3]
            if (x + k * 37) % 61 == 0 and yy % 20 in (6, 13): c = RUST[2]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    for x in (20, 120, 220): d.rectangle([x, 0, x + 9, WH], fill=WET[3], outline=WET[0])
    for y in range(0, WH, 24):
        for x in range(0, WW, 3):
            if random.Random(x * 7 + y).random() < 0.3: d.point((x, WH - 40 + (y % 40)), fill=SALT[1])
    return img

def plaster_wall(seed, stained=False):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    PAP = [(48, 36, 30), (70, 54, 42), (92, 72, 54), (110, 88, 66)]
    for y in range(WH):
        for x in range(WW):
            c = PAP[2] if (x // 12) % 2 == 0 else PAP[1]
            if (x % 12 == 6) and (y % 18 in (4, 5)): c = PAP[3]
            if rnd.random() < 0.03: c = PAP[0]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, WW, 23], fill=(28, 20, 18)); d.line([0, 23, WW, 23], fill=WOOD[3])
    wain = grain(WW, 64, WOOD, seed + 4, vertical=True); img.paste(wain, (0, WH - 64))
    d.line([0, WH - 64, WW, WH - 64], fill=WOOD[4])
    if stained:
        for cx in (40, 150, 210):
            r = 18 + cx % 13
            for y in range(24, 24 + r * 2):
                for x in range(cx - r, cx + r):
                    if 0 <= x < WW and (x - cx) ** 2 / r ** 2 + (y - 24) ** 2 / (r * 2) ** 2 < 1 and (x + y) % 2 == 0:
                        px[x, y] = (54, 52, 40, 255)
    return img

for k, s in zip("nesw", (31, 32, 33, 34)):
    save(brick_wall(s, SALT, IRON), "r3_wall_" + k)
    save(plank_wall(s + 10), "r4_wall_" + k)
    save(plaster_wall(s + 20), "h1_wall_" + k)
    save(plaster_wall(s + 20, True), "h2_wall_" + k)

def deck(w, h, pal, seed, grate=None):
    img = new(w, h); px = img.load(); rnd = random.Random(seed)
    for y in range(h):
        for x in range(w):
            c = pal[2] if (x // 16) % 2 else pal[1]
            if x % 16 == 0: c = pal[0]
            if rnd.random() < 0.02: c = pal[3]
            px[x, y] = c + (255,)
    return img

f = deck(240, 240, IRON, 41); d = ImageDraw.Draw(f)
for r in range(30, 120, 30): d.ellipse([120 - r, 120 - r, 120 + r, 120 + r], outline=IRON[0])
save(f, "r3_floor")
c = brick_wall(42, SALT, IRON).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c)
d.ellipse([70, 70, 170, 170], fill=IRON[1], outline=IRON[3]); d.ellipse([96, 96, 144, 144], fill=(8, 8, 12))
for a in range(8):
    ang = a * math.pi / 4
    d.line([120 + 26 * math.cos(ang), 120 + 26 * math.sin(ang), 120 + 50 * math.cos(ang), 120 + 50 * math.sin(ang)], fill=IRON[3])
save(c, "r3_ceiling")
f = deck(240, 240, WET, 43); d = ImageDraw.Draw(f)
d.rectangle([152, 24, 216, 88], fill=(10, 8, 6), outline=RUST[2])
for x in range(156, 214, 6): d.line([x, 26, x, 86], fill=RUST[1])
save(f, "r4_floor")
c = deck(240, 240, WET, 44); d = ImageDraw.Draw(c)
for y in (40, 120, 200): d.rectangle([0, y, 240, y + 11], fill=WET[3], outline=WET[0])
save(c, "r4_ceiling")
for n, st in (("h1", False), ("h2", True)):
    f = new(240, 240, VELVET[0]); d = ImageDraw.Draw(f)
    d.rectangle([24, 24, 215, 215], fill=VELVET[1], outline=BRASS[1])
    for i in range(32, 208, 16): d.line([32, i, 207, i], fill=VELVET[2])
    if st:
        for x in range(0, 240, 2): d.point((x, 236 - (x % 7)), fill=SALT[3])
    save(f, n + "_floor")
    c = plaster_wall(50, st).crop((0, 0, 240, 240)); save(c, n + "_ceiling")

# ---------------- generic faces ----------------
for n, (w, h) in {"iron_side_48x96": (48, 96), "iron_top_96x48": (96, 48), "iron_side_24x176": (24, 176),
                  "iron_side_8x80": (8, 80)}.items():
    save(metal(w, h, IRON, w + h), n)
for n, (w, h) in {"wood_top_112x40": (112, 40), "wood_side_40x64": (40, 64), "wood_side_40x152": (40, 152),
                  "wood_side_32x64": (32, 64), "wet_side_64x64": (64, 64), "wet_top_96x64": (96, 64)}.items():
    save(metal(w, h, WET if n.startswith("wet") else WOOD, w * 3 + h), n)

# ================= ROOM 3: the lamp room =================
p = metal(96, 96, IRON, 51, 3); d = ImageDraw.Draw(p)
d.rectangle([12, 12, 83, 83], outline=IRON[4]); rivets(p, IRON)
text(p, 48 - text_w("KINGSPORT") // 2, 40, "KINGSPORT", BRASS[2]); text(p, 48 - text_w("1868") // 2, 50, "1868", BRASS[1])
save(p, "pedestal_front")

def carriage_face(seed, socket=False, gears=True):
    img = metal(96, 96, BRASS, seed, 3); d = ImageDraw.Draw(img); rivets(img, BRASS)
    if gears:
        for (cx, cy, r) in ((30, 34, 14), (62, 58, 18), (70, 22, 8)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BRASS[0])
            for k in range(10):
                a = k * math.pi / 5 + seed
                d.point((round(cx + (r + 1) * math.cos(a)), round(cy + (r + 1) * math.sin(a))), fill=BRASS[0])
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=BRASS[0])
    if socket:
        d.rectangle([40, 68, 55, 83], fill=BRASS[0]); d.rectangle([44, 72, 51, 79], fill=INK)
    return img
save(carriage_face(52, True), "carriage_front")
for k, s in (("back", 53), ("left", 54), ("right", 55), ("bottom", 56)): save(carriage_face(s), "carriage_" + k)
top = metal(96, 96, BRASS, 57, 3); d = ImageDraw.Draw(top)
d.rectangle([11, 11, 84, 84], fill=IRON[0], outline=BRASS[0])
for i in range(7):
    d.line([12 + i * 12, 12, 12 + i * 12, 84], fill=IRON[1]); d.line([12, 12 + i * 12, 84, 12 + i * 12], fill=IRON[1])
save(top, "carriage_top")
lin = new(96, 96, (16, 12, 10)); d = ImageDraw.Draw(lin)
for i in range(0, 96, 6): d.line([i, 0, i, 95], fill=(26, 20, 16))
save(lin, "carriage_liner")

def mirror(state):
    img = new(12, 12); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, 11, 11], fill=IRON[2], outline=IRON[0])
    pts = {0: [(2, 9), (9, 2)], 1: [(1, 6), (10, 6)], 2: [(2, 2), (9, 9)], 3: [(6, 1), (6, 10)]}[state]
    d.line(pts, fill=SILVER[4], width=2)
    d.point((6, 6), fill=IRON[0])
    return img
for s in range(4): save(mirror(s), "mirror_%d" % s)
gm = new(12, 12); d = ImageDraw.Draw(gm); d.line([(2, 9), (9, 2)], fill=GLOW, width=2); d.point((1, 10), fill=GLOW); save(gm, "ghost_mirror")
def port(col, lit, sym):
    img = new(12, 12); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 11, 11], fill=IRON[0], outline=BRASS[1])
    d.rectangle([3, 3, 8, 8], fill=LAMP[3] if lit else col)
    if sym == "wave": d.line([3, 6, 4, 5, 6, 7, 8, 5], fill=SEA[4] if not lit else LAMP[1])
    if sym == "house": d.polygon([(3, 6), (6, 3), (8, 6)], fill=WOOD[3] if not lit else LAMP[1])
    if sym == "eye": d.ellipse([3, 4, 8, 7], fill=EYE[0] if lit else EYE[1]); d.point((5, 5), fill=INK); d.point((6, 6), fill=INK)
    return img
save(port(SEA[2], False, "wave"), "port_sea"); save(port(SEA[2], True, "wave"), "port_sea_lit")
save(port(WOOD[1], False, "house"), "port_land"); save(port(WOOD[1], True, "house"), "port_land_lit")
save(port(SEA[1], False, "eye"), "fisheye"); save(port(SEA[1], True, "eye"), "fisheye_lit")
src = new(12, 12); d = ImageDraw.Draw(src); d.rectangle([0, 0, 11, 11], fill=BRASS[1], outline=BRASS[0]); d.ellipse([3, 3, 8, 8], fill=LAMP[2]); save(src, "lamp_port")
src = new(12, 12); d = ImageDraw.Draw(src); d.rectangle([0, 0, 11, 11], fill=BRASS[1], outline=BRASS[0]); d.ellipse([3, 3, 8, 8], fill=INK); save(src, "lsocket")
src = new(12, 12); d = ImageDraw.Draw(src); d.rectangle([0, 0, 11, 11], fill=BRASS[1], outline=BRASS[0]); d.ellipse([2, 2, 9, 9], fill=LAMP[3]); save(src, "lsocket_lit")
pil = new(12, 12); d = ImageDraw.Draw(pil); d.rectangle([1, 1, 10, 10], fill=IRON[3], outline=IRON[0]); d.line([1, 1, 10, 10], fill=IRON[1]); save(pil, "pillar")
gb = Image.new("RGBA", (6, 2), LAMP[3] + (255,)); save(gb, "glow_beam_h")
gb = Image.new("RGBA", (2, 6), LAMP[3] + (255,)); save(gb, "glow_beam_v")

cr = new(24, 24); d = ImageDraw.Draw(cr)
d.rectangle([9, 9, 14, 14], fill=IRON[3], outline=IRON[0]); d.rectangle([11, 2, 12, 11], fill=IRON[3]); d.rectangle([11, 1, 20, 3], fill=IRON[3]); d.rectangle([18, 0, 21, 5], fill=WOOD[3])
save(cr, "crank_fitted")

def fresnel(lit):
    img = new(64, 96); d = ImageDraw.Draw(img)
    d.rectangle([4, 84, 59, 95], fill=BRASS[1], outline=BRASS[0])
    d.polygon([(12, 84), (52, 84), (58, 20), (32, 4), (6, 20)], fill=LAMP[2] if lit else SILVER[1], outline=BRASS[0])
    for y in range(18, 84, 8): d.line([10, y, 54, y], fill=LAMP[1] if lit else SILVER[0])
    d.ellipse([22, 40, 41, 59], fill=LAMP[3] if lit else SILVER[2])
    d.rectangle([28, 0, 35, 5], fill=BRASS[2])
    return img
save(fresnel(False), "fresnel"); save(fresnel(True), "fresnel_lit")
gl = Image.new("RGBA", (160, 160), (0, 0, 0, 0)); px = gl.load()
for y in range(160):
    for x in range(160):
        r = math.hypot(x - 79.5, y - 79.5) / 80
        if r < 1: px[x, y] = (255, 210, 110, int(150 * (1 - r) ** 2))
gl.save(os.path.join(OUT, "glow_lamp.png"))
gl = Image.new("RGBA", (48, 48), (0, 0, 0, 0)); px = gl.load()
for y in range(48):
    for x in range(48):
        r = math.hypot(x - 23.5, y - 23.5) / 24
        if r < 1: px[x, y] = (255, 180, 80, int(120 * (1 - r) ** 2))
gl.save(os.path.join(OUT, "glow_lantern.png"))

cl = new(112, 160); d = ImageDraw.Draw(cl)
d.polygon([(10, 0), (100, 0), (110, 159), (2, 159)], fill=IVORY[1], outline=IVORY[0])
for x in range(16, 104, 14): d.line([x, 4, x + (x - 56) // 6, 156], fill=IVORY[0])
d.line([56, 0, 56, 6], fill=WOOD[1])
save(cl, "cloth")
cle = new(48, 48); d = ImageDraw.Draw(cle)
d.rectangle([18, 4, 29, 43], fill=IRON[3], outline=IRON[0]); d.rectangle([8, 18, 39, 25], fill=IRON[2], outline=IRON[0])
for y in range(6, 40, 3): d.line([20, y, 27, y + 2], fill=WOOD[3])
save(cle, "cleat")
cle = new(48, 48); d = ImageDraw.Draw(cle)
d.rectangle([18, 4, 29, 43], fill=IRON[3], outline=IRON[0]); d.rectangle([8, 18, 39, 25], fill=IRON[2], outline=IRON[0])
save(cle, "cleat_free")

kd = wood_face(112, 64, 61); d = ImageDraw.Draw(kd)
d.rectangle([8, 8, 103, 26], outline=WOOD[0]); d.rectangle([52, 16, 59, 18], fill=BRASS[2])
save(kd, "kdesk_front")
lg = new(32, 24); d = ImageDraw.Draw(lg)
d.polygon([(0, 22), (15, 18), (15, 2), (0, 6)], fill=IVORY[2], outline=IVORY[0]); d.polygon([(31, 22), (16, 18), (16, 2), (31, 6)], fill=IVORY[2], outline=IVORY[0])
for y in range(8, 18, 3): d.line([3, y, 12, y - 2], fill=INK); d.line([19, y - 2, 28, y], fill=INK)
d.rectangle([0, 22, 31, 23], fill=VELVET[1])
save(lg, "logbook")

bf = wood_face(40, 80, 62, DARKW); save(bf, "baro_front")
WORDS = ["STORM", "RAIN", "CHANGE", "FAIR"]
def baro(v):
    img = new(32, 32); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, 31, 31], fill=BRASS[1]); d.ellipse([2, 2, 29, 29], fill=IVORY[2])
    for i in range(4):
        a = math.pi * (0.85 + 0.43 * i)
        d.line([16 + 9 * math.cos(a), 16 + 9 * math.sin(a), 16 + 12 * math.cos(a), 16 + 12 * math.sin(a)], fill=INK)
    a = math.pi * (0.85 + 0.43 * v)
    d.line([16, 16, 16 + 11 * math.cos(a), 16 + 11 * math.sin(a)], fill=RED, width=1)
    w = WORDS[v]; text(img, 16 - text_w(w) // 2, 21, w, INK)
    d.ellipse([14, 14, 17, 17], fill=BRASS[0])
    return img
for v in range(4): save(baro(v), "baro_%d" % v)
bd = metal(16, 16, BRASS, 63, 1); d = ImageDraw.Draw(bd); d.point((12, 8), fill=INK); save(bd, "baro_door")
save(new(16, 16, (10, 8, 6)), "baro_door_open")
sk = new(12, 8); d = ImageDraw.Draw(sk); d.ellipse([0, 1, 5, 6], fill=IRON[3], outline=IRON[0]); d.rectangle([5, 3, 11, 4], fill=IRON[3]); d.rectangle([9, 5, 10, 7], fill=IRON[2]); save(sk, "small_locker_key")

pl = new(48, 48); d = ImageDraw.Draw(pl); d.ellipse([2, 2, 45, 45], fill=SALT[1], outline=SALT[0]); d.ellipse([10, 10, 37, 37], outline=SALT[0]); save(pl, "plaque")
pl = new(48, 48); d = ImageDraw.Draw(pl); d.ellipse([2, 2, 45, 45], fill=LAMP[2], outline=LAMP[1]); d.ellipse([10, 10, 37, 37], outline=LAMP[1]); save(pl, "plaque_lit")
pw = new(48, 48); text(pw, 24 - text_w("W", 3) // 2, 17, "W", GLOW, 3); save(pw, "plaque_w")

lf = metal(64, 96, IRON, 64, 2); d = ImageDraw.Draw(lf); rivets(lf, IRON, 10)
text(lf, 32 - text_w("OIL") // 2, 4, "OIL", SALT[3]); save(lf, "locker_front")
ld = metal(48, 72, IRON, 65, 2); d = ImageDraw.Draw(ld)
for y in (14, 34, 54): d.rectangle([0, y - 2, 47, y + 9], fill=IRON[0])
d.rectangle([40, 30, 47, 42], fill=BRASS[1])
save(ld, "locker_door")
lo = new(48, 72, (8, 6, 6)); d = ImageDraw.Draw(lo); bevel(lo, IRON, 1)
d.rectangle([8, 40, 21, 66], fill=RUST[2], outline=RUST[0]); d.line([21, 44, 28, 36], fill=RUST[2], width=2)
d.rectangle([28, 50, 33, 55], fill=IRON[3]); d.rectangle([30, 30, 31, 52], fill=IRON[3]); d.rectangle([30, 28, 38, 30], fill=IRON[3])
save(lo, "locker_door_open")
le = new(48, 72, (8, 6, 6)); bevel(le, IRON, 1); save(le, "locker_door_empty")
pad = new(12, 16); d = ImageDraw.Draw(pad); d.arc([2, 0, 9, 9], 180, 360, fill=IRON[4], width=2); d.rectangle([0, 6, 11, 15], fill=BRASS[1], outline=BRASS[0]); d.point((6, 10), fill=INK); d.point((6, 11), fill=INK)
save(pad, "padlock")
def bar(notch):
    img = new(48, 8); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 47, 7], fill=IRON[3], outline=IRON[0]); d.line([1, 1, 46, 1], fill=IRON[4])
    for x in notch: d.rectangle([x, 5, x + 3, 7], fill=IRON[0])
    d.rectangle([20, 2, 27, 5], fill=RUST[2])
    return img
save(bar([6]), "lbar_t"); save(bar([12, 34]), "lbar_m"); save(bar([24]), "lbar_b")

no = new(48, 64, IVORY[2]); d = ImageDraw.Draw(no); d.rectangle([0, 0, 47, 63], outline=IVORY[0])
y = 4
for line in ["NOTICE TO", "MARINERS", "", "KINGSPORT", "LIGHT", "", "FL 3", "EVERY 7S", "SEEN 9M"]:
    if line: text(no, 24 - text_w(line) // 2, y, line, INK)
    y += 6
save(no, "notice")

def hatch(open_):
    img = metal(80, 80, IRON, 66, 3); d = ImageDraw.Draw(img)
    if open_:
        d.rectangle([6, 6, 73, 73], fill=(4, 4, 6))
        for i in range(5): d.rectangle([14, 14 + i * 12, 65, 18 + i * 12], fill=IRON[2])
    else:
        rivets(img, IRON, 10); d.rectangle([30, 34, 49, 45], fill=IRON[1], outline=IRON[4])
        text(img, 40 - text_w("STAIR") // 2, 60, "STAIR", SALT[2])
    return img
save(hatch(False), "hatch"); save(hatch(True), "hatch_open")

def sea_window(beam):
    img = new(192, 176); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 191, 175], fill=IRON[1])
    d.rectangle([8, 8, 183, 167], fill=SKY[0])
    for y in range(8, 100):
        for x in range(8, 184):
            if random.Random(x * 13 + y * 7).random() < 0.006: img.putpixel((x, y), SALT[3] + (255,))
    for y in range(100, 168):
        for x in range(8, 184):
            v = math.sin(x * 0.2 + y * 0.9) + math.sin(x * 0.07 - y * 0.3)
            img.putpixel((x, y), (SEA[3] if v > 1.2 else SEA[2] if v > 0 else SEA[1]) + (255,))
    d.polygon([(110, 112), (122, 104), (136, 110), (150, 114), (104, 116)], fill=STONE[1])
    d.line([126, 104, 132, 92], fill=WET[2], width=2); d.line([126, 104, 118, 96], fill=WET[2])
    if beam:
        d.polygon([(8, 70), (184, 92), (184, 120), (8, 82)], fill=LAMP[2])
        d.polygon([(8, 74), (184, 100), (184, 110), (8, 78)], fill=LAMP[3])
    for x in (66, 126): d.rectangle([x, 8, x + 3, 167], fill=IRON[2])
    d.rectangle([8, 86, 183, 89], fill=IRON[2])
    return img
save(sea_window(False), "sea_window"); save(sea_window(True), "sea_window_beam")
se = new(32, 16); d = ImageDraw.Draw(se); d.ellipse([0, 2, 31, 13], fill=EYE[0], outline=EYE[1]); d.ellipse([12, 2, 19, 13], fill=INK); d.point((14, 5), fill=SALT[3])
save(se, "sea_eye")
def lantern(present):
    img = new(24, 40); d = ImageDraw.Draw(img)
    d.rectangle([10, 0, 13, 5], fill=IRON[3]); d.line([4, 5, 19, 5], fill=IRON[3])
    if present:
        d.arc([6, 3, 17, 12], 180, 360, fill=IRON[3])
        d.rectangle([5, 12, 18, 33], fill=LAMP[1], outline=IRON[0]); d.rectangle([8, 15, 15, 30], fill=LAMP[3])
        d.rectangle([3, 33, 20, 38], fill=IRON[2]); d.rectangle([5, 9, 18, 12], fill=IRON[2])
    return img
save(lantern(True), "lantern"); save(lantern(False), "lantern_hook")
hp = new(64, 32); d = ImageDraw.Draw(hp)
d.rectangle([2, 14, 40, 19], fill=WOOD[2], outline=WOOD[0]); d.rectangle([40, 15, 62, 17], fill=IRON[3]); d.polygon([(58, 12), (63, 16), (58, 20)], fill=IRON[4])
d.rectangle([10, 19, 15, 30], fill=WOOD[1]); d.rectangle([28, 19, 31, 26], fill=IRON[2])
save(hp, "harpoon")

# prism case (nested in the carriage) and the keeper's tin (nested in the prism case)
def enamel_face(seed, stars=False):
    img = metal(96, 96, ENAMEL, seed, 3); d = ImageDraw.Draw(img); rivets(img, [BRASS[0], BRASS[2]], 16)
    rnd = random.Random(seed)
    for i in range(40): d.point((rnd.randrange(8, 88), rnd.randrange(8, 88)), fill=ENAMEL[3])
    return img
for k, s in (("front", 71), ("back", 72), ("left", 73), ("right", 74), ("top", 75), ("bottom", 76)): save(enamel_face(s), "prism_" + k)
pl = new(96, 96, (6, 8, 18)); save(pl, "prism_liner")
st = new(12, 12); d = ImageDraw.Draw(st); stamp(st, 0, 0, sym_mask("star"), SILVER[3]); save(st, "star")
st = new(12, 12); d = ImageDraw.Draw(st); stamp(st, 0, 0, sym_mask("star"), LAMP[3]); save(st, "star_lit")
STARS = {"a": (-1.8, 1.6), "b": (0.4, 2.0), "c": (1.9, 0.6), "d": (-0.6, -0.2), "e": (1.0, -1.8)}
def spx(k): x, y = STARS[k]; return (48 + x * 16, 48 - y * 16)
ln = new(96, 96); d = ImageDraw.Draw(ln)
order = "dbaec"
for a, b in zip(order, order[1:]): d.line([spx(a), spx(b)], fill=GLOW)
x, y = spx("d"); d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=GLOW)
save(ln, "prism_lines")

def tin_face(seed, labels=False):
    img = metal(96, 96, SILVER, seed, 3); d = ImageDraw.Draw(img)
    if labels:
        for i, lab in enumerate(["FL", "S", "M"]):
            cx = 24 + i * 24
            d.rectangle([cx - 8, 36, cx + 7, 59], fill=INK)
            text(img, cx - text_w(lab) // 2, 66, lab, INK)
        text(img, 48 - text_w("A. PIKE") // 2, 14, "A. PIKE", SILVER[0])
    return img
save(tin_face(81, True), "tin_front")
for k, s in (("back", 82), ("left", 83), ("right", 84), ("top", 85), ("bottom", 86)): save(tin_face(s), "tin_" + k)
save(new(96, 96, (30, 30, 36)), "tin_liner")
for n in range(10):
    dg = new(12, 16, IVORY[2]); d = ImageDraw.Draw(dg); d.rectangle([0, 0, 11, 15], outline=IVORY[0])
    text(dg, 3, 3, str(n), INK, 2) if False else text(dg, 4, 5, str(n), INK)
    save(dg, "digit_%d" % n)

# ================= ROOM 4: the wreck =================
def water(h, top_foam=True):
    img = new(240, h); px = img.load()
    for y in range(h):
        for x in range(240):
            if y < 2 and top_foam:
                if (x // 3 + y) % 2 == 0: px[x, y] = WATER[2] + (255,)
                continue
            if (x + y) % 2 == 0:
                v = math.sin(x * 0.15 + y * 0.4)
                px[x, y] = (WATER[1] if v > 0.6 else WATER[0]) + (255,)
    return img
save(water(144), "water_9"); save(water(80), "water_5"); save(water(24), "water_1")
save(water(240, False), "water_floor")

def porthole(abyss):
    img = new(48, 48); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, 47, 47], fill=BRASS[1], outline=BRASS[0]); d.ellipse([5, 5, 42, 42], fill=SEA[1])
    if abyss:
        d.ellipse([5, 5, 42, 42], fill=(24, 22, 18))
        d.rectangle([5, 34, 42, 42], fill=WET[2])
        d.ellipse([8, 14, 39, 30], fill=EYE[0], outline=EYE[1]); d.ellipse([20, 14, 27, 30], fill=INK)
    else:
        for i in range(12):
            r = random.Random(i)
            d.point((r.randrange(10, 38), r.randrange(10, 38)), fill=SEA[4])
    for a in range(6):
        ang = a * math.pi / 3
        d.point((round(23.5 + 21 * math.cos(ang)), round(23.5 + 21 * math.sin(ang))), fill=BRASS[3])
    return img
save(porthole(False), "porthole"); save(porthole(True), "porthole_abyss")

MAZE_WALLS = [(1, 0), (1, 2), (2, 0), (3, 2), (3, 3), (4, 1)]
def chest_front():
    """128x64 (8 x 4 units). Maze: 6 x 4 cells of 8 texels at x 26, y 14 (centre uv -0.875, 0.125). Keyhole plate centre uv (2.59, 0.03)."""
    img = grain(128, 64, WET, 91); bevel(img, WET, 2); d = ImageDraw.Draw(img)
    for x in (4, 120): d.rectangle([x, 0, x + 3, 63], fill=IRON[2])
    x0, y0 = 26, 14
    d.rectangle([x0 - 2, y0 - 2, x0 + 49, y0 + 33], fill=IVORY[0], outline=IRON[0])
    d.rectangle([x0, y0, x0 + 47, y0 + 31], fill=IVORY[2])
    for (c, r) in MAZE_WALLS: d.rectangle([x0 + c * 8, y0 + r * 8, x0 + c * 8 + 7, y0 + r * 8 + 7], fill=WET[1])
    gx, gy = x0 + 5 * 8, y0 + 2 * 8; d.ellipse([gx + 1, gy + 1, gx + 6, gy + 6], fill=INK)
    d.line([gx + 8, gy + 4, 97, gy + 4], fill=IRON[0])
    d.rectangle([98, 22, 113, 41], fill=IRON[2], outline=IRON[0])
    return img
save(chest_front(), "chest_front")
cb = grain(128, 64, WET, 92); bevel(cb, WET, 2); save(cb, "chest_back")
cs = grain(64, 64, WET, 93); bevel(cs, WET, 2); d = ImageDraw.Draw(cs); d.rectangle([28, 0, 35, 63], fill=IRON[2]); save(cs, "chest_side")
ct = grain(128, 64, WET, 94); bevel(ct, WET, 2); d = ImageDraw.Draw(ct)
for x in (4, 120): d.rectangle([x, 0, x + 3, 63], fill=IRON[2])
save(ct, "chest_top")
save(new(128, 64, (20, 14, 10)), "chest_liner")
pe = new(8, 8); d = ImageDraw.Draw(pe); d.ellipse([0, 0, 7, 7], fill=IVORY[2], outline=SILVER[1]); d.point((2, 2), fill=SILVER[4]); save(pe, "pearl")
for k, pts in {"n": [(6, 2), (10, 9), (2, 9)], "s": [(6, 10), (2, 3), (10, 3)], "e": [(10, 6), (3, 2), (3, 10)], "w": [(2, 6), (9, 2), (9, 10)]}.items():
    b = new(12, 12); d = ImageDraw.Draw(b); d.ellipse([0, 0, 11, 11], fill=BRASS[1], outline=BRASS[0]); d.polygon(pts, fill=BRASS[3]); save(b, "tilt_" + k)
kc = metal(16, 20, IRON, 95, 1); save(kc, "keyhole_cover")
kh = new(16, 20); d = ImageDraw.Draw(kh); d.rectangle([0, 0, 15, 19], fill=IRON[2], outline=IRON[0]); d.ellipse([5, 4, 10, 9], fill=INK); d.rectangle([7, 9, 8, 15], fill=INK); save(kh, "keyhole")
fb = grain(80, 48, WOOD, 96); bevel(fb, WOOD, 1); d = ImageDraw.Draw(fb)
for i, line in enumerate(["NEVER DRAIN HER", "PAST THE THIRD", "MARK. J.P."]): text(fb, 40 - text_w(line) // 2, 8 + i * 9, line, WOOD[0])
save(fb, "fbottom")
k2 = new(12, 16); d = ImageDraw.Draw(k2); d.ellipse([3, 1, 8, 6], fill=INK, outline=GLOW); d.rectangle([5, 6, 6, 13], fill=INK); d.rectangle([4, 6, 7, 13], outline=GLOW); save(k2, "keyhole2")

def binn_face(seed, rose=False):
    img = metal(96, 96, BRASS, seed, 3); d = ImageDraw.Draw(img); rivets(img, BRASS, 16)
    if rose:
        d.ellipse([20, 20, 75, 75], fill=IVORY[2], outline=BRASS[0])
        for a in range(8):
            ang = a * math.pi / 4; r = 26 if a % 2 == 0 else 14
            d.polygon([(48, 48), (48 + r * math.cos(ang - 0.2), 48 + r * math.sin(ang - 0.2)), (48 + (r + 2) * math.cos(ang), 48 + (r + 2) * math.sin(ang))], fill=INK)
        text(img, 46, 22, "N", RED)
    return img
save(binn_face(101, True), "binn_front")
for k, s in (("back", 102), ("left", 103), ("right", 104), ("bottom", 106)): save(binn_face(s), "binn_" + k)
bt = metal(96, 96, BRASS, 105, 3); d = ImageDraw.Draw(bt)
d.rectangle([17, 17, 78, 78], fill=SEA[0], outline=BRASS[0])
for i in range(6):
    d.line([18 + i * 12, 18, 18 + i * 12, 78], fill=SEA[1]); d.line([18, 18 + i * 12, 78, 18 + i * 12], fill=SEA[1])
save(bt, "binn_top")
save(new(96, 96, (14, 10, 6)), "binn_liner")

ctf = grain(112, 152, WOOD, 111); bevel(ctf, WOOD, 2); d = ImageDraw.Draw(ctf)
for y in (20, 60, 100): d.rectangle([10, y, 101, y + 30], outline=WOOD[0]); d.rectangle([52, y + 13, 59, y + 16], fill=BRASS[1])
for x in range(0, 112, 2): d.point((x, 150 - (x % 5)), fill=SALT[2])
save(ctf, "ctable_front")
cl = new(40, 24); d = ImageDraw.Draw(cl)
d.polygon([(0, 22), (19, 18), (19, 2), (0, 6)], fill=IVORY[1], outline=WOOD[0]); d.polygon([(39, 22), (20, 18), (20, 2), (39, 6)], fill=IVORY[1], outline=WOOD[0])
for y in range(8, 18, 3): d.line([3, y, 16, y - 2], fill=INK); d.line([23, y - 2, 36, y], fill=INK)
save(cl, "clog")
ch = new(80, 64, IVORY[1]); d = ImageDraw.Draw(ch); d.rectangle([0, 0, 79, 63], outline=WOOD[0])
d.line([6, 50, 20, 40, 34, 44, 50, 26, 70, 20], fill=SEA[2]); d.polygon([(48, 30), (54, 26), (58, 32)], fill=STONE[2])
text(ch, 4, 4, "KINGSPORT", INK); text(ch, 4, 56, "REEF", INK); d.line([52, 28, 70, 10], fill=LAMP[1])
save(ch, "chart")
pf = metal(32, 176, IRON, 112, 2); d = ImageDraw.Draw(pf)
d.rectangle([4, 20, 27, 150], fill=IRON[1], outline=IRON[3]); d.rectangle([10, 150, 21, 175], fill=IRON[2])
save(pf, "pump_front")
ps = new(16, 16); d = ImageDraw.Draw(ps); d.rectangle([0, 0, 15, 15], fill=IRON[3], outline=IRON[0]); d.rectangle([5, 5, 10, 10], fill=INK); save(ps, "pump_socket")
ps = new(16, 16); d = ImageDraw.Draw(ps); d.rectangle([0, 0, 15, 15], fill=IRON[3], outline=IRON[0]); d.rectangle([6, 1, 9, 14], fill=IRON[4]); d.rectangle([6, 0, 15, 3], fill=IRON[4]); save(ps, "pump_socket_crank")
ga = new(24, 160, IVORY[1]); d = ImageDraw.Draw(ga); d.rectangle([0, 0, 23, 159], outline=WOOD[0])
# gauge spans wall y 0.5 .. 10.5; marks at tide levels: 9 (high), 5 (mid), 1.5 (low)
for lvl, lab in ((9, "1"), (5, "2"), (1.5, "3")):
    yy = 160 - int((lvl - 0.5) * 16)
    d.line([2, yy, 21, yy], fill=RED if lab == "3" else INK); text(ga, 9, yy - 7, lab, RED if lab == "3" else INK)
save(ga, "gauge")
cd = grain(64, 160, WET, 113); bevel(cd, WET, 2); d = ImageDraw.Draw(cd); d.rectangle([50, 76, 55, 84], fill=BRASS[1])
d.line([0, 40, 63, 64], fill=WET[0], width=2); save(cd, "cdoor")
def seacock(free):
    img = new(32, 32); d = ImageDraw.Draw(img)
    pal = IRON if free else RUST
    d.rectangle([12, 16, 19, 31], fill=pal[1]); d.ellipse([1, 1, 30, 30], outline=pal[3], width=3)
    d.line([4, 16, 27, 16], fill=pal[2], width=2); d.line([16, 4, 16, 27], fill=pal[2], width=2); d.ellipse([12, 12, 19, 19], fill=pal[3])
    if not free:
        for i in range(14): r = random.Random(i); d.point((r.randrange(2, 30), r.randrange(2, 30)), fill=RUST[3])
    return img
save(seacock(False), "seacock_rust"); save(seacock(True), "seacock")
sh = new(80, 16); d = ImageDraw.Draw(sh); d.rectangle([0, 10, 79, 15], fill=WET[3], outline=WET[0]); d.rectangle([6, 0, 9, 10], fill=WET[2]); d.rectangle([70, 0, 73, 10], fill=WET[2]); save(sh, "shelf")
sck = new(24, 12); d = ImageDraw.Draw(sck); d.ellipse([0, 2, 9, 11], fill=IRON[3], outline=IRON[0]); d.rectangle([9, 5, 23, 7], fill=IRON[3])
for x in (13, 17, 21): d.line([x, 8, x - 1, 11], fill=IRON[3])
save(sck, "small_chest_key")
pc = new(48, 64, (40, 30, 20)); d = ImageDraw.Draw(pc); d.rectangle([3, 3, 44, 60], fill=(70, 66, 58)); d.ellipse([14, 10, 33, 32], fill=(150, 126, 100)); d.rectangle([10, 34, 37, 60], fill=SEA[1])
d.rectangle([18, 18, 21, 20], fill=INK); d.rectangle([26, 18, 29, 20], fill=INK); d.rectangle([12, 26, 35, 34], fill=SALT[2]); save(pc, "portrait_captain")
ca = new(128, 48); d = ImageDraw.Draw(ca)
for i, line in enumerate(["THE GLASS TURNS", "WHAT BRASS CANNOT"]): text(ca, 64 - text_w(line, 2) // 2, 6 + i * 18, line, WET[0], 2)
save(ca, "carving")
sl = new(64, 64); d = ImageDraw.Draw(sl); d.rectangle([0, 0, 63, 63], fill=WET[3], outline=WET[0]); d.rectangle([6, 6, 57, 57], fill=SKY[1])
for x in (30, 33): d.line([x, 6, x, 57], fill=WET[2])
d.line([6, 31, 57, 31], fill=WET[2]); d.rectangle([26, 52, 37, 57], fill=IRON[3]); save(sl, "skylight")
sl = new(64, 64); d = ImageDraw.Draw(sl); d.rectangle([0, 0, 63, 63], fill=WET[3], outline=WET[0]); d.rectangle([6, 6, 57, 57], fill=SKY[0])
for i in range(12): r = random.Random(i + 9); d.point((r.randrange(8, 56), r.randrange(8, 56)), fill=SALT[3])
save(sl, "skylight_open")

# ================= HUB: Thorne's study =================
so = new(12, 12); d = ImageDraw.Draw(so); d.ellipse([0, 0, 11, 11], fill=(40, 34, 48), outline=GLOW); d.ellipse([3, 3, 8, 8], fill=GLOW); save(so, "socket_lit")
dr = metal(48, 8, BRASS, 121, 1); save(dr, "cab_drawer")
dr = new(48, 8, INK); d = ImageDraw.Draw(dr); d.rectangle([4, 1, 43, 7], fill=IVORY[2]); save(dr, "cab_drawer_open")
td = wood_face(112, 64, 122, DARKW); d = ImageDraw.Draw(td); d.rectangle([8, 8, 103, 26], outline=DARKW[0]); save(td, "tdesk_front")
ml = new(32, 16); d = ImageDraw.Draw(ml)
for i in range(3): d.rectangle([2 + i * 3, 6 - i * 2, 25 + i * 3, 15 - i * 2], fill=IVORY[2], outline=IVORY[0])
save(ml, "mail")
ml = new(48, 32); d = ImageDraw.Draw(ml)
for i in range(9): r = random.Random(i); x, y = r.randrange(0, 20), 26 - i * 3; d.rectangle([x, y, x + 24, y + 5], fill=IVORY[2] if i % 3 else IVORY[1], outline=IVORY[0])
save(ml, "mail_pile")
mi = new(48, 80); d = ImageDraw.Draw(mi); d.rectangle([0, 0, 47, 79], fill=BRASS[1], outline=BRASS[0]); d.rectangle([4, 4, 43, 75], fill=SILVER[1])
d.line([8, 70, 38, 10], fill=SILVER[3]); d.ellipse([16, 22, 31, 40], fill=(110, 96, 84)); d.rectangle([14, 40, 33, 75], fill=(30, 28, 34))
save(mi, "mirror")
mi = new(48, 80); d = ImageDraw.Draw(mi); d.rectangle([0, 0, 47, 79], fill=BRASS[1], outline=BRASS[0]); d.polygon([(0, 2), (47, 0), (46, 79), (2, 78)], fill=IVORY[1], outline=IVORY[0])
for x in (12, 26, 38): d.line([x, 2, x - 3, 77], fill=IVORY[0])
save(mi, "mirror_covered")
wn = new(64, 96); d = ImageDraw.Draw(wn); d.rectangle([0, 0, 63, 95], fill=WOOD[1]); d.rectangle([4, 4, 59, 91], fill=SKY[1])
for i in range(40): r = random.Random(i); d.point((r.randrange(5, 58), r.randrange(5, 90)), fill=IVORY[2])
d.rectangle([4, 82, 59, 91], fill=IVORY[2]); d.rectangle([30, 4, 33, 91], fill=WOOD[1]); d.rectangle([4, 46, 59, 49], fill=WOOD[1])
save(wn, "window_snow")
pk = new(32, 24, IVORY[2]); d = ImageDraw.Draw(pk); d.rectangle([0, 0, 31, 23], outline=IVORY[0]); d.rectangle([3, 3, 18, 20], fill=SKY[1])
d.rectangle([9, 8, 12, 20], fill=SALT[3]); d.rectangle([8, 6, 13, 8], fill=LAMP[2]); d.line([21, 6, 28, 6], fill=INK); d.line([21, 10, 28, 10], fill=INK); save(pk, "postcard")
af = new(32, 24, IVORY[2]); d = ImageDraw.Draw(af); d.rectangle([0, 0, 31, 23], outline=IVORY[0]); text(af, 3, 3, "ARKHAM", INK)
for y in (11, 15, 19): d.line([3, y, 28, y], fill=IVORY[0])
save(af, "admission")
sa = new(96, 8); d = ImageDraw.Draw(sa)
for x in range(0, 96): d.point((x, 6 - (x * 7 % 3)), fill=SALT[3])
save(sa, "salt_line")

# ================= items (24x24 tray icons) =================
def icon(): return new(24, 24)
k = icon(); d = ImageDraw.Draw(k); d.ellipse([2, 8, 9, 15], fill=IRON[3], outline=IRON[0]); d.rectangle([9, 11, 21, 12], fill=IRON[3]); d.rectangle([17, 13, 18, 16], fill=IRON[2]); d.arc([0, 2, 10, 16], 90, 270, fill=WOOD[1]); save(k, "item_locker_key")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([3, 15, 8, 20], fill=IRON[3], outline=IRON[0]); d.rectangle([5, 4, 6, 16], fill=IRON[3]); d.rectangle([5, 3, 18, 5], fill=IRON[3]); d.rectangle([16, 1, 20, 9], fill=WOOD[3]); save(k, "item_crank")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([4, 10, 15, 21], fill=RUST[2], outline=RUST[0]); d.line([15, 12, 22, 4], fill=RUST[2], width=2); d.arc([2, 6, 12, 16], 180, 300, fill=IRON[3]); save(k, "item_oil_can")
k = icon(); d = ImageDraw.Draw(k); d.arc([7, 1, 16, 9], 180, 360, fill=IRON[3]); d.rectangle([6, 6, 17, 8], fill=IRON[2]); d.rectangle([7, 8, 16, 19], fill=LAMP[1], outline=IRON[0]); d.rectangle([9, 10, 14, 17], fill=LAMP[3]); d.rectangle([5, 19, 18, 22], fill=IRON[2]); save(k, "item_lantern")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([1, 6, 12, 17], fill=IRON[3], outline=IRON[0]); d.ellipse([4, 9, 9, 14], fill=T); d.rectangle([12, 11, 22, 13], fill=IRON[3]); d.rectangle([18, 14, 22, 18], fill=IRON[3]); d.rectangle([14, 17, 18, 22], fill=IVORY[2]); save(k, "item_keeper_key")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([1, 7, 11, 16], fill=IRON[3], outline=IRON[0]); d.rectangle([11, 10, 22, 12], fill=IRON[3])
for x in (14, 17, 20): d.line([x, 13, x - 1, 17], fill=IRON[3])
d.line([2, 6, 0, 3], fill=IRON[3]); d.line([10, 6, 12, 3], fill=IRON[3]); save(k, "item_chest_key")
k = icon(); d = ImageDraw.Draw(k); d.polygon([(12, 1), (21, 8), (18, 21), (6, 21), (3, 8)], fill=(28, 40, 52), outline=(90, 200, 180)); d.line([7, 14, 9, 12, 12, 15, 15, 12, 17, 14], fill=GLOW); save(k, "item_seal_stone2")
print("seal 2 art written to", os.path.abspath(OUT))

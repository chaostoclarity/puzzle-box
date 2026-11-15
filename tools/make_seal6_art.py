"""Seal 6 art: the antechamber (room 11) and the hall of coffins (room 12) of the city under the sand.
Rule: 16 texels per world unit. Run: python3 tools/make_seal6_art.py  (writes assets/rooms/)
The keepers count in dots and bars: a dot is one, a bar is three (so 9 is three bars).
"""
from artkit import *

SAND  = [(70, 52, 34), (104, 78, 50), (140, 108, 70), (178, 142, 96), (214, 182, 132)]
DUNE  = [(120, 92, 58), (168, 132, 86), (206, 170, 116), (222, 190, 140), (236, 210, 166)]
BRONZE= [(52, 30, 14), (96, 58, 26), (146, 94, 40), (196, 138, 64), (232, 186, 110)]
CRYPT = [(18, 14, 12), (32, 26, 22), (48, 40, 32), (66, 56, 44), (88, 76, 60)]
OCHRE, TEAL, BLOOD = (170, 110, 40), (40, 110, 104), (110, 24, 20)
GLOW = (120, 255, 220)
WW, WH = 240, 352

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def numeral(img, x, y, n, col):
    """Dots and bars, read left to right: bars first (3 each), then dots. Bars are 2 wide and 7 tall, dots 2 x 2."""
    d = ImageDraw.Draw(img); cx = x
    for _ in range(n // 3):
        d.rectangle([cx, y, cx + 1, y + 6], fill=col); cx += 3
    for _ in range(n % 3):
        d.rectangle([cx, y + 2, cx + 1, y + 4], fill=col); cx += 3
    return cx - x

def numeral_w(n): return 3 * (n // 3 + n % 3) - 1

def carved_wall(seed, pal=SAND, rows=16):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            band = (y // rows) % 2
            c = pal[2 + band] if rnd.random() > 0.06 else pal[1]
            if y % rows == 0 or (x + (y // rows) * 37) % 60 == 0: c = pal[0]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    for i in range(10):   # low reptile friezes
        x, y = rnd.randrange(10, 220), rnd.randrange(200, 330)
        d.line([x, y, x + 14, y - 2], fill=pal[0]); d.line([x + 4, y, x + 2, y + 4], fill=pal[0]); d.line([x + 10, y - 1, x + 12, y + 3], fill=pal[0])
    return img

# ================= room 11: the antechamber =================
for k, s in zip("nesw", (201, 202, 203, 204)):
    save(carved_wall(s), "r11_wall_" + k)
f = grain(240, 240, DUNE, 205); d = ImageDraw.Draw(f)
for i in range(12): d.arc([i * 20 - 40, 60 + (i % 3) * 30, i * 20 + 60, 140 + (i % 3) * 30], 200, 340, fill=DUNE[0])
save(f, "r11_floor")
c = carved_wall(206).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c)
for i in range(6):
    x = 20 + i * 36; d.ellipse([x, 100, x + 24, 112], outline=SAND[0]); d.line([x + 24, 106, x + 34, 104], fill=SAND[0])
save(c, "r11_ceiling")
def low_door(open_):
    img = face(80, 64, SAND, 207, 3); d = ImageDraw.Draw(img)
    if open_:
        d.rectangle([6, 6, 73, 63], fill=(6, 4, 4))
    else:
        d.rectangle([6, 6, 73, 63], fill=SAND[1], outline=SAND[0]); d.ellipse([30, 20, 49, 39], outline=SAND[0])
        for a in range(0, 360, 45):
            d.line([39.5, 29.5, 39.5 + 9 * math.cos(math.radians(a)), 29.5 + 9 * math.sin(math.radians(a))], fill=SAND[0])
    return img
save(low_door(False), "low_door"); save(low_door(True), "low_door_open")
# lintel glyph: a 2x2 picture; the panel tiles must match it
# The keepers' glyph: 64 x 64, heavy strokes, no two quarters alike in any turn.
def make_glyph():
    g = new(64, 64); d = ImageDraw.Draw(g)
    d.arc([8, 6, 56, 54], 180, 360, fill=INK, width=5)       # a dome over the top half
    d.rectangle([30, 30, 34, 60], fill=INK)                   # a stem down the middle
    d.rectangle([4, 42, 26, 46], fill=INK)                    # a bar to the left
    d.ellipse([42, 36, 54, 48], fill=INK)                     # an eye to the right
    d.line([40, 54, 58, 60], fill=INK, width=4)               # a tail, bottom right
    d.rectangle([12, 14, 18, 20], fill=INK)                   # a notch, top left
    return g
GLYPH = make_glyph()
STONE_T = (214, 186, 136); STONE_E = (120, 92, 58)
def lintel_glyph(eroded):
    img = new(96, 48); d = ImageDraw.Draw(img); d.rectangle([0, 0, 95, 47], fill=STONE_T, outline=STONE_E, width=2)
    g = GLYPH.resize((44, 44), Image.NEAREST); img.paste(g, (26, 2), g)
    if eroded:
        px = img.load(); rnd = random.Random(208)
        for y in range(48):
            for x in range(96):
                if rnd.random() < 0.6 and px[x, y][:3] == INK: px[x, y] = STONE_T + (255,)
    return img
save(lintel_glyph(True), "lintel"); save(lintel_glyph(False), "lintel_lens")
gl = new(96, 48); px = gl.load(); src = lintel_glyph(False).load()
for y in range(48):
    for x in range(96):
        if src[x, y][:3] == INK: px[x, y] = GLOW + (255,)
save(gl, "lintel_glow")
# the 4 tiles: quarters of the glyph on plain stone, each can be turned
for q, (ox, oy) in enumerate(((0, 0), (32, 0), (0, 32), (32, 32))):
    part_ = GLYPH.crop((ox, oy, ox + 32, oy + 32))
    for r in range(4):
        tt = new(32, 32); d = ImageDraw.Draw(tt); d.rectangle([0, 0, 31, 31], fill=STONE_T, outline=STONE_E)
        rp = part_.rotate(-90 * r); tt.paste(rp, (0, 0), rp); d.rectangle([0, 0, 31, 31], outline=STONE_E)
        save(tt, "gtile_%d_%d" % (q, r))
gp = new(80, 80); d = ImageDraw.Draw(gp); d.rectangle([0, 0, 79, 79], fill=SAND[1], outline=SAND[0], width=2); d.rectangle([6, 6, 73, 73], fill=STONE_E); save(gp, "gpanel")
gk = new(16, 16); d = ImageDraw.Draw(gk); d.ellipse([0, 0, 15, 15], fill=BRONZE[3], outline=BRONZE[0]); d.ellipse([5, 5, 10, 10], fill=BRONZE[0]); save(gk, "gpanel_key")
# hourglass on a plinth: u = weight end up (1) or down (0); s = sand left in the top bulb, 0..5
def hglass(u, s, taken=False):
    """48 x 96: bronze frame, two clear bulbs, sand, and the stranded weight drawn big."""
    img = new(48, 96); d = ImageDraw.Draw(img)
    d.rectangle([2, 0, 45, 6], fill=BRONZE[3], outline=BRONZE[0]); d.rectangle([2, 89, 45, 95], fill=BRONZE[3], outline=BRONZE[0])
    for x in (4, 43): d.rectangle([x - 1, 7, x + 1, 88], fill=BRONZE[2])
    glass = (210, 232, 236)
    d.polygon([(9, 7), (38, 7), (26, 46), (21, 46)], fill=glass, outline=(90, 110, 120))
    d.polygon([(21, 49), (26, 49), (38, 88), (9, 88)], fill=glass, outline=(90, 110, 120))
    sand = (226, 176, 92)
    if s:   # sand in the top bulb, s of 5
        top = 45 - s * 7; half = int(2 + (45 - top) * 0.36)
        d.polygon([(23.5 - half, top), (23.5 + half, top), (26, 45), (21, 45)], fill=sand)
    b = 5 - s
    if b:
        top = 88 - b * 7; half = int(14 - (88 - top) * 0.2)
        d.polygon([(10, 88), (37, 88), (23.5 + half, top), (23.5 - half, top)], fill=sand)
    if 0 < b < 5: d.line([23, 47, 23, 87], fill=sand)
    if not taken:
        wy = 10 if u else 78
        buried = (u and s >= 3) or (not u and b >= 2)
        d.rectangle([17, wy, 30, wy + 8], fill=BRONZE[3] if not buried else BRONZE[1], outline=INK)
        if not buried: d.rectangle([22, wy - 3, 25, wy], fill=BRONZE[2])
    return img
for u in (0, 1):
    for s in range(6): save(hglass(u, s), "hglass_%d_%d" % (u, s))
save(hglass(1, 0, True), "hglass_taken")
pl = face(48, 48, SAND, 214, 2); save(pl, "plinth")
# offering niche: a carved mouth with a hand cut into the lip
def niche(open_):
    img = face(64, 64, SAND, 215, 3); d = ImageDraw.Draw(img)
    d.ellipse([12, 14, 51, 47], fill=(10, 6, 6) if open_ else SAND[0])
    if not open_:
        for x in range(16, 48, 6): d.polygon([(x, 14), (x + 4, 14), (x + 2, 24)], fill=SAND[3])
    d.polygon([(24, 52), (40, 52), (36, 62), (28, 62)], fill=SAND[1])
    return img
save(niche(False), "niche"); save(niche(True), "niche_open")
# scales: beam tilt -1 (left down), 0, 1 (right down)
def beam(t):
    img = new(128, 64); d = ImageDraw.Draw(img)
    d.rectangle([61, 14, 66, 63], fill=BRONZE[1]); d.polygon([(52, 63), (75, 63), (68, 54), (59, 54)], fill=BRONZE[2])
    dy = 10 * t
    d.line([8, 14 - dy, 119, 14 + dy], fill=BRONZE[3], width=3); d.ellipse([60, 10, 67, 17], fill=BRONZE[4])
    d.polygon([(62, 20), (65, 20), (63 - t * 6, 34)], fill=BLOOD)   # the pointer
    return img
for t, nm in ((-1, "l"), (0, "level"), (1, "r")): save(beam(t), "beam_" + nm)
pan = new(48, 24); d = ImageDraw.Draw(pan); d.line([4, 0, 0, 16], fill=BRONZE[1]); d.line([43, 0, 47, 16], fill=BRONZE[1]); d.chord([0, 6, 47, 23], 0, 180, fill=BRONZE[2], outline=BRONZE[0]); save(pan, "pan")
idol = new(24, 32); d = ImageDraw.Draw(idol); d.ellipse([4, 2, 19, 14], fill=TEAL); d.rectangle([6, 12, 17, 30], fill=TEAL); d.line([2, 20, 6, 18], fill=TEAL, width=2); d.point((8, 7), fill=BLOOD); d.point((15, 7), fill=BLOOD); save(idol, "idol")
for w in (1, 3, 9):
    s_ = 8 + (w // 3) * 2
    k = new(24, 24); d = ImageDraw.Draw(k); d.rectangle([12 - s_ // 2, 22 - s_, 11 + s_ // 2, 22], fill=BRONZE[2], outline=BRONZE[0]); d.rectangle([10, 22 - s_ - 3, 13, 22 - s_], fill=BRONZE[1])
    nw = numeral_w(w); numeral(k, 12 - nw // 2, 22 - s_ + 1 + max(0, s_ - 8) // 2, w, INK); save(k, "item_weight%d" % w); save(k, "wsprite_%d" % w)
alt = face(112, 48, SAND, 216, 3); d = ImageDraw.Draw(alt); d.rectangle([48, 14, 63, 29], fill=SAND[1], outline=SAND[0]); d.ellipse([51, 17, 60, 26], fill=BLOOD); save(alt, "altar_front")
save(face(112, 32, SAND, 217), "sand_top_112x32"); save(face(32, 48, SAND, 218), "sand_side_32x48")
ag = new(16, 16); d = ImageDraw.Draw(ag); d.rectangle([0, 0, 15, 15], fill=SAND[1], outline=SAND[0]); d.ellipse([3, 3, 12, 12], fill=BLOOD); save(ag, "altar_glyph")
dr = new(240, 32); d = ImageDraw.Draw(dr)
for x in range(0, 240, 3): d.line([x, 32, x + 8, 32 - (x * 7) % 18], fill=DUNE[(x // 3) % 3])
save(dr, "sand_drift")
k = new(24, 24); d = ImageDraw.Draw(k); d.ellipse([3, 3, 20, 20], fill=(30, 6, 6), outline=BLOOD); d.ellipse([8, 7, 15, 16], fill=OCHRE); d.ellipse([10, 9, 13, 14], fill=INK); save(k, "item_slot_eye")

# ================= room 12: the hall of coffins =================
for k, s in zip("nesw", (221, 222, 223, 224)):
    save(carved_wall(s, CRYPT, 22), "r12_wall_" + k)
f = grain(240, 240, CRYPT, 225); d = ImageDraw.Draw(f)
for i in range(0, 240, 30): d.line([i, 0, i, 239], fill=CRYPT[0]); d.line([0, i, 239, i], fill=CRYPT[0])
save(f, "r12_floor")
c = grain(240, 240, CRYPT, 226); d = ImageDraw.Draw(c); d.ellipse([70, 70, 169, 169], outline=CRYPT[4]); save(c, "r12_ceiling")
# mural strip: five panels, each the city with the sand higher (0 = no sand, 4 = buried)
def mural(k):
    """44 x 64. The city, and the sand rising over it: no sand (0) to buried (4)."""
    img = new(44, 64, (40, 60, 92)); d = ImageDraw.Draw(img)
    for i in range(8): d.point(((i * 13) % 40 + 2, (i * 7) % 18 + 2), fill=(230, 230, 240))
    towers = ((3, 30), (11, 42), (20, 24), (27, 36), (35, 28))
    for x, h in towers:
        d.rectangle([x, 60 - h, x + 6, 60], fill=TEAL, outline=(20, 60, 56))
        d.rectangle([x + 2, 60 - h + 4, x + 4, 60 - h + 7], fill=OCHRE)
    if k == 0:   # keepers in the street
        for x in (8, 18, 30): d.ellipse([x, 54, x + 5, 59], fill=OCHRE)
    if k:
        top = [60, 48, 36, 22, 2][k]
        d.polygon([(0, 63), (43, 63), (43, top + 4), (30, top), (14, top + 6), (0, top + 2)], fill=(214, 172, 104), outline=(150, 110, 60))
    d.rectangle([0, 0, 43, 63], outline=OCHRE, width=2)
    return img
for k in range(5): save(mural(k), "mural_%d" % k)
mf = new(232, 80); d = ImageDraw.Draw(mf); d.rectangle([0, 0, 231, 79], fill=CRYPT[1], outline=OCHRE, width=2); save(mf, "mural_frame")
ms = new(16, 16); d = ImageDraw.Draw(ms); d.ellipse([0, 0, 15, 15], fill=OCHRE, outline=CRYPT[0]); d.ellipse([5, 5, 10, 10], fill=CRYPT[0]); save(ms, "mural_stone")
# the hidden panel: a seven-fingered hand; five fingers marked, in dots and bars, with the order to press them
ORDER = [5, 2, 7, 1, 4]   # fingers (1..7, left to right) in the order to press
hp = new(44, 64, (30, 44, 70)); d = ImageDraw.Draw(hp)
d.ellipse([6, 36, 37, 60], fill=TEAL, outline=(20, 60, 56))
fx = [5, 10, 16, 21, 27, 32, 38]
for i, x in enumerate(fx):
    tip = 20 - (3 - abs(i - 3)) * 2
    d.rectangle([x - 1, tip, x + 1, 42], fill=TEAL)
for step_, finger in enumerate(ORDER):
    x = fx[finger - 1]; n = step_ + 1; y = 2
    for _ in range(n // 3): d.rectangle([x - 2, y, x + 2, y + 1], fill=(244, 226, 176)); y += 3
    for _ in range(n % 3): d.rectangle([x - 1, y, x, y + 1], fill=(244, 226, 176)); y += 3
d.rectangle([0, 0, 43, 63], outline=OCHRE, width=2)
save(hp, "mural_hand")
# upright coffin: a keeper's case, low and long, standing at a slant
def coffin_front(open_):
    img = face(64, 128, CRYPT, 227, 3); d = ImageDraw.Draw(img)
    d.polygon([(8, 4), (55, 4), (60, 40), (50, 123), (13, 123), (3, 40)], fill=CRYPT[3], outline=OCHRE)
    d.ellipse([22, 14, 41, 30], fill=TEAL)
    d.ellipse([18, 60, 45, 84], fill=CRYPT[1], outline=OCHRE)   # the palm
    plate_y = 100; d.rectangle([16, plate_y, 47, plate_y + 12], fill=BRONZE[2])
    numeral(img, 19, plate_y + 3, 3, INK); numeral(img, 34, plate_y + 3, 7, INK)
    return img
save(coffin_front(False), "coffin_front")
save(face(32, 128, CRYPT, 228), "crypt_side_32x128"); save(face(64, 32, CRYPT, 229), "crypt_top_64x32")
cl = new(64, 128); d = ImageDraw.Draw(cl); d.rectangle([4, 4, 59, 123], fill=(8, 6, 6)); save(cl, "coffin_inside")
mm = new(48, 112); d = ImageDraw.Draw(mm)
d.ellipse([12, 2, 35, 22], fill=(150, 140, 110)); d.rectangle([10, 20, 37, 104], fill=(140, 130, 100))
for y in range(24, 104, 5): d.line([10, y, 37, y + 2], fill=(110, 100, 80))
d.point((18, 10), fill=INK); d.point((29, 10), fill=INK)
for i in range(7): d.line([8 + i * 5, 64, 6 + i * 5, 74], fill=(130, 120, 90))
save(mm, "mummy")
mt = new(48, 112); text(mt, 8, 40, "E T", GLOW); text(mt, 6, 50, "HERE", GLOW); save(mt, "mummy_lens")
fp = new(12, 12); d = ImageDraw.Draw(fp); d.ellipse([0, 0, 11, 11], fill=TEAL, outline=CRYPT[0]); d.ellipse([3, 3, 8, 8], fill=CRYPT[1]); save(fp, "finger")
fp = new(12, 12); d = ImageDraw.Draw(fp); d.ellipse([0, 0, 11, 11], fill=OCHRE, outline=CRYPT[0]); d.ellipse([3, 3, 8, 8], fill=CRYPT[1]); save(fp, "finger_pulled")
# the keepers' reliquary: two rings of numerals 1..8, the inner for the birth flood, the outer for the sealing flood
for k, s in (("back", 230), ("side", 231), ("top", 232), ("front", 233)):
    save(face(96, 96, BRONZE, s, 3), "reli_" + k)
save(new(96, 96, (16, 10, 8)), "reli_liner")
def ring(size, r, seed, band=11):
    """A flat dark band with bold ivory numerals, so the dots and bars read at a glance."""
    img = new(size, size); d = ImageDraw.Draw(img); c = (size - 1) / 2
    d.ellipse([0, 0, size - 1, size - 1], fill=(36, 22, 12), outline=BRONZE[3])
    d.ellipse([c - r + band, c - r + band, c + r - band, c + r - band], fill=T, outline=BRONZE[3])
    for k in range(8):
        a = math.radians(-90 - k * 45 - 22.5)   # a thin divider between numerals
        d.line([c + (r - band) * math.cos(a), c + (r - band) * math.sin(a), c + (r - 1) * math.cos(a), c + (r - 1) * math.sin(a)], fill=BRONZE[1])
        a = math.radians(-90 - k * 45); x, y = c + (r - band / 2) * math.cos(a), c + (r - band / 2) * math.sin(a)
        n = k + 1; w = numeral_w(n); numeral(img, int(round(x - w / 2)), int(round(y - 3)), n, (244, 226, 176))
    return img
save(ring(72, 36, 234), "rring_o"); save(ring(48, 24, 235), "rring_i")
rp = new(12, 12); d = ImageDraw.Draw(rp); d.polygon([(6, 0), (11, 11), (0, 11)], fill=BLOOD); save(rp, "reli_pin")
mk = new(16, 8); d = ImageDraw.Draw(mk); d.polygon([(4, 0), (11, 0), (7, 7)], fill=BRONZE[4]); save(mk, "reli_mark")
stair = new(80, 160); d = ImageDraw.Draw(stair)
for i in range(10): d.rectangle([4 + i * 2, 150 - i * 15, 75 - i * 2, 159 - i * 15], fill=CRYPT[2 + i % 2], outline=CRYPT[0])
save(stair, "stair")
gate = new(80, 160); d = ImageDraw.Draw(gate)
for x in range(4, 80, 10): d.rectangle([x, 0, x + 3, 159], fill=BRONZE[1])
save(gate, "stair_gate")
k = new(24, 24); d = ImageDraw.Draw(k); d.polygon([(12, 1), (22, 9), (18, 22), (6, 22), (2, 9)], fill=TEAL, outline=GLOW); numeral(k, 7, 9, 6, INK); save(k, "item_seal_stone6")
print("seal 6 art written to", os.path.abspath(OUT))

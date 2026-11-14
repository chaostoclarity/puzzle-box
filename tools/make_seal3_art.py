"""Seal 3 art: Arkham Sanitarium. Ada Merrow's cell (room 5) and the records room (room 6).
Rule: 16 texels per world unit. Run: python3 tools/make_seal3_art.py  (writes assets/rooms/)
Placeholder art; sizes are the contract.
"""
from artkit import *

ASY   = [(36, 44, 40), (58, 70, 62), (84, 98, 88), (116, 130, 118), (156, 168, 156)]
TILE  = [(120, 126, 120), (164, 170, 162), (204, 208, 200), (222, 226, 218), (238, 240, 234)]
IRON  = [(20, 22, 26), (36, 38, 44), (54, 58, 66), (80, 86, 96), (112, 118, 128)]
STEEL = [(40, 44, 50), (70, 76, 86), (110, 116, 126), (150, 156, 166), (196, 200, 208)]
PAPER = [(150, 140, 116), (200, 190, 164), (232, 224, 200)]
OAK   = [(46, 30, 20), (72, 48, 30), (98, 66, 40), (126, 88, 54), (156, 114, 72)]
GLOW  = (120, 255, 220)
RED2  = (150, 34, 34)

def wood_face(w, h, seed, pal=WOOD, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def metal(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def lined_text(img, x, y, lines, col, gap=6):
    for i, line in enumerate(lines):
        text(img, x, y + i * gap, line, col)

# ================= walls =================
WW, WH = 240, 352
def cell_wall(seed, padded=False):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            c = ASY[2]
            if rnd.random() < 0.05: c = ASY[1]
            elif rnd.random() < 0.02: c = ASY[3]
            if y > WH - 120:  # tiled dado
                c = TILE[1] if (x // 16 + y // 16) % 2 else TILE[2]
                if x % 16 == 0 or y % 16 == 0: c = TILE[0]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    d.rectangle([0, WH - 122, WW, WH - 119], fill=ASY[0])
    d.rectangle([0, 0, WW, 11], fill=ASY[0])
    for i in range(30):   # water streaks and scuffs
        x = rnd.randrange(WW); d.line([x, 12, x + rnd.randrange(-3, 4), 12 + rnd.randrange(20, 80)], fill=ASY[1])
    return img
for k, s in zip("nesw", (51, 52, 53, 54)):
    save(cell_wall(s), "r5_wall_" + k)
f = new(240, 240); px = f.load()
for y in range(240):
    for x in range(240):
        c = TILE[1] if (x // 20 + y // 20) % 2 else TILE[2]
        if x % 20 == 0 or y % 20 == 0: c = TILE[0]
        px[x, y] = c + (255,)
save(f, "r5_floor")
c = cell_wall(55).crop((0, 20, 240, 260)); d = ImageDraw.Draw(c); save(c, "r5_ceiling")

def records_wall(seed):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            c = ASY[3] if y < 200 else OAK[2]
            if y >= 200 and (x % 40 == 0 or y % 50 == 0): c = OAK[0]
            if y < 200 and rnd.random() < 0.04: c = ASY[2]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img); d.rectangle([0, 196, WW, 203], fill=OAK[3]); d.rectangle([0, 0, WW, 15], fill=OAK[1])
    return img
for k, s in zip("nesw", (61, 62, 63, 64)):
    save(records_wall(s), "r6_wall_" + k)
f = grain(240, 240, OAK, 65, vertical=True); d = ImageDraw.Draw(f)
for y in range(0, 240, 30): d.line([0, y, 239, y], fill=OAK[0])
save(f, "r6_floor")
c = records_wall(66).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c)
d.ellipse([90, 90, 149, 149], fill=STEEL[1], outline=STEEL[3]); d.ellipse([104, 104, 135, 135], fill=(8, 8, 10))
d.rectangle([116, 0, 123, 90], fill=STEEL[2]); d.line([116, 0, 116, 90], fill=STEEL[3])
save(c, "r6_ceiling")

# ================= room 5: the cell =================
cot = new(128, 48); d = ImageDraw.Draw(cot)
d.rectangle([0, 0, 127, 47], fill=(0, 0, 0, 0))
d.rectangle([2, 0, 125, 18], fill=PAPER[1], outline=PAPER[0])
for x in range(8, 124, 12): d.line([x, 2, x, 16], fill=PAPER[0])
d.rectangle([0, 18, 127, 23], fill=IRON[3], outline=IRON[0])
for x in (2, 122): d.rectangle([x, 18, x + 3, 47], fill=IRON[3])
for x in range(10, 120, 8): d.arc([x, 24, x + 8, 40], 0, 360, fill=IRON[2])
save(cot, "cot_front")
save(metal(48, 48, IRON, 71), "iron_side_48x48")
ct = new(128, 48, PAPER[1]); d = ImageDraw.Draw(ct); d.rectangle([0, 0, 127, 47], outline=PAPER[0])
for y in range(4, 48, 8): d.line([2, y, 125, y], fill=PAPER[0])
save(ct, "cot_top")
sp = new(16, 16); d = ImageDraw.Draw(sp)
for i in range(4): d.arc([2, 2 + i * 3, 13, 7 + i * 3], 0, 360, fill=IRON[4])
d.line([13, 12, 15, 15], fill=IRON[4]); save(sp, "loose_spring")

def kerchief():
    img = new(48, 48, PAPER[2]); d = ImageDraw.Draw(img); d.rectangle([0, 0, 47, 47], outline=PAPER[0])
    for i in range(0, 48, 4): d.point((i, 0), fill=RED2); d.point((i, 47), fill=RED2)
    for c_ in range(3):
        for r in range(3):
            x, y = 9 + c_ * 12, 9 + r * 12
            d.rectangle([x, y, x + 8, y + 8], outline=PAPER[0])
            if c_ < 2 and GOAL[r * 3 + c_] == "1":
                d.line([x + 1, y + 1, x + 7, y + 7], fill=RED2); d.line([x + 7, y + 1, x + 1, y + 7], fill=RED2)
    d.polygon([(36, 0), (47, 0), (47, 47), (40, 47), (44, 30), (38, 14)], fill=(0, 0, 0, 0))   # right column torn away
    return img
GOAL = "001101001"
save(kerchief(), "kerchief")
cp = new(48, 48); d = ImageDraw.Draw(cp)
for r in range(3):
    x, y = 20, 9 + r * 12
    d.rectangle([x, y, x + 8, y + 8], outline=GLOW)
    if GOAL[r * 3 + 2] == "1": d.line([x + 1, y + 1, x + 7, y + 7], fill=GLOW); d.line([x + 7, y + 1, x + 1, y + 7], fill=GLOW)
text(cp, 8, 1, "MY LAST", GLOW); save(cp, "ceiling_pins")

def stool():
    img = new(32, 32); d = ImageDraw.Draw(img)
    d.rectangle([2, 4, 29, 9], fill=OAK[3], outline=OAK[0])
    for x in (5, 24): d.rectangle([x, 9, x + 2, 31], fill=OAK[2])
    d.line([7, 22, 24, 22], fill=OAK[1])
    return img
save(stool(), "stool")
for n in range(31):   # tally marks: one per turn, in groups of five
    t = new(48, 32); d = ImageDraw.Draw(t)
    for i in range(n):
        g, k = divmod(i, 5)
        gx, gy = 2 + (g % 3) * 15, 2 + (g // 3) * 15
        if k < 4: d.line([gx + k * 3, gy, gx + k * 3, gy + 10], fill=ASY[0])
        else: d.line([gx - 1, gy + 8, gx + 11, gy + 2], fill=ASY[0])
    save(t, "tally_%d" % n)
cw = new(64, 64, ASY[1]); d = ImageDraw.Draw(cw); d.rectangle([4, 4, 59, 59], fill=SKY[1])
for x in range(10, 60, 10): d.rectangle([x, 4, x + 2, 59], fill=IRON[2])
d.rectangle([0, 56, 63, 63], fill=ASY[3]); save(cw, "cell_window")
sl = new(64, 8, ASY[3]); d = ImageDraw.Draw(sl); d.line([0, 0, 63, 0], fill=ASY[4]); save(sl, "sill")
dr = new(32, 32, TILE[0]); d = ImageDraw.Draw(dr); d.ellipse([2, 2, 29, 29], fill=IRON[1], outline=IRON[3])
for x in range(6, 28, 4): d.line([x, 5, x, 26], fill=IRON[0])
d.point((18, 18), fill=BRASS[4]); d.point((19, 17), fill=BRASS[3]); save(dr, "drain")
dr2 = dr.copy(); d = ImageDraw.Draw(dr2); d.point((18, 18), fill=IRON[0]); d.point((19, 17), fill=IRON[0]); save(dr2, "drain_empty")
bc = new(32, 32); d = ImageDraw.Draw(bc); d.ellipse([6, 6, 25, 25], fill=PAPER[2]); d.ellipse([2, 2, 29, 29], outline=IRON[3])
for a in range(6): d.line([16, 16, 16 + 14 * math.cos(a), 16 + 14 * math.sin(a)], fill=IRON[3])
save(bc, "bulb_cage")
ws = metal(64, 64, TILE, 72, 2); d = ImageDraw.Draw(ws); d.ellipse([12, 4, 51, 20], fill=TILE[0]); save(ws, "washstand_front")
save(metal(32, 64, TILE, 73), "tile_side_32x64"); save(metal(64, 32, TILE, 74), "tile_top_64x32")
tm = new(32, 48, STEEL[2]); d = ImageDraw.Draw(tm); d.rectangle([0, 0, 31, 47], outline=STEEL[0]); d.line([4, 40, 26, 8], fill=STEEL[4]); save(tm, "tin_mirror")
cu = new(12, 12); d = ImageDraw.Draw(cu); d.rectangle([2, 3, 8, 11], fill=STEEL[3], outline=STEEL[0]); d.arc([7, 5, 11, 9], 270, 90, fill=STEEL[3]); save(cu, "tin_cup")
dn = new(32, 48, ASY[4]); d = ImageDraw.Draw(dn); d.rectangle([0, 0, 31, 47], outline=ASY[1])
lined_text(dn, 2, 3, ["IT WALKS", "WHEN I", "DO NOT", "WATCH.", "COUNT MY", "LOOKS. ON", "THE 4TH IT", "RESTS BY"], ASY[0])
save(dn, "ada_note")
def cell_door(open_):
    img = metal(80, 176, STEEL, 75, 3); d = ImageDraw.Draw(img)
    if open_:
        d.rectangle([6, 6, 73, 169], fill=(10, 10, 12)); d.rectangle([6, 6, 20, 169], fill=STEEL[1])
    else:
        d.rectangle([24, 30, 55, 41], fill=INK, outline=STEEL[0]); rivets_ = range(10, 70, 12)
        for x in rivets_: d.point((x, 8), fill=STEEL[4]); d.point((x, 166), fill=STEEL[4])
        d.rectangle([60, 80, 71, 100], fill=STEEL[1], outline=STEEL[0])
    return img
save(cell_door(False), "cell_door"); save(cell_door(True), "cell_door_open")
ts = new(16, 16, STEEL[1]); d = ImageDraw.Draw(ts); d.rectangle([0, 0, 15, 15], outline=STEEL[0]); d.rectangle([3, 3, 12, 12], fill=INK); save(ts, "tile_socket")
ts2 = new(16, 16, STEEL[1]); d = ImageDraw.Draw(ts2); d.rectangle([0, 0, 15, 15], outline=STEEL[0]); d.rectangle([3, 3, 12, 12], fill=VELVET[1]); stamp(ts2, 2, 2, sym_mask("eye"), GLOW)
save(ts2, "tile_socket_full")

# sewing box built from cot slats: 6 x 4 x 4
def slats(w, h, seed):
    img = new(w, h); px = img.load(); rnd = random.Random(seed)
    for y in range(h):
        for x in range(w):
            c = OAK[2] if (y // 8) % 2 else OAK[3]
            if y % 8 == 0: c = OAK[0]
            elif rnd.random() < 0.03: c = OAK[1]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img)
    for x in (2, w - 6): d.rectangle([x, 0, x + 3, h - 1], fill=IRON[2])
    return img
sf = slats(96, 64, 81); d = ImageDraw.Draw(sf); d.rectangle([40, 24, 55, 43], fill=IRON[2], outline=IRON[0]); d.ellipse([45, 28, 50, 33], fill=INK); d.rectangle([47, 33, 48, 39], fill=INK)
save(sf, "sew_front")
save(slats(96, 64, 82), "sew_back"); save(slats(64, 64, 83), "sew_side")
st = slats(96, 64, 84); d = ImageDraw.Draw(st); d.rectangle([24, 8, 71, 55], fill=PAPER[1], outline=OAK[0]); save(st, "sew_top")
sl_ = new(96, 64, (40, 20, 24)); d = ImageDraw.Draw(sl_)
d.line([16, 40, 26, 24, 34, 40, 44, 24, 52, 40, 62, 24, 70, 40, 80, 24], fill=PAPER[2], width=1)   # Ada's sketch of the pick: zigzag
text(sl_, 26, 50, "MY KEY", PAPER[2])
save(sl_.transpose(Image.ROTATE_180), "sew_liner")   # the floor liner is seen from above, turned round: draw it turned
pu = new(12, 12); d = ImageDraw.Draw(pu); d.ellipse([1, 1, 10, 10], fill=PAPER[0]); d.ellipse([4, 4, 7, 7], fill=STEEL[1]); save(pu, "pin_down")
pu = new(12, 12); d = ImageDraw.Draw(pu); d.ellipse([1, 1, 10, 10], fill=PAPER[0]); d.ellipse([3, 3, 8, 8], fill=RED2); d.point((4, 4), fill=(220, 120, 120)); save(pu, "pin_up")
nc = metal(96, 96, STEEL, 85, 3); d = ImageDraw.Draw(nc)
for i in range(6): d.arc([10 + i * 2, 10 + i * 2, 85 - i * 2, 85 - i * 2], 200, 340, fill=STEEL[3])
save(nc, "case_front")
for k, s in (("back", 86), ("side", 87), ("top", 88)): save(metal(96, 96, STEEL, s, 3), "case_" + k)
save(new(96, 96, VELVET[0]), "case_liner")
zk = new(16, 24, STEEL[1]); d = ImageDraw.Draw(zk); d.rectangle([0, 0, 15, 23], outline=STEEL[0]); d.line([8, 3, 5, 7, 11, 11, 5, 15, 8, 20], fill=INK, width=2); save(zk, "zig_keyhole")

# ================= room 6: records =================
WARDS = "ABCD"
dw = metal(128, 168, OAK, 91, 3); d = ImageDraw.Draw(dw)
for c_ in range(4):
    for r in range(4):
        x0, y0 = 4 + c_ * 30, 4 + r * 32
        d.rectangle([x0, y0, x0 + 27, y0 + 29], fill=OAK[2], outline=OAK[0])
        d.rectangle([x0 + 7, y0 + 5, x0 + 20, y0 + 12], fill=PAPER[2], outline=BRASS[0])
        text(dw, x0 + 9, y0 + 6, WARDS[c_] + str(r + 1), INK)
        d.rectangle([x0 + 9, y0 + 19, x0 + 18, y0 + 22], fill=BRASS[2])
d.rectangle([4, 136, 123, 163], fill=OAK[1], outline=OAK[0]); text(dw, 52, 138, "INDEX", BRASS[3])
save(dw, "drawers_front")
save(metal(32, 168, OAK, 92), "oak_side_32x168"); save(metal(128, 32, OAK, 93), "oak_top_128x32")
df = new(36, 36, OAK[0]); d = ImageDraw.Draw(df); d.rectangle([2, 2, 33, 33], fill=(10, 8, 6))
for i in range(5): d.rectangle([5 + i * 5, 6, 8 + i * 5, 30], fill=PAPER[1 + i % 2], outline=PAPER[0])
df = new(28, 32, OAK[0]); d = ImageDraw.Draw(df); d.rectangle([2, 2, 25, 29], fill=(10, 8, 6))
for i in range(4): d.rectangle([4 + i * 5, 6, 7 + i * 5, 27], fill=PAPER[1 + i % 2], outline=PAPER[0])
save(df, "drawer_out")
for i, ch in enumerate(WARDS):
    w_ = new(16, 16, PAPER[2]); d = ImageDraw.Draw(w_); d.rectangle([0, 0, 15, 15], outline=BRASS[0]); text(w_, 6, 5, ch, INK); save(w_, "ward_" + ch)
for i in range(4):
    w_ = new(16, 16, PAPER[2]); d = ImageDraw.Draw(w_); d.rectangle([0, 0, 15, 15], outline=BRASS[0]); text(w_, 6, 5, str(i + 1), INK); save(w_, "row_%d" % (i + 1))
lv = new(24, 16); d = ImageDraw.Draw(lv); d.rectangle([0, 10, 23, 15], fill=BRASS[1]); d.rectangle([10, 0, 13, 10], fill=IRON[3]); d.ellipse([8, 0, 15, 5], fill=RED2); save(lv, "index_lever")
dead = new(40, 24); text(dead, 2, 2, "DIED IN", GLOW); text(dead, 2, 9, "CARE", GLOW); text(dead, 2, 16, "1913", GLOW); save(dead, "ada_stamp")

lg = new(40, 24); d = ImageDraw.Draw(lg)
d.polygon([(0, 22), (19, 18), (19, 2), (0, 6)], fill=PAPER[2], outline=OAK[0]); d.polygon([(39, 22), (20, 18), (20, 2), (39, 6)], fill=PAPER[2], outline=OAK[0])
for y in range(8, 18, 2): d.line([3, y, 16, y - 2], fill=INK); d.line([23, y - 2, 36, y], fill=INK)
save(lg, "ledger")
fc = new(64, 80, PAPER[2]); d = ImageDraw.Draw(fc); d.rectangle([0, 0, 63, 79], outline=PAPER[0])
lined_text(fc, 3, 3, ["FILING", "", "WARD BY", "PATIENT NO.", "A  1-250", "B  251-500", "C  501-750", "D  751-1000", "", "ROW BY LAST", "DIGIT OF YR"], INK)
save(fc, "filing_chart")
fc2 = new(48, 32, PAPER[2]); d = ImageDraw.Draw(fc2); d.rectangle([0, 0, 47, 31], outline=PAPER[0])
lined_text(fc2, 3, 3, ["1 5 9  ROW 1", "2 6 0  ROW 2", "3 7    ROW 3", "4 8    ROW 4"], INK, 7)
save(fc2, "row_chart")
POSTER = ["RULES OF THE", "WARD.", "PATIENTS", "REST AFTER", "SUPPER. NO", "VISITORS.", "EXIT BY THE", "TWO GATES. 2", "LIGHTS OUT", "AT 10 SHARP.", "ROOMS 1-6."]
po = new(80, 96, PAPER[2]); d = ImageDraw.Draw(po); d.rectangle([0, 0, 79, 95], outline=PAPER[0])
lined_text(po, 3, 3, POSTER, INK, 8)
save(po, "ward_rules")
# the punch card's holes fall on E, X, T in EXIT, then 2 (TWO), 0 (OR... O), 6: drawn as a highlight overlay
def char_pos(line, col):
    x = 3
    for ch in POSTER[line][:col]: x += 3 if ch == " " else 4
    return x, 3 + line * 8
holes = [(6, 0), (6, 1), (6, 2), (7, 11), (9, 4), (10, 8)]   # E X T  2  0  6
gr = new(80, 96, (30, 26, 22)); d = ImageDraw.Draw(gr)
for (ln, col) in holes:
    x, y = char_pos(ln, col); d.rectangle([x - 1, y - 1, x + 3, y + 5], fill=(0, 0, 0, 0))
save(gr, "grille_overlay")
ph = wood_face(48, 64, 94, OAK); d = ImageDraw.Draw(ph)
d.ellipse([6, 6, 41, 41], fill=INK, outline=BRASS[1]); d.ellipse([18, 18, 29, 29], fill=PAPER[2])
d.rectangle([14, 48, 33, 58], fill=INK); d.rectangle([20, 44, 27, 48], fill=IRON[3])
save(ph, "phone_front")
for n in range(10):
    h_ = new(8, 8); d = ImageDraw.Draw(h_); d.ellipse([0, 0, 7, 7], fill=PAPER[2]); text(h_, 3, 2, str(n), INK); save(h_, "dial_%d" % n)
    h_ = new(8, 8); d = ImageDraw.Draw(h_); d.ellipse([0, 0, 7, 7], fill=BRASS[3]); text(h_, 3, 2, str(n), INK); save(h_, "dial_%d_lit" % n)
tb = new(48, 48); d = ImageDraw.Draw(tb); d.ellipse([0, 0, 47, 47], fill=STEEL[1], outline=STEEL[3]); d.ellipse([12, 12, 35, 35], fill=(8, 8, 10)); save(tb, "tube")
tb2 = tb.copy(); d = ImageDraw.Draw(tb2); d.ellipse([12, 12, 35, 35], fill=STEEL[0]); save(tb2, "tube_open")
cap = new(16, 24); d = ImageDraw.Draw(cap); d.rectangle([2, 0, 13, 23], fill=BRASS[2], outline=BRASS[0]); d.rectangle([2, 10, 13, 13], fill=STEEL[2]); save(cap, "capsule")
rd = metal(72, 144, OAK, 95, 3); d = ImageDraw.Draw(rd); d.rectangle([12, 12, 59, 70], outline=OAK[0]); d.rectangle([56, 72, 63, 80], fill=BRASS[2]); save(rd, "rec_door")
# lockbox (6 x 4 x 4) and the thimble box (6)
lbf = metal(96, 64, STEEL, 96, 3); d = ImageDraw.Draw(lbf); d.rectangle([40, 22, 55, 41], fill=STEEL[3], outline=STEEL[0]); d.ellipse([45, 26, 50, 31], fill=INK); d.rectangle([47, 31, 48, 37], fill=INK)
text(lbf, 48 - text_w("EFFECTS") // 2, 6, "EFFECTS", STEEL[0]); save(lbf, "lockbox_front")
save(metal(96, 64, STEEL, 97, 3), "lockbox_back"); save(metal(64, 64, STEEL, 98, 3), "lockbox_side"); save(metal(96, 64, STEEL, 99, 3), "lockbox_top")
save(new(96, 64, (24, 20, 18)), "lockbox_liner")
def bone(w, h, seed):
    pal = [(60, 54, 44), (120, 110, 92), (176, 164, 136), (210, 200, 172), (236, 228, 204)]
    img = grain(w, h, pal, seed); bevel(img, pal, 3); return img
tf = bone(96, 96, 101); d = ImageDraw.Draw(tf); d.polygon([(46, 6), (50, 6), (48, 10)], fill=RED2)
text(tf, 6, 86, "IN MEMORIAM 1...", (60, 54, 44)); save(tf, "thim_front")
for k, s in (("back", 102), ("side", 103), ("top", 104)): save(bone(96, 96, s), "thim_" + k)
save(new(96, 96, (30, 22, 20)), "thim_liner")
def num_ring(size, inner, digits_r):
    img = new(size, size); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=PAPER[1], outline=OAK[0])
    if inner: d.ellipse([inner, inner, size - 1 - inner, size - 1 - inner], fill=(0, 0, 0, 0), outline=OAK[0])
    c_ = size / 2
    for k in range(10):
        a = -math.pi / 2 - k * 2 * math.pi / 10   # digits run counterclockwise, so turning clockwise brings the next one up
        x = c_ + digits_r * math.cos(a) - 1.5; y = c_ + digits_r * math.sin(a) - 2.5
        text(img, round(x), round(y), str(k), INK)
    return img
save(num_ring(72, 10, 30), "nring_0"); save(num_ring(52, 10, 20), "nring_1"); save(num_ring(32, 0, 10), "nring_2")
pin = new(12, 12); d = ImageDraw.Draw(pin); d.ellipse([0, 0, 11, 11], fill=RED2, outline=OAK[0]); d.point((4, 4), fill=(220, 120, 120)); save(pin, "thim_pin")

# ================= items =================
def icon(): return new(24, 24)
k = icon(); d = ImageDraw.Draw(k); d.line([3, 20, 20, 3], fill=IRON[4], width=1); save(k, "item_wire")
k = icon(); d = ImageDraw.Draw(k); d.line([12, 21, 12, 6], fill=IRON[4]); d.arc([6, 2, 17, 12], 180, 360, fill=IRON[4]); d.line([6, 7, 7, 10], fill=IRON[4]); save(k, "item_wire_hook")
k = icon(); d = ImageDraw.Draw(k); d.line([12, 21, 12, 15, 8, 12, 15, 9, 9, 6, 12, 3], fill=IRON[4]); save(k, "item_wire_zigzag")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([2, 6, 13, 17], fill=BRASS[2], outline=BRASS[0]); d.ellipse([5, 9, 10, 14], fill=T); d.rectangle([13, 10, 15, 13], fill=BRASS[2]); d.line([16, 9, 16, 14], fill=BRASS[0]); save(k, "item_key_bow")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([3, 10, 20, 12], fill=BRASS[2]); d.rectangle([15, 13, 17, 17], fill=BRASS[1]); d.rectangle([19, 13, 20, 15], fill=BRASS[1]); d.line([2, 9, 2, 14], fill=BRASS[0]); save(k, "item_key_blade")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([1, 6, 10, 15], fill=BRASS[2], outline=BRASS[0]); d.ellipse([4, 9, 7, 12], fill=T); d.rectangle([10, 10, 21, 11], fill=BRASS[2]); d.rectangle([16, 12, 17, 15], fill=BRASS[1]); d.line([11, 8, 11, 13], fill=BRASS[4]); save(k, "item_sew_key")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([5, 6, 18, 21], fill=BRASS[2], outline=BRASS[0]); d.ellipse([8, 9, 15, 18], fill=BRASS[3]); d.line([11, 1, 11, 6], fill=BRASS[1]); save(k, "item_locket")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([5, 5, 18, 18], fill=VELVET[1], outline=BRASS[1]); stamp(k, 6, 6, sym_mask("eye"), GLOW); save(k, "item_tile")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([2, 5, 21, 18], fill=PAPER[2], outline=PAPER[0])
for (x, y) in [(5, 8), (9, 8), (13, 12), (17, 9), (7, 14), (15, 15)]: d.rectangle([x, y, x + 1, y + 1], fill=INK)
save(k, "item_punch_card")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([2, 7, 11, 16], fill=STEEL[3], outline=STEEL[0]); d.ellipse([5, 10, 8, 13], fill=T); d.rectangle([11, 10, 21, 12], fill=STEEL[3]); d.rectangle([17, 13, 19, 16], fill=STEEL[2]); save(k, "item_lockbox_key")
k = icon(); d = ImageDraw.Draw(k); d.polygon([(12, 1), (21, 8), (18, 21), (6, 21), (3, 8)], fill=(44, 40, 30), outline=(90, 200, 180)); d.line([8, 10, 16, 10], fill=GLOW); d.line([8, 14, 16, 14], fill=GLOW); save(k, "item_seal_stone3")
# examine views
ex = new(96, 72, (30, 24, 20)); d = ImageDraw.Draw(ex); d.ellipse([18, 6, 77, 65], fill=BRASS[2], outline=BRASS[0]); d.ellipse([24, 12, 71, 59], fill=(60, 52, 44))
d.ellipse([36, 18, 59, 44], fill=(150, 130, 110)); d.rectangle([32, 44, 63, 59], fill=(36, 32, 40)); d.rectangle([40, 28, 43, 30], fill=INK); d.rectangle([52, 28, 55, 30], fill=INK)
save(ex, "examine_locket")
ex = new(96, 72, (30, 24, 20)); d = ImageDraw.Draw(ex); d.rectangle([8, 10, 87, 61], fill=PAPER[2], outline=PAPER[0])
for (x, y) in [(20, 22), (34, 22), (48, 30), (62, 24), (26, 44), (56, 48)]: d.rectangle([x, y, x + 3, y + 3], fill=(30, 24, 20))
text(ex, 12, 13, "WARD 9 TABULATOR", INK); save(ex, "examine_punch_card")
print("seal 3 art written to", os.path.abspath(OUT))

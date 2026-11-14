"""Seal 4 art: the Gardner farm west of Arkham. The kitchen (room 7) and the well house (room 8).
Rule: 16 texels per world unit. Run: python3 tools/make_seal4_art.py  (writes assets/rooms/)
Placeholder art; sizes are the contract.
"""
from artkit import *

ASH   = [(46, 46, 44), (72, 72, 68), (100, 100, 94), (132, 132, 124), (168, 168, 158)]
GREYW = [(40, 36, 32), (62, 56, 50), (84, 78, 70), (108, 102, 92), (134, 128, 116)]
ROOT  = [(70, 70, 66), (110, 108, 100), (160, 158, 148)]
SOIL  = [(40, 30, 22), (62, 46, 32)]
LEAF  = [(40, 70, 36), (70, 110, 54), (110, 150, 80)]
STONE2 = [(34, 34, 38), (56, 56, 62), (80, 80, 88), (108, 108, 116), (140, 140, 148)]
IRON  = [(20, 22, 26), (36, 38, 44), (54, 58, 66), (80, 86, 96), (112, 118, 128)]
PAPER = [(150, 140, 116), (200, 190, 164), (232, 224, 200)]
GLOW  = (120, 255, 220)
VEL5 = [(34, 9, 16), (58, 15, 27), (86, 24, 40), (120, 40, 60), (150, 60, 80)]
PURPLE = [(70, 40, 90), (130, 80, 170), (200, 150, 240)]   # the colour out of space

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def roots_over(img, seed, n=6, col=ROOT):
    d = ImageDraw.Draw(img); rnd = random.Random(seed)
    for i in range(n):
        x, y = rnd.randrange(img.width), 0
        while y < img.height:
            nx = x + rnd.randrange(-3, 4); ny = y + rnd.randrange(3, 8)
            d.line([x, y, nx, ny], fill=col[rnd.randrange(2)], width=1 + (i % 2)); x, y = nx, ny

WW, WH = 240, 352
def farm_wall(seed):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            k = x // 20
            c = GREYW[2] if k % 2 else GREYW[3]
            if x % 20 == 0: c = GREYW[0]
            elif rnd.random() < 0.03: c = GREYW[1]
            px[x, y] = c + (255,)
    d = ImageDraw.Draw(img); d.rectangle([0, 0, WW, 14], fill=GREYW[0]); d.rectangle([0, WH - 10, WW, WH], fill=GREYW[0])
    roots_over(img, seed, 4)
    return img
for k, s in zip("nesw", (71, 72, 73, 74)):
    save(farm_wall(s), "r7_wall_" + k)
f = new(240, 240); px = f.load(); rnd = random.Random(75)
for y in range(240):
    for x in range(240):
        c = GREYW[2] if (y // 24) % 2 else GREYW[3]
        if y % 24 == 0: c = GREYW[0]
        if rnd.random() < 0.08: c = ASH[3]
        px[x, y] = c + (255,)
d = ImageDraw.Draw(f); d.ellipse([70, 70, 169, 169], outline=ASH[4]); d.ellipse([90, 90, 149, 149], outline=PURPLE[0])
save(f, "r7_floor")
c = farm_wall(76).crop((0, 0, 240, 240)); d = ImageDraw.Draw(c)
for y in (30, 110, 190): d.rectangle([0, y, 239, y + 14], fill=GREYW[1], outline=GREYW[0])
roots_over(c, 77, 14)
save(c, "r7_ceiling")

# ---- pie safe: front 96 x 160 (6 x 10) ----
pf = face(96, 160, GREYW, 81, 3); d = ImageDraw.Draw(pf)
d.rectangle([8, 28, 87, 92], fill=IRON[2], outline=IRON[0])          # punched tin panel (root grid)
for y in range(32, 90, 4):
    for x in range(12, 86, 4): d.point((x, y), fill=IRON[3])
d.rectangle([8, 104, 87, 148], fill=GREYW[1], outline=GREYW[0])      # jar shelf
for i, m in enumerate(["MAR", "MAY", "JUN"]):
    cx = 24 + i * 24
    text(pf, cx - text_w(m) // 2, 136, m, PAPER[2])
save(pf, "piesafe_front")
save(face(40, 160, GREYW, 82), "grey_side_40x160"); save(face(96, 40, GREYW, 83), "grey_top_96x40")
lt = new(16, 12); d = ImageDraw.Draw(lt); d.rectangle([0, 3, 15, 8], fill=BRASS[1], outline=BRASS[0]); d.rectangle([6, 0, 9, 11], fill=BRASS[2]); save(lt, "latch_shut")
lo = new(16, 12); d = ImageDraw.Draw(lo); d.rectangle([0, 3, 15, 8], fill=BRASS[1], outline=BRASS[0]); d.rectangle([12, 0, 15, 11], fill=BRASS[3]); save(lo, "latch_open")
rt = new(32, 24); roots_over(rt, 84, 7); d = ImageDraw.Draw(rt); d.line([0, 12, 31, 10], fill=ROOT[0], width=3); save(rt, "root_knot")
def tile(state):
    img = new(12, 12, IRON[1]); d = ImageDraw.Draw(img); d.rectangle([0, 0, 11, 11], outline=IRON[0])
    pts = {0: [(1, 10), (10, 1)], 1: [(0, 6), (11, 6)], 2: [(1, 1), (10, 10)], 3: [(6, 0), (6, 11)]}[state]
    d.line(pts, fill=IRON[3], width=2)
    return img
for s in range(4): save(tile(s), "rtile_%d" % s)
st = new(12, 12, IRON[1]); d = ImageDraw.Draw(st); d.ellipse([2, 2, 9, 9], fill=ROOT[1]); save(st, "root_stub")
bl = new(12, 12, IRON[0]); save(bl, "rivet_block")
ml = new(12, 12, IRON[1]); d = ImageDraw.Draw(ml); d.rectangle([2, 4, 9, 7], fill=BRASS[1]); save(ml, "mlatch_shut")
ml = new(12, 12, IRON[1]); d = ImageDraw.Draw(ml); d.rectangle([2, 4, 9, 7], fill=BRASS[3]); d.line([2, 2, 9, 9], fill=ROOT[2]); save(ml, "mlatch_open")
save(Image.new("RGBA", (6, 4), ROOT[1] + (255,)), "seg_root_h"); save(Image.new("RGBA", (4, 6), ROOT[1] + (255,)), "seg_root_v")
CROPS = ["peas", "corn", "squash", "wheat", "apple", "bean"]
def crop(i):
    img = new(16, 16, PAPER[1]); d = ImageDraw.Draw(img); d.rectangle([0, 0, 15, 15], outline=PAPER[0])
    if i == 0: [d.ellipse([3 + k * 3, 6, 5 + k * 3, 8], fill=LEAF[2]) for k in range(3)]; d.arc([2, 4, 13, 11], 180, 360, fill=LEAF[1])
    if i == 1: d.ellipse([6, 2, 9, 13], fill=(220, 190, 70)); d.line([5, 6, 4, 13], fill=LEAF[1]); d.line([10, 6, 11, 13], fill=LEAF[1])
    if i == 2: d.ellipse([3, 5, 12, 12], fill=(220, 140, 50)); d.line([7, 2, 8, 5], fill=LEAF[0])
    if i == 3: [d.line([4 + k * 3, 13, 5 + k * 3, 3], fill=(210, 180, 100)) for k in range(3)]
    if i == 4: d.ellipse([4, 5, 11, 12], fill=(170, 40, 40)); d.line([7, 2, 8, 5], fill=LEAF[0])
    if i == 5: d.arc([3, 3, 12, 14], 200, 340, fill=LEAF[2], width=2)
    return img
for i in range(6): save(crop(i), "crop_%d" % i)
jl = new(16, 8); d = ImageDraw.Draw(jl); d.rectangle([0, 1, 15, 6], fill=BRASS[1], outline=BRASS[0]); save(jl, "jar_latch")
al = new(64, 80, PAPER[1]); d = ImageDraw.Draw(al); d.rectangle([0, 0, 63, 79], outline=PAPER[0]); text(al, 4, 3, "ALMANAC 1882", INK)
for i, m in enumerate(["MAR", "APR", "MAY", "JUN"]):
    y = 14 + i * 15; text(al, 4, y, m, INK); d.rectangle([20, y - 1, 59, y + 7], fill=ASH[2])
save(al, "almanac")
alx = new(64, 80)
for i, cname in enumerate(["PEAS", "WHEAT", "CORN", "SQUASH"]):
    text(alx, 22, 14 + i * 15, cname, GLOW)
save(alx, "almanac_lens")
def flower(stage):
    img = new(16, 32); d = ImageDraw.Draw(img)
    d.polygon([(4, 31), (11, 31), (13, 20), (2, 20)], fill=(90, 110, 130), outline=(50, 60, 70))
    droop = stage * 1.5
    col = [(200, 60, 90), (190, 70, 90), (170, 90, 100), (150, 110, 110), (130, 120, 116), (120, 118, 112), (110, 110, 104), (100, 100, 96), (92, 92, 88)][stage]
    sx, sy = 8 + droop * 0.6, 5 + droop
    d.line([7, 20, sx, sy], fill=LEAF[1] if stage < 5 else ASH[2])
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 2], fill=col)
    return img
for s in range(9): save(flower(s), "flower_%d" % s)
nn = new(32, 24, PAPER[2]); d = ImageDraw.Draw(nn); d.rectangle([0, 0, 31, 23], outline=PAPER[0])
for y in range(4, 22, 3): d.line([3, y, 28, y], fill=ASH[1])
save(nn, "nahum_notes")
def pot(stage):
    img = new(24, 32); d = ImageDraw.Draw(img)
    d.polygon([(4, 31), (19, 31), (22, 18), (1, 18)], fill=(150, 80, 50), outline=(90, 50, 30)); d.rectangle([1, 16, 22, 19], fill=SOIL[1])
    if stage >= 1: d.line([11, 16, 11, 12], fill=LEAF[1])
    if stage >= 2: d.line([11, 12, 9, 4], fill=LEAF[1]); d.line([11, 12, 15, 6], fill=LEAF[1]); d.ellipse([12, 4, 17, 8], fill=LEAF[2])
    if stage == 3: d.arc([5, 4, 12, 15], 300, 120, fill=LEAF[2], width=2)
    if stage == 4: d.arc([5, 4, 12, 15], 300, 120, fill=ASH[3], width=2)
    if stage >= 4: d.ellipse([12, 4, 17, 8], fill=ASH[2])
    if stage == 5: d.line([11, 16, 6, 10], fill=ASH[1]); d.line([6, 10, 4, 14], fill=ASH[1])
    return img
for s in range(6): save(pot(s), "pot_%d" % s)
pe = new(24, 32); d = ImageDraw.Draw(pe); d.polygon([(4, 31), (19, 31), (22, 18), (1, 18)], fill=(150, 80, 50), outline=(90, 50, 30)); d.rectangle([1, 16, 22, 19], fill=SOIL[0]); save(pe, "pot_empty")
stv = face(64, 64, IRON, 85, 2); d = ImageDraw.Draw(stv); d.rectangle([12, 16, 51, 44], fill=IRON[0]); save(stv, "stove_front")
save(face(32, 64, IRON, 86), "iron_side_32x64")
win = new(64, 64, GREYW[1]); d = ImageDraw.Draw(win); d.rectangle([4, 4, 59, 59], fill=ASH[3])
for i in range(20): r_ = random.Random(i); d.point((r_.randrange(5, 58), r_.randrange(5, 58)), fill=PURPLE[1])
d.rectangle([30, 4, 33, 59], fill=GREYW[1]); d.rectangle([4, 30, 59, 33], fill=GREYW[1]); save(win, "farm_window")
bd = face(72, 144, GREYW, 87, 3); d = ImageDraw.Draw(bd); d.rectangle([56, 72, 63, 80], fill=IRON[3]); save(bd, "back_door")
bdo = new(72, 144, (60, 60, 56)); d = ImageDraw.Draw(bdo); d.rectangle([0, 0, 71, 143], outline=GREYW[0]); d.rectangle([4, 100, 67, 143], fill=ASH[2]); save(bdo, "back_door_open")
dr = new(80, 96); roots_over(dr, 88, 10); d = ImageDraw.Draw(dr); d.line([0, 50, 79, 46], fill=ROOT[0], width=4); d.line([4, 20, 76, 70], fill=ROOT[1], width=2); save(dr, "door_roots")
tb = face(112, 56, GREYW, 89, 2); save(tb, "table_front"); save(face(112, 48, GREYW, 90), "grey_top_112x48"); save(face(48, 56, GREYW, 91), "grey_side_48x56")
sh = new(32, 24); d = ImageDraw.Draw(sh); d.line([4, 4, 26, 18], fill=IRON[4], width=2); d.line([4, 18, 26, 4], fill=IRON[4], width=2); d.ellipse([0, 0, 8, 8], outline=(150, 40, 40), width=2); d.ellipse([0, 16, 8, 23], outline=(150, 40, 40), width=2)
save(sh, "shears_part")
sp = new(12, 16, PAPER[1]); d = ImageDraw.Draw(sp); d.rectangle([0, 0, 11, 15], outline=PAPER[0]); d.ellipse([3, 5, 8, 10], fill=LEAF[1]); save(sp, "seed_packet")
# bread tin (6x4x4) and Abby's box (6)
btf = face(96, 64, [(70, 20, 20), (110, 40, 36), (150, 60, 50), (180, 90, 70), (210, 130, 100)], 92, 3); d = ImageDraw.Draw(btf)
text(btf, 48 - text_w("BREAD") // 2, 8, "BREAD", PAPER[2])
d.rectangle([40, 26, 55, 45], fill=IRON[2], outline=IRON[0]); d.arc([43, 29, 52, 42], 300, 120, fill=INK, width=2); save(btf, "tin_front2")
for k, s in (("back", 93), ("top", 94)): save(face(96, 64, [(70, 20, 20), (110, 40, 36), (150, 60, 50), (180, 90, 70), (210, 130, 100)], s, 3), "btin_" + k)
save(face(64, 64, [(70, 20, 20), (110, 40, 36), (150, 60, 50), (180, 90, 70), (210, 130, 100)], 95, 3), "btin_side")
save(new(96, 64, (40, 20, 18)), "btin_liner")
ab = face(96, 96, VEL5, 96, 3); d = ImageDraw.Draw(ab); stamp(ab, 42, 42, sym_mask("moon"), BRASS[3]); save(ab, "abby_front")
for k, s in (("back", 97), ("side", 98), ("top", 99)): save(face(96, 96, VEL5, s, 3), "abby_" + k)
abb = face(96, 96, VEL5, 100, 3); d = ImageDraw.Draw(abb); text(abb, 48 - text_w("PRESS") // 2, 30, "PRESS", BRASS[1]); save(abb, "abby_bottom")
save(new(96, 96, (30, 10, 16)), "abby_liner")
btn = new(16, 16); d = ImageDraw.Draw(btn); d.ellipse([0, 0, 15, 15], fill=BRASS[1], outline=BRASS[0]); d.ellipse([4, 4, 11, 11], fill=BRASS[3]); save(btn, "abby_button")

# ================= room 8: the well house =================
def well_wall(seed):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            c = GREYW[2] if (x // 16) % 2 else GREYW[1]
            if x % 16 == 0: c = GREYW[0]
            if y > WH - 80: c = STONE2[2] if ((x + (y // 16) * 8) // 16 + y // 16) % 2 else STONE2[1]
            if rnd.random() < 0.02: c = ASH[2]
            px[x, y] = c + (255,)
    roots_over(img, seed, 3)
    return img
for k, s in zip("nesw", (101, 102, 103, 104)):
    save(well_wall(s), "r8_wall_" + k)
wf = new(240, 240, STONE2[1]); d = ImageDraw.Draw(wf)
for y in range(0, 240, 16):
    for x in range(0, 240, 24): d.rectangle([x + (y // 16 % 2) * 12, y, x + 23 + (y // 16 % 2) * 12, y + 15], outline=STONE2[0])
d.ellipse([50, 50, 189, 189], fill=STONE2[3], outline=STONE2[0]); d.ellipse([66, 66, 173, 173], fill=(4, 4, 6))
save(wf, "r8_floor")
wc = well_wall(105).crop((0, 0, 240, 240)); d = ImageDraw.Draw(wc); d.rectangle([0, 100, 239, 139], fill=GREYW[3], outline=GREYW[0]); save(wc, "r8_ceiling")
def drum(depth):
    img = new(160, 48); d = ImageDraw.Draw(img)
    d.rectangle([0, 10, 159, 37], fill=GREYW[3], outline=GREYW[0])
    turns = 6 - depth
    for i in range(turns): d.line([30 + i * 16, 10, 38 + i * 16, 37], fill=IRON[3], width=2)
    d.rectangle([150, 18, 159, 29], fill=IRON[2])
    return img
for k in range(6): save(drum(k), "drum_%d" % k)
hd = new(24, 24); d = ImageDraw.Draw(hd); d.rectangle([0, 9, 15, 14], fill=IRON[3]); d.rectangle([14, 2, 19, 21], fill=IRON[3]); d.rectangle([16, 18, 23, 23], fill=WOOD[3]); save(hd, "handle_fitted")
def shaft(depth):
    img = new(112, 112); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, 111, 111], fill=(4, 4, 6))
    r = 50 - depth * 8
    for k in range(depth + 1): d.ellipse([56 - 50 + k * 8, 56 - 50 + k * 8, 56 + 50 - k * 8, 56 + 50 - k * 8], outline=STONE2[0])
    d.line([56, 0, 56, 56 - r // 3], fill=IRON[3])
    if depth > 0:
        s = max(4, 18 - depth * 3); d.rectangle([56 - s // 2, 56 - r // 3, 56 + s // 2, 56 - r // 3 + s], fill=GREYW[3])
    return img
for k in range(6): save(shaft(k), "shaft_%d" % k)
CARV = {1: "I 7", 3: "II 2", 5: "III 4"}   # no 6 or 9: the floor can be seen upside down
for k in range(6):
    cv = new(112, 112)
    if k in CARV:
        txt = CARV[k]; text(cv, 56 - text_w(txt, 2) // 2, 20, txt, GLOW, 2)
    save(cv, "carv_%d" % k)
bf = face(96, 96, GREYW, 106, 3); d = ImageDraw.Draw(bf)
for i, x in enumerate((20, 48, 76)):
    d.ellipse([x - 10, 30, x + 10, 50], outline=GREYW[0])
d.ellipse([38, 32, 58, 52], fill=GREYW[1])   # the phantom dial's shadow: visible without the Lens
d.rectangle([4, 4, 91, 12], fill=IRON[2]); save(bf, "bucket_front")
for k, s in (("back", 107), ("side", 108), ("top", 109)): save(face(96, 96, GREYW, s, 3), "bucket_" + k)
save(new(96, 96, (20, 18, 16)), "bucket_liner")
for i in range(10):
    dd = new(16, 16); d = ImageDraw.Draw(dd); d.ellipse([0, 0, 15, 15], fill=PAPER[2], outline=IRON[0]); text(dd, 6, 5, str(i), INK); save(dd, "wdial_%d" % i)
    dd = new(16, 16); d = ImageDraw.Draw(dd); d.ellipse([0, 0, 15, 15], outline=GLOW); text(dd, 6, 5, str(i), GLOW); save(dd, "pdial_%d" % i)
bp = new(12, 12); d = ImageDraw.Draw(bp); d.rectangle([0, 0, 11, 11], fill=IRON[3], outline=IRON[0]); d.rectangle([4, 4, 7, 7], fill=IRON[1]); save(bp, "bucket_pin")
jf = face(96, 96, STONE2, 110, 3); d = ImageDraw.Draw(jf); roots_over(jf, 111, 12); save(jf, "jar_front")
for k, s in (("back", 112), ("side", 113), ("top", 114)): save(face(96, 96, STONE2, s, 3), "jar_" + k)
save(new(96, 96, (12, 10, 14)), "jar_liner")
jr = new(64, 64); roots_over(jr, 115, 16); d = ImageDraw.Draw(jr); d.line([0, 32, 63, 30], fill=ROOT[0], width=4); save(jr, "jar_roots")
kn = new(16, 16, GREYW[2]); d = ImageDraw.Draw(kn); d.ellipse([3, 3, 12, 12], fill=GREYW[0]); save(kn, "knothole")
wn = new(48, 64); text(wn, 2, 2, "WREN", GLOW); d = ImageDraw.Draw(wn); d.rectangle([2, 10, 45, 61], outline=GLOW); save(wn, "post_note")
rack = new(64, 48); d = ImageDraw.Draw(rack); d.rectangle([0, 0, 63, 5], fill=GREYW[3])
for x in (8, 26, 44): d.line([x, 5, x + 4, 46], fill=IRON[3], width=2)
save(rack, "tool_rack")
sdoor = face(72, 144, GREYW, 116, 3); save(sdoor, "shed_door")

# ================= items =================
def icon(): return new(24, 24)
k = icon(); d = ImageDraw.Draw(k); d.line([4, 4, 19, 17], fill=IRON[4], width=2); d.line([4, 17, 19, 4], fill=IRON[4], width=2); d.ellipse([0, 0, 6, 6], outline=(150, 40, 40), width=2); d.ellipse([0, 15, 6, 21], outline=(150, 40, 40), width=2); save(k, "item_shears")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([5, 3, 18, 20], fill=PAPER[1], outline=PAPER[0]); d.ellipse([8, 8, 15, 15], fill=LEAF[1]); save(k, "item_seeds")
k = icon(); d = ImageDraw.Draw(k); d.arc([4, 2, 19, 21], 300, 120, fill=LEAF[2], width=3); d.ellipse([10, 4, 13, 7], fill=LEAF[1]); save(k, "item_pod_key")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([2, 10, 15, 13], fill=IRON[3]); d.rectangle([14, 3, 18, 20], fill=IRON[3]); d.rectangle([16, 16, 22, 21], fill=WOOD[3]); save(k, "item_handle")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([1, 6, 12, 17], fill=GREYW[3], outline=GREYW[0]); d.ellipse([4, 9, 9, 14], fill=T); d.rectangle([12, 11, 22, 13], fill=GREYW[3]); d.rectangle([18, 14, 21, 18], fill=GREYW[3]); save(k, "item_back_key")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([4, 4, 19, 19], fill=(60, 120, 110), outline=SILVER[2]); d.ellipse([8, 7, 12, 11], fill=(180, 255, 230)); save(k, "item_lens_element")
k = icon(); d = ImageDraw.Draw(k); d.ellipse([2, 3, 15, 16], fill=(60, 120, 110), outline=BRASS[2], width=2); d.ellipse([8, 8, 21, 21], fill=(40, 100, 120), outline=SILVER[2], width=2); d.ellipse([11, 11, 14, 14], fill=(180, 255, 230)); save(k, "item_lens2")
k = icon(); d = ImageDraw.Draw(k); d.polygon([(12, 1), (21, 8), (18, 21), (6, 21), (3, 8)], fill=(60, 60, 58), outline=(90, 200, 180)); d.ellipse([9, 9, 14, 14], fill=PURPLE[1]); save(k, "item_seal_stone4")
print("seal 4 art written to", os.path.abspath(OUT))

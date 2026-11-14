"""Seal 7 art: the violist's garret (room 13) and the impossible street (room 14).
Rule: 16 texels per world unit. Run: python3 tools/make_seal7_art.py  (writes assets/rooms/)
"""
from artkit import *

ROOF  = [(40, 30, 26), (62, 46, 38), (86, 64, 50), (112, 86, 66), (140, 110, 86)]
PLAST = [(96, 90, 80), (130, 122, 108), (160, 152, 134), (188, 180, 160), (212, 206, 188)]
SLATE = [(24, 26, 34), (36, 40, 52), (52, 58, 72), (72, 80, 96), (96, 104, 120)]
NIGHT = [(6, 8, 18), (12, 16, 32), (22, 28, 52)]
LAMP, BLUE, RED3, GLOW = (255, 210, 120), (40, 70, 140), (140, 40, 40), (120, 255, 220)
WW, WH = 240, 352

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def wave(img, x0, y0, w, h, bumps, col):
    d = ImageDraw.Draw(img); pts = []
    for x in range(w):
        pts.append((x0 + x, y0 + h / 2 - (h / 2 - 1) * math.sin(x / (w - 1) * bumps * math.pi)))
    d.line(pts, fill=col)

# ================= room 13: the garret =================
def garret_wall(seed, slope):
    img = grain(WW, WH, PLAST, seed); d = ImageDraw.Draw(img)
    for y in range(0, WH, 44): d.line([0, y, WW, y], fill=PLAST[1])
    if slope:   # the roof comes down across the top of the wall
        d.polygon([(0, 0), (WW, 0), (WW, 60), (0, 140)], fill=ROOF[2])
        for x in range(0, WW, 24): d.line([x, 0, x, 140 - x * 80 // WW], fill=ROOF[0])
    return img
for k, s, sl in (("n", 241, True), ("e", 242, False), ("s", 243, True), ("w", 244, False)):
    save(garret_wall(s, sl), "r13_wall_" + k)
f = grain(240, 240, ROOF, 245); d = ImageDraw.Draw(f)
for y in range(0, 240, 20): d.line([0, y, 239, y], fill=ROOF[0])
save(f, "r13_floor")
c = grain(240, 240, ROOF, 246); d = ImageDraw.Draw(c)
for x in range(0, 240, 24): d.line([x, 0, x, 239], fill=ROOF[0], width=3)
save(c, "r13_ceiling")
def gwindow(state):
    img = new(80, 96, ROOF[1]); d = ImageDraw.Draw(img); d.rectangle([6, 6, 73, 89], fill=NIGHT[1])
    if state == "void":
        rnd = random.Random(247)
        for i in range(140): d.point((rnd.randrange(8, 72), rnd.randrange(8, 88)), fill=[(255, 255, 255), GLOW, (200, 120, 255)][i % 3])
        d.ellipse([28, 30, 52, 60], outline=(200, 120, 255))
    else:
        for i in range(5): d.rectangle([10 + i * 13, 60 - (i * 7) % 20, 19 + i * 13, 89], fill=SLATE[2]); d.point((14 + i * 13, 70), fill=LAMP)
    if state == "shut":
        d.rectangle([6, 6, 73, 89], fill=RED3); [d.line([x, 6, x, 89], fill=(110, 30, 30)) for x in range(10, 74, 8)]
    d.line([40, 6, 40, 89], fill=ROOF[1], width=2); d.line([6, 48, 73, 48], fill=ROOF[1], width=2)
    return img
for st in ("shut", "street", "void"): save(gwindow(st), "gwin_" + st)
def viol():
    img = new(64, 144); d = ImageDraw.Draw(img)
    d.ellipse([10, 70, 53, 130], fill=(120, 60, 24), outline=(60, 28, 10)); d.ellipse([14, 40, 49, 84], fill=(120, 60, 24), outline=(60, 28, 10))
    d.rectangle([28, 4, 35, 60], fill=(40, 24, 16)); d.rectangle([22, 104, 41, 108], fill=(60, 40, 24))
    d.arc([18, 80, 28, 96], 90, 270, fill=INK); d.arc([36, 80, 46, 96], 270, 90, fill=INK)
    for x in (24, 30, 34, 40): d.line([x, 106, 30 + (x - 32) // 4, 6], fill=(40, 24, 16))
    d.rectangle([22, 140, 41, 143], fill=ROOF[0]); d.line([31, 128, 31, 143], fill=ROOF[0], width=2)
    return img
save(viol(), "viol")
for k in range(4):
    s_ = new(4, 96); d = ImageDraw.Draw(s_); d.line([1, 0, 1, 95], fill=SILVER[2 + k % 2]); save(s_, "vstring_%d" % k)
    s_ = new(4, 96); d = ImageDraw.Draw(s_); [d.point((0 + (y // 3) % 3, y), fill=GLOW) for y in range(96)]; save(s_, "vstring_%d_hum" % k)
nb = new(40, 28); d = ImageDraw.Draw(nb); d.rectangle([0, 0, 39, 27], fill=IVORY[2], outline=INK); d.line([20, 0, 20, 27], fill=INK)
for y in range(5, 25, 4): d.line([3, y, 17, y], fill=IVORY[0]); d.line([23, y, 36, y], fill=IVORY[0])
save(nb, "notebook")
bed = new(112, 48); d = ImageDraw.Draw(bed); d.rectangle([0, 14, 111, 32], fill=PLAST[3], outline=ROOF[0]); d.rectangle([0, 32, 111, 38], fill=ROOF[2])
d.rectangle([2, 4, 26, 16], fill=IVORY[2]); [d.rectangle([x, 38, x + 3, 47], fill=ROOF[1]) for x in (2, 106)]; save(bed, "gbed")
fk = new(16, 48); d = ImageDraw.Draw(fk); d.line([5, 2, 5, 28], fill=SILVER[3], width=2); d.line([10, 2, 10, 28], fill=SILVER[3], width=2); d.line([5, 28, 10, 28], fill=SILVER[3]); d.line([7, 28, 7, 46], fill=SILVER[2], width=2); save(fk, "fork")
fl = new(16, 48); wave(fl, 1, 4, 14, 20, 5, GLOW); save(fl, "fork_lens")
ds = face(96, 64, ROOF, 248, 2); save(ds, "gdesk_front"); save(face(96, 32, ROOF, 249), "roof_top_96x32"); save(face(32, 64, ROOF, 250), "roof_side_32x64")
hatch = face(48, 48, ROOF, 251, 3); save(hatch, "dumb_hatch")
ho = new(48, 48, (10, 8, 8)); d = ImageDraw.Draw(ho); d.rectangle([0, 0, 47, 47], outline=ROOF[0]); d.rectangle([4, 30, 43, 33], fill=ROOF[2]); save(ho, "dumb_hatch_open")
gd = face(64, 144, ROOF, 252, 3); d = ImageDraw.Draw(gd); d.ellipse([50, 70, 55, 75], fill=BRASS[2]); save(gd, "gdoor")
rs = new(12, 8); d = ImageDraw.Draw(rs); d.rectangle([1, 1, 10, 6], fill=(170, 120, 40), outline=(90, 60, 20)); save(rs, "rosin_floor")
# viol case: 8 x 3 x 3, black leather, three pegs in the lid that each tune a little wire
def case_face(w, h, seed):
    img = face(w, h, SLATE, seed, 2); d = ImageDraw.Draw(img); d.rectangle([0, 0, w - 1, h - 1], outline=BRASS[1]); return img
save(case_face(128, 48, 253), "vcase_front"); save(case_face(128, 48, 254), "vcase_back"); save(case_face(48, 48, 255), "vcase_side"); save(case_face(128, 48, 256), "vcase_top")
li = new(128, 48, VELVET[1]); text(li, 6, 4, "FROM THE BRIDGE", IVORY[1]); text(li, 6, 12, "E  A  D  G", IVORY[2]); save(li, "vcase_liner")
for k in range(7):
    p = new(16, 32); d = ImageDraw.Draw(p); d.rectangle([5, 0, 10, 10], fill=BRASS[2], outline=BRASS[0]); d.rectangle([1, 12, 14, 31], fill=SLATE[0]); wave(p, 2, 14, 12, 16, k + 1, SILVER[3]); save(p, "vpeg_%d" % k)
cl = new(16, 16); d = ImageDraw.Draw(cl); d.rectangle([2, 4, 13, 11], fill=BRASS[2], outline=BRASS[0]); d.line([4, 8, 11, 8], fill=BRASS[0]); save(cl, "vcase_clasp")
bw = new(16, 112); d = ImageDraw.Draw(bw); d.line([4, 4, 6, 108], fill=(80, 50, 24), width=2); d.line([10, 4, 10, 100], fill=IVORY[2]); save(bw, "bow_inside")

# ================= room 14: the street =================
def facade(name, seed):
    img = grain(WW, WH, PLAST if name not in ("church", "stairs") else SLATE, seed); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, WW - 1, 60], fill=NIGHT[1])
    rnd = random.Random(seed)
    for i in range(30): d.point((rnd.randrange(WW), rnd.randrange(60)), fill=(220, 220, 240))
    d.polygon([(0, 60), (WW, 60), (WW, 90), (0, 90)], fill=ROOF[1])
    for x in range(20, 220, 60): d.rectangle([x, 120, x + 30, 170], fill=NIGHT[2], outline=ROOF[0])
    d.rectangle([0, 320, WW - 1, WH - 1], fill=SLATE[1])
    return img
fac = {}
im = facade("home", 261); d = ImageDraw.Draw(im); d.rectangle([90, 210, 149, 319], fill=ROOF[1], outline=ROOF[0]); text(im, 104, 196, "N 7", INK); d.rectangle([100, 120, 139, 170], fill=LAMP); fac["home"] = im
im = facade("bakery", 262); d = ImageDraw.Draw(im); d.rectangle([40, 220, 199, 319], fill=(70, 50, 30)); [d.line([40, y, 199, y], fill=(40, 30, 20)) for y in range(224, 320, 6)]; text(im, 80, 200, "PATISSERIE", INK); fac["r1"] = im
im = facade("poster", 263); d = ImageDraw.Draw(im); d.rectangle([60, 180, 179, 300], fill=IVORY[2], outline=INK); text(im, 82, 190, "RECITAL", RED3)
text(im, 70, 210, "THE MUTE", INK); text(im, 70, 220, "VIOLIST", INK); text(im, 70, 240, "PLAYS IT", INK); text(im, 70, 250, "BACKWARD", INK); text(im, 70, 260, "WHEN THE", INK); text(im, 70, 270, "COCK FACES", INK); text(im, 70, 280, "THE WIND", INK); fac["r2"] = im
def bluehouse(open_):
    im = facade("blue", 264); d = ImageDraw.Draw(im); d.rectangle([90, 210, 149, 319], fill=(4, 4, 8) if open_ else BLUE, outline=INK); d.ellipse([136, 260, 141, 265], fill=BRASS[3])
    return im
fac["r3"] = bluehouse(False); save(bluehouse(True), "fac_r3_open")
im = facade("chimney", 265); d = ImageDraw.Draw(im); d.rectangle([150, 20, 169, 62], fill=ROOF[0])
for i in range(8): d.ellipse([150 - i * 14, 10 - i * 2, 166 - i * 14, 22 - i * 2], fill=PLAST[2 + i % 2])   # smoke drifting left
cx, cy = 120, 250; d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=INK)
for txt, (dx, dy) in (("N", (0, -24)), ("E", (24, 0)), ("S", (0, 24)), ("O", (-24, 0))): text(im, cx + dx - 1, cy + dy - 2, txt, INK)
d.line([cx, cy - 18, cx, cy + 18], fill=INK); d.line([cx - 18, cy, cx + 18, cy], fill=INK); fac["r4"] = im
im = facade("stairs", 266); d = ImageDraw.Draw(im)
for i in range(8): d.rectangle([60 + i * 6, 200 + i * 15, 179 - i * 6, 212 + i * 15], fill=SLATE[2 + i % 2])
[d.line([x, 190, x, 320], fill=INK, width=2) for x in range(60, 182, 12)]; fac["l1"] = im
im = facade("church", 267); d = ImageDraw.Draw(im); d.polygon([(70, 90), (170, 90), (120, 40)], fill=SLATE[2]); d.line([120, 40, 120, 10], fill=INK)
d.rectangle([100, 230, 139, 319], fill=ROOF[0]); d.arc([100, 210, 139, 250], 180, 360, fill=ROOF[0], width=3)
d.line([150, 100, 150, 300], fill=(150, 120, 80), width=2); fac["l2"] = im
for k, im in fac.items(): save(im, "fac_" + k)
for k, s in zip("nesw", (268, 269, 270, 271)): save(grain(WW, WH, SLATE, s), "r14_wall_" + k)
f = grain(240, 240, SLATE, 272); d = ImageDraw.Draw(f)
for y in range(0, 240, 12):
    for x in range((y // 12) % 2 * 6, 240, 12): d.rectangle([x, y, x + 10, y + 10], outline=SLATE[0])
save(f, "r14_floor")
c = new(240, 240, NIGHT[0]); rnd = random.Random(273); d = ImageDraw.Draw(c)
for i in range(200): d.point((rnd.randrange(240), rnd.randrange(240)), fill=(220, 220, 240))
save(c, "r14_ceiling")
def vane(k):
    img = new(48, 48); d = ImageDraw.Draw(img); a = math.radians(-90 + k * 45); c = 23.5
    x1, y1 = c + 20 * math.cos(a), c + 20 * math.sin(a); x0, y0 = c - 16 * math.cos(a), c - 16 * math.sin(a)
    d.line([x0, y0, x1, y1], fill=INK, width=2); d.polygon([(x1, y1), (x1 - 6 * math.cos(a - 0.5), y1 - 6 * math.sin(a - 0.5)), (x1 - 6 * math.cos(a + 0.5), y1 - 6 * math.sin(a + 0.5))], fill=INK)
    d.ellipse([c - 5, c - 9, c + 5, c + 1], fill=RED3)   # the cock
    return img
for k in range(8): save(vane(k), "vane_%d" % k)
vb = new(48, 48); d = ImageDraw.Draw(vb); d.line([23, 10, 23, 47], fill=INK, width=2)
for txt, (dx, dy) in (("N", (0, -20)), ("E", (20, 0)), ("S", (0, 20)), ("O", (-20, 0))): text(vb, 22 + dx, 22 + dy, txt, IVORY[2])
save(vb, "vane_bare")
rope = new(8, 96); d = ImageDraw.Draw(rope); d.line([3, 0, 4, 95], fill=(150, 120, 80), width=2); d.ellipse([0, 86, 7, 95], fill=(120, 90, 60)); save(rope, "bell_rope")
# music box on the cobbles: four keys and a crank
for k, s in (("front", 274), ("back", 275), ("side", 276), ("top", 277)): save(face(96, 64 if k != "side" else 64, WOOD, s, 3), "mbox_" + k)
save(new(96, 64, VELVET[0]), "mbox_liner")
for L in "GDAE":
    kk = new(16, 32); d = ImageDraw.Draw(kk); d.rectangle([1, 0, 14, 31], fill=IVORY[2], outline=INK); text(kk, 6, 22, L, INK); save(kk, "mkey_" + L.lower())
    kk = new(16, 32); d = ImageDraw.Draw(kk); d.rectangle([1, 4, 14, 31], fill=IVORY[1], outline=INK); text(kk, 6, 22, L, INK); save(kk, "mkey_" + L.lower() + "_pulled")
def icon(): return new(24, 24)
k = icon(); d = ImageDraw.Draw(k); d.line([3, 21, 20, 3], fill=(80, 50, 24), width=2); d.line([6, 21, 22, 6], fill=IVORY[2]); save(k, "item_bow")
k = icon(); d = ImageDraw.Draw(k); d.line([3, 21, 20, 3], fill=(80, 50, 24), width=2); d.line([6, 21, 22, 6], fill=(255, 220, 140)); d.point((14, 13), fill=(255, 255, 255)); save(k, "item_rosined_bow")
k = icon(); d = ImageDraw.Draw(k); d.rectangle([6, 8, 17, 15], fill=(170, 120, 40), outline=(90, 60, 20)); save(k, "item_rosin")
k = icon(); d = ImageDraw.Draw(k); d.line([2, 12, 21, 12], fill=INK, width=2); d.polygon([(21, 12), (16, 8), (16, 16)], fill=INK); d.ellipse([8, 4, 14, 10], fill=RED3); save(k, "item_vane_cock")
k = icon(); d = ImageDraw.Draw(k); d.polygon([(12, 1), (22, 9), (18, 22), (6, 22), (2, 9)], fill=(140, 120, 200), outline=GLOW); d.line([7, 16, 17, 8], fill=INK); save(k, "item_seal_stone7")
print("seal 7 art written to", os.path.abspath(OUT))

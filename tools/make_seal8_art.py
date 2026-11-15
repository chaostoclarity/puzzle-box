"""Seal 8 art: the dreaming study (room 15) and the cellar that loops (room 16).
Rule: 16 texels per world unit. Run: python3 tools/make_seal8_art.py  (writes assets/rooms/)
The dreaming study reuses Thorne's study (hub) walls and furniture; these are the dream's additions.
"""
from artkit import *

BRICK = [(50, 26, 22), (74, 38, 30), (96, 50, 38), (118, 64, 48), (140, 82, 62)]
DREAM = (200, 170, 255)
WAX = [(200, 190, 160), (230, 222, 196), (250, 246, 230)]
FLAME = [(255, 160, 40), (255, 220, 120)]
WW, WH = 240, 352

def face(w, h, pal, seed, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

def clock(h, mirrored=False):
    img = new(48, 48); d = ImageDraw.Draw(img); c = 23.5
    d.ellipse([0, 0, 47, 47], fill=IVORY[2], outline=WOOD[0]); d.ellipse([2, 2, 45, 45], outline=WOOD[2])
    for k in range(12):
        a = math.radians(-90 + k * 30); x, y = c + 19 * math.cos(a), c + 19 * math.sin(a)
        d.rectangle([x - 1, y - 1, x, y], fill=INK)
    for k, s in ((0, "XII"), (3, "III"), (6, "VI"), (9, "IX")):
        a = math.radians(-90 + k * 30); x, y = c + 14 * math.cos(a), c + 14 * math.sin(a); w = text_w(s)
        text(img, int(x - w / 2), int(y - 2), s, INK)
    a = math.radians(-90 + h * 30); d.line([c, c, c + 11 * math.cos(a), c + 11 * math.sin(a)], fill=INK, width=2)
    d.line([c, c, c, c - 16], fill=INK)
    if mirrored: img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img
for h in range(12): save(clock(h), "dclock_%d" % h)
pend = new(16, 48); d = ImageDraw.Draw(pend); d.line([8, 0, 8, 36], fill=BRASS[2]); d.ellipse([3, 34, 12, 43], fill=BRASS[3], outline=BRASS[0]); save(pend, "pendulum")
pend = new(16, 48); d = ImageDraw.Draw(pend); d.line([8, 0, 3, 36], fill=BRASS[2]); d.ellipse([0, 34, 8, 43], fill=BRASS[1], outline=BRASS[0]); save(pend, "pendulum_stopped")
# the mirror: in it, the waking study, messy, and the clock stopped at three, seen backwards
mi = new(48, 80, (40, 44, 56)); d = ImageDraw.Draw(mi); d.rectangle([0, 0, 47, 79], outline=BRASS[1], width=2)
cm = clock(3).resize((24, 24), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT); mi.paste(cm, (12, 8), cm)
rnd = random.Random(281)
for i in range(14): x, y = rnd.randrange(6, 40), rnd.randrange(40, 74); d.rectangle([x, y, x + 6, y + 4], fill=IVORY[rnd.randrange(3)])
d.rectangle([14, 56, 34, 70], fill=WOOD[1]); d.ellipse([20, 48, 28, 56], fill=(90, 70, 60))   # a man asleep at the desk
save(mi, "dmirror")
note = new(32, 24); d = ImageDraw.Draw(note); d.rectangle([0, 0, 31, 23], fill=(250, 246, 236), outline=IVORY[0]); text(note, 3, 3, "SLEEP", INK); text(note, 3, 10, "WELL", INK); text(note, 3, 17, "2 2 2", INK); save(note, "dnote")
pp = new(32, 32); d = ImageDraw.Draw(pp); d.rectangle([2, 2, 29, 29], outline=DREAM)
text(pp, 6, 6, "4", DREAM); d.line([14, 6, 16, 12], fill=DREAM); text(pp, 22, 6, "8", DREAM); text(pp, 4, 18, "MID IS", DREAM); text(pp, 4, 24, "WOKE", DREAM); save(pp, "pinned_lens")
hd = new(32, 24); d = ImageDraw.Draw(hd); d.rectangle([0, 0, 31, 23], fill=WOOD[2], outline=WOOD[0]); d.rectangle([12, 10, 19, 13], fill=BRASS[2]); save(hd, "ddrawer")
hd = new(32, 24, (10, 6, 4)); d = ImageDraw.Draw(hd); d.rectangle([0, 0, 31, 23], outline=WOOD[0]); save(hd, "ddrawer_open")
dl = new(48, 24); d = ImageDraw.Draw(dl); d.rectangle([0, 0, 47, 23], fill=WOOD[1], outline=WOOD[0]); d.rectangle([18, 9, 29, 14], fill=BRASS[2]); save(dl, "dcab_lock")
for k in range(10):
    dd = new(16, 16); d = ImageDraw.Draw(dd); d.ellipse([0, 0, 15, 15], fill=BRASS[2], outline=BRASS[0]); d.ellipse([2, 2, 13, 13], fill=IVORY[2]); text(dd, 6, 5, str(k), INK); save(dd, "ddial_%d" % k)
def candle(n, lit=True):
    img = new(16, 48); d = ImageDraw.Draw(img); top = 10 + n * 6
    d.rectangle([4, top, 11, 45], fill=WAX[1], outline=WAX[0]); d.rectangle([1, 44, 14, 47], fill=BRASS[1])
    for i in range(1, 5):
        y = 10 + i * 6
        if y > top: d.line([4, y, 7, y], fill=WOOD[0])
    for i in range(n): d.line([8, 46 - i * 2, 11, 46 - i * 2], fill=(140, 30, 30))   # notches you cut
    if lit: d.polygon([(8, top - 7), (10, top - 2), (6, top - 2)], fill=FLAME[1]); d.point((8, top - 3), fill=FLAME[0])
    return img
for n in range(5): save(candle(n), "dcandle_%d" % n)
k = new(24, 24); d = ImageDraw.Draw(k); d.ellipse([3, 3, 20, 20], fill=(150, 130, 220), outline=DREAM); d.ellipse([8, 8, 15, 15], outline=(255, 255, 255)); save(k, "item_dream_glass")
k = new(24, 24); d = ImageDraw.Draw(k); d.ellipse([2, 2, 21, 21], outline=BRASS[2], width=2); d.ellipse([5, 5, 18, 18], fill=(110, 90, 200)); d.ellipse([9, 9, 14, 14], fill=DREAM); save(k, "item_lens3")
k = new(24, 24); d = ImageDraw.Draw(k); d.rectangle([9, 6, 14, 21], fill=WAX[1]); d.polygon([(11, 1), (13, 5), (10, 5)], fill=FLAME[1]); save(k, "item_candle")

# ================= room 16: the cellar =================
def brick_wall(seed):
    img = new(WW, WH); px = img.load(); rnd = random.Random(seed)
    for y in range(WH):
        for x in range(WW):
            row = y // 8; off = 8 if row % 2 else 0
            c = BRICK[0] if y % 8 == 0 or (x + off) % 16 == 0 else BRICK[1 + (((x + off) // 16 + row) * 7 % 3)]
            if rnd.random() < 0.03: c = BRICK[0]
            px[x, y] = c + (255,)
    return img
for k, s in zip("nesw", (291, 292, 293, 294)): save(brick_wall(s), "r16_wall_" + k)
f = grain(240, 240, STONE, 295); save(f, "r16_floor")
c = grain(240, 240, DARKW, 296); d = ImageDraw.Draw(c)
for x in range(0, 240, 40): d.rectangle([x, 0, x + 12, 239], fill=DARKW[0])
save(c, "r16_ceiling")
rack = new(96, 112); d = ImageDraw.Draw(rack)
for y in range(0, 112, 16):
    d.line([0, y, 95, y], fill=WOOD[1], width=2)
    for x in range(6, 96, 14): d.ellipse([x, y + 3, x + 10, y + 13], fill=(30, 40, 30), outline=(10, 14, 10))
for x in (0, 94): d.line([x, 0, x, 111], fill=WOOD[1], width=2)
save(rack, "wine_rack")
lab = new(20, 12); d = ImageDraw.Draw(lab); d.rectangle([0, 0, 19, 11], fill=IVORY[2], outline=INK); text(lab, 2, 3, "I 3", INK); save(lab, "label_1")
chute = new(64, 64); d = ImageDraw.Draw(chute); d.polygon([(0, 0), (63, 0), (48, 63), (16, 63)], fill=STONE[1], outline=STONE[0]); d.rectangle([20, 50, 44, 63], fill=(10, 10, 10)); save(chute, "coal_chute")
lab = new(24, 12); d = ImageDraw.Draw(lab); text(lab, 2, 3, "II 1", (220, 220, 220)); save(lab, "label_2")
grate = new(48, 48); d = ImageDraw.Draw(grate); d.rectangle([0, 0, 47, 47], fill=(10, 10, 10), outline=STONE[2])
for x in range(4, 48, 8): d.line([x, 0, x, 47], fill=STONE[3], width=2)
save(grate, "cellar_grate")
lab = new(32, 12); d = ImageDraw.Draw(lab); text(lab, 2, 3, "III 2", (200, 220, 160)); save(lab, "label_3")
dr = face(80, 144, WOOD, 297, 3); d = ImageDraw.Draw(dr); [d.line([x, 0, x, 143], fill=WOOD[0]) for x in (26, 52)]; save(dr, "cellar_door")
dro = new(80, 144, (6, 6, 8)); d = ImageDraw.Draw(dro)
for i in range(8): d.rectangle([10, 130 - i * 16, 69, 138 - i * 16], fill=STONE[1 + i % 2])
save(dro, "cellar_door_open")
hn = new(16, 16); d = ImageDraw.Draw(hn); d.rectangle([2, 6, 13, 9], fill=IRON2 if False else (60, 60, 70)); d.ellipse([11, 4, 15, 11], fill=(90, 90, 100)); save(hn, "cellar_handle")
ww = new(48, 64); d = ImageDraw.Draw(ww); text(ww, 2, 4, "WAKE", DREAM); text(ww, 2, 12, "UP", DREAM); text(ww, 2, 24, "ELIAS", DREAM); text(ww, 2, 36, "IT IS", DREAM); text(ww, 2, 44, "ONLY", DREAM); text(ww, 2, 52, "A LOOP", DREAM); save(ww, "wren_lens3")
sh = new(96, 32); d = ImageDraw.Draw(sh); d.rectangle([0, 20, 95, 24], fill=WOOD[2]); [d.rectangle([x, 4, x + 10, 20], fill=(60 + x, 50, 40)) for x in range(4, 90, 14)]; save(sh, "jar_shelf")
k = new(24, 24); d = ImageDraw.Draw(k); d.polygon([(12, 1), (22, 9), (18, 22), (6, 22), (2, 9)], fill=(60, 60, 80), outline=DREAM); d.ellipse([8, 9, 15, 15], fill=DREAM); save(k, "item_seal_stone8")
print("seal 8 art written to", os.path.abspath(OUT))

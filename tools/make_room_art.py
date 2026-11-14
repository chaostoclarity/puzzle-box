"""Seal 1 art: Wren's study (room 1) and the restricted stacks (room 2).
Rule: 16 texels per world unit. Run: python3 tools/make_room_art.py  (writes assets/rooms/)
Placeholder art, generated so the whole game can be built and tested before final art.
"""
import math, os, random
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "rooms")
os.makedirs(OUT, exist_ok=True)

WOOD   = [(40,22,17),(64,37,25),(86,52,32),(110,68,41),(138,90,54)]
DARKW  = [(22,14,12),(36,24,20),(52,34,28),(70,48,38),(92,64,50)]
BRASS  = [(64,40,16),(118,82,30),(172,130,48),(220,180,84),(250,228,152)]
IVORY  = [(104,92,74),(176,164,136),(232,222,196)]
VELVET = [(34,9,16),(58,15,27),(86,24,40)]
GREEN  = [(14,26,22),(22,40,33),(32,56,45),(46,74,58)]
STONE  = [(26,28,34),(38,41,50),(52,56,66),(70,75,86),(92,98,110)]
INK    = (22,12,10)
SKY    = [(8,12,26),(16,24,46),(30,44,74)]
SILVER = [(66,70,84),(116,122,138),(172,178,192),(228,232,240),(250,252,255)]
BOOKS  = [(96,30,30),(40,70,50),(40,52,92),(110,84,40),(70,40,80),(60,60,60),(120,60,30)]
RED, GRN, BLU = (150,34,34), (40,120,60), (44,70,150)
T = (0, 0, 0, 0)

def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))

def new(w, h, col=T):
    return Image.new("RGBA", (w, h), col if len(col) == 4 else col + (255,))

def grain(w, h, pal, seed, vertical=False):
    rnd = random.Random(seed)
    img = new(w, h); px = img.load()
    for y in range(h):
        for x in range(w):
            a, b = (y, x) if vertical else (x, y)
            v = math.sin((a + 2.2 * math.sin(b * 0.13 + seed) + 0.6 * math.sin(b * 0.41)) * 0.85)
            i = 1 + (v > 0.35) + (v > 0.85)
            if rnd.random() < 0.02: i = max(0, i - 1)
            px[x, y] = pal[i] + (255,)
    return img

def bevel(img, pal, band=2, box=None):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box or (0, 0, img.width - 1, img.height - 1)
    d.rectangle([x0, y0, x1, y1], outline=pal[0])
    for i in range(1, band + 1):
        d.line([x0+i, y0+i, x1-i, y0+i], fill=pal[3]); d.line([x0+i, y0+i, x0+i, y1-i], fill=pal[3])
        d.line([x0+i, y1-i, x1-i, y1-i], fill=pal[1]); d.line([x1-i, y0+i, x1-i, y1-i], fill=pal[1])

def noise_fill(img, box, pal, seed, density=0.08):
    rnd = random.Random(seed); px = img.load()
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            px[x, y] = (pal[1] if rnd.random() < density else pal[2] if rnd.random() < 0.04 else pal[0]) + (255,) \
                if len(pal) > 2 else pal[0] + (255,)

def damask(img, box, pal, seed):
    x0, y0, x1, y1 = box; px = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            u, v = (x - x0) % 16, (y - y0) % 24
            d = abs(u - 8) + abs(v - 12) * 0.66
            c = pal[1]
            if 6.5 < d < 8: c = pal[2]
            if d < 2.5: c = pal[2]
            if (x + y) % 7 == 0 and random.Random(x * 991 + y).random() < 0.3: c = pal[0]
            px[x, y] = c + (255,)

def sym_mask(sym, n=12):
    m = Image.new("L", (n, n), 0); d = ImageDraw.Draw(m); c = n / 2 - 0.5
    if sym == "sun":
        d.ellipse([3, 3, 8, 8], fill=255)
        for a in range(8):
            ang = a * math.pi / 4
            d.point((round(c + 5.4 * math.cos(ang)), round(c + 5.4 * math.sin(ang))), fill=255)
    elif sym == "eye":
        d.ellipse([0, 3, 11, 8], outline=255); d.ellipse([4, 3, 7, 8], fill=255)
    elif sym == "star":
        pts = [(c + (5.6 if k % 2 == 0 else 2.3) * math.cos(-math.pi/2 + k*math.pi/5),
                c + 0.5 + (5.6 if k % 2 == 0 else 2.3) * math.sin(-math.pi/2 + k*math.pi/5)) for k in range(10)]
        d.polygon(pts, fill=255)
    elif sym == "moon":
        d.ellipse([1, 1, 10, 10], fill=255); d.ellipse([4, 0, 12, 8], fill=0)
    return m

def stamp(img, x, y, mask, col):
    img.paste(Image.new("RGBA", mask.size, col + (255,)), (x, y), mask)

DIGITS = {"1": ["010", "110", "010", "010", "111"], "2": ["110", "001", "010", "100", "111"],
          "3": ["110", "001", "010", "001", "110"], "I": ["1", "1", "1", "1", "1"], "W": ["10001", "10001", "10101", "10101", "01010"]}
def glyph(img, x, y, ch, col, scale=1):
    d = ImageDraw.Draw(img)
    for r, row in enumerate(DIGITS[ch]):
        for c, b in enumerate(row):
            if b == "1": d.rectangle([x + c*scale, y + r*scale, x + c*scale + scale - 1, y + r*scale + scale - 1], fill=col)
    return len(DIGITS[ch][0]) * scale

def roman(img, x, y, n, col, scale=1):
    for i in range(n): glyph(img, x + i * (scale + scale), y, "I", col, scale)

def book_row(img, x0, x1, y_bottom, rnd, h_range=(22, 30), pal=BOOKS):
    d = ImageDraw.Draw(img); x = x0
    while x < x1 - 3:
        w = rnd.randint(4, 7); h = rnd.randint(*h_range)
        if x + w > x1: w = x1 - x
        c = pal[rnd.randrange(len(pal))]
        dk = tuple(max(0, v - 30) for v in c); lt = tuple(min(255, v + 35) for v in c)
        d.rectangle([x, y_bottom - h, x + w - 1, y_bottom], fill=c)
        d.line([x, y_bottom - h, x, y_bottom], fill=lt); d.line([x + w - 1, y_bottom - h, x + w - 1, y_bottom], fill=dk)
        if w > 4:
            d.line([x + 1, y_bottom - h + 3, x + w - 2, y_bottom - h + 3], fill=BRASS[2])
            d.line([x + 1, y_bottom - 4, x + w - 2, y_bottom - 4], fill=BRASS[1])
        x += w
        if rnd.random() < 0.08 and x < x1 - 10:  # leaning book
            d.polygon([(x, y_bottom), (x + 4, y_bottom), (x + 10, y_bottom - h + 4), (x + 6, y_bottom - h + 4)], fill=pal[rnd.randrange(len(pal))])
            x += 11

# ---------------- walls ----------------
W, H = 240, 352   # 15 x 22 units

def wall(seed, upper_pal, lower_pal, style):
    img = new(W, H)
    d = ImageDraw.Draw(img)
    if style == "damask":
        damask(img, (0, 32, W, H - 64), upper_pal, seed)
    else:  # plaster/stone
        rnd = random.Random(seed); px = img.load()
        for y in range(32, H - 64):
            for x in range(W):
                c = upper_pal[1]
                if (y // 12) % 2 == 0 and x % 24 == 0 or (y // 12) % 2 == 1 and (x + 12) % 24 == 0 or y % 12 == 0: c = upper_pal[0]
                elif rnd.random() < 0.05: c = upper_pal[2]
                px[x, y] = c + (255,)
    # ceiling band + crown molding
    d.rectangle([0, 0, W, 27], fill=(10, 8, 10))
    for x in range(0, W, 30): d.rectangle([x, 0, x + 9, 27], fill=DARKW[1])
    d.rectangle([0, 28, W, 31], fill=lower_pal[3]); d.line([0, 31, W, 31], fill=lower_pal[0])
    # wainscot
    wain = grain(W, 64, lower_pal, seed + 9, vertical=True)
    img.paste(wain, (0, H - 64))
    d.line([0, H - 64, W, H - 64], fill=lower_pal[4]); d.line([0, H - 63, W, H - 63], fill=lower_pal[0])
    for x in range(8, W, 46): d.rectangle([x, H - 56, x + 37, H - 10], outline=lower_pal[1])
    d.rectangle([0, H - 6, W, H], fill=lower_pal[0])
    return img

for name, seed in [("r1_wall_n", 1), ("r1_wall_e", 2), ("r1_wall_s", 3), ("r1_wall_w", 4)]:
    save(wall(seed, GREEN, WOOD, "damask"), name)
for name, seed in [("r2_wall_n", 5), ("r2_wall_e", 6), ("r2_wall_s", 7), ("r2_wall_w", 8)]:
    save(wall(seed, STONE, DARKW, "stone"), name)

# ---------------- generic furniture faces ----------------
def wood_face(w, h, seed, pal=WOOD, band=2):
    img = grain(w, h, pal, seed); bevel(img, pal, band); return img

for n, (w, h) in {"wood_side_48x56": (48, 56), "wood_top_112x48": (112, 48), "wood_side_16x64": (16, 64),
                  "wood_top_32x16": (32, 16), "wood_side_24x208": (24, 208), "wood_top_128x24": (128, 24),
                  "wood_side_32x48": (32, 48), "wood_top_48x32": (48, 32), "wood_side_32x80": (32, 80),
                  "wood_side_40x48": (40, 48), "wood_top_96x40": (96, 40), "wood_side_32x96": (32, 96),
                  "wood_top_56x32": (56, 32), "wood_top_80x32": (80, 32), "wood_side_24x256": (24, 256),
                  "wood_top_104x24": (104, 24)}.items():
    save(wood_face(w, h, w * 7 + h), n)
for n, (w, h) in {"dark_side_32x96": (32, 96), "dark_top_56x32": (56, 32)}.items():
    save(wood_face(w, h, w + h, DARKW), n)

# desk front 112x56 with drawer slot outline (drawer is a separate part at 48x16 centred, y 6..22)
desk = wood_face(112, 56, 21)
d = ImageDraw.Draw(desk)
for x0 in (8, 80):
    d.rectangle([x0, 26, x0 + 23, 50], outline=WOOD[0]); d.rectangle([x0 + 9, 36, x0 + 14, 38], fill=BRASS[2])
d.rectangle([31, 5, 80, 22], fill=WOOD[0])
save(desk, "desk_front")

drawer = wood_face(48, 16, 22)
d = ImageDraw.Draw(drawer); d.rectangle([21, 5, 26, 10], fill=BRASS[2]); d.rectangle([23, 7, 24, 9], fill=INK)
save(drawer, "drawer")
dopen = new(48, 16, INK); d = ImageDraw.Draw(dopen)
d.rectangle([0, 9, 47, 15], fill=WOOD[2]); d.line([0, 9, 47, 9], fill=WOOD[4]); bevel(dopen, WOOD, 1, (0, 9, 47, 15))
d.rectangle([2, 0, 45, 8], fill=VELVET[0])
save(dopen, "drawer_open")

# wall clock front 32x64; face centre at (16, 18), pendulum window below; base door at y 46..62
clock = wood_face(32, 64, 31, DARKW)
d = ImageDraw.Draw(clock)
d.ellipse([4, 6, 27, 29], fill=BRASS[1]); d.ellipse([6, 8, 25, 27], fill=IVORY[2])
for k in range(12):
    a = k * math.pi / 6
    d.point((round(15.5 + 8 * math.sin(a)), round(17.5 - 8 * math.cos(a))), fill=INK)
glyph(clock, 14, 9, "3", INK) if False else None
d.rectangle([9, 32, 22, 43], fill=INK); d.line([15, 33, 15, 40], fill=BRASS[2]); d.ellipse([13, 39, 18, 43], fill=BRASS[3])
save(clock, "clock_front")
hand = new(16, 16); d = ImageDraw.Draw(hand)
d.line([7, 8, 7, 2], fill=INK); d.line([8, 8, 8, 2], fill=INK); d.point((7, 1), fill=INK); d.rectangle([6, 7, 9, 9], fill=BRASS[0])
save(hand, "clock_hand")
cdoor = wood_face(20, 16, 33, DARKW); d = ImageDraw.Draw(cdoor); d.rectangle([9, 6, 10, 9], fill=BRASS[3])
save(cdoor, "clock_door")
cdo = new(20, 16, INK); bevel(cdo, DARKW, 1); save(cdo, "clock_door_open")

# lamp 24x40 unlit and lit
def lamp(lit):
    img = new(24, 40); d = ImageDraw.Draw(img)
    d.polygon([(6, 38), (17, 38), (15, 33), (8, 33)], fill=BRASS[1]); d.rectangle([10, 26, 13, 33], fill=BRASS[2])
    d.ellipse([5, 18, 18, 30], fill=BRASS[2]); d.arc([5, 18, 18, 30], 200, 300, fill=BRASS[4])
    d.ellipse([7, 4, 16, 20], fill=(255, 220, 120) if lit else (70, 80, 70), outline=(200, 210, 200))
    if lit:
        d.polygon([(11, 15), (12, 8), (13, 15)], fill=(255, 250, 200)); d.point((12, 7), fill=(255, 255, 255))
    d.rectangle([9, 1, 14, 3], fill=BRASS[0])
    return img
save(lamp(False), "lamp"); save(lamp(True), "lamp_lit")
glow = new(64, 64); px = glow.load()
for y in range(64):
    for x in range(64):
        r = math.hypot(x - 31.5, y - 31.5) / 32
        a = max(0, 1 - r)
        if a > 0: px[x, y] = (255, 200, 110, int(90 * round(a * 3) / 3))
save(glow, "glow")

letter = new(20, 16); d = ImageDraw.Draw(letter)
d.rectangle([0, 2, 19, 15], fill=IVORY[2], outline=IVORY[0]); d.line([0, 2, 10, 9], fill=IVORY[0]); d.line([19, 2, 10, 9], fill=IVORY[0])
d.ellipse([8, 7, 12, 11], fill=VELVET[2])
save(letter, "letter")

diploma = new(64, 48); d = ImageDraw.Draw(diploma)
d.rectangle([0, 0, 63, 47], fill=BRASS[1]); d.rectangle([3, 3, 60, 44], fill=IVORY[2])
for y in range(12, 38, 5): d.line([12, y, 51, y], fill=IVORY[0])
d.ellipse([28, 32, 35, 39], fill=VELVET[2])
save(diploma, "diploma")

# bookshelf front 128x208 (8 x 13 units), shelves every 40px; special books & compartment are parts
def bookshelf(seed, w=128, h=208, pal=WOOD, gap_box=None):
    img = wood_face(w, h, seed, pal, 3)
    d = ImageDraw.Draw(img); rnd = random.Random(seed)
    for sy in range(8, h - 8, 40):
        d.rectangle([5, sy, w - 6, sy + 33], fill=pal[0])
        book_row(img, 6, w - 6, sy + 33, rnd)
        d.rectangle([4, sy + 34, w - 5, sy + 39], fill=pal[3]); d.line([4, sy + 39, w - 5, sy + 39], fill=pal[0])
    if gap_box:
        for (x0, y0, x1, y1) in gap_box: d.rectangle([x0, y0, x1, y1], fill=pal[0])
    return img
# gap on shelf 3 (y 88..121) for three special books (x 44..83) and the compartment (x 92..115)
save(bookshelf(41, gap_box=[(44, 90, 84, 121), (92, 96, 116, 121)]), "bookshelf")

def special_book(col, pulled):
    img = new(8, 32); d = ImageDraw.Draw(img)
    top = 4 if pulled else 0
    lt = tuple(min(255, v + 40) for v in col); dk = tuple(max(0, v - 40) for v in col)
    d.rectangle([0, top, 7, 31], fill=col); d.line([0, top, 0, 31], fill=lt); d.line([7, top, 7, 31], fill=dk)
    d.line([1, top + 4, 6, top + 4], fill=BRASS[3]); d.line([1, 27, 6, 27], fill=BRASS[3])
    if pulled: d.rectangle([0, 0, 7, 3], fill=WOOD[0])
    return img
for nm, col in [("red", RED), ("green", GRN), ("blue", BLU)]:
    save(special_book(col, False), "book_" + nm); save(special_book(col, True), "book_" + nm + "_pulled")
comp = wood_face(24, 24, 44); d = ImageDraw.Draw(comp); d.rectangle([10, 10, 13, 13], fill=BRASS[2]); save(comp, "compartment")
compo = new(24, 24, VELVET[0]); bevel(compo, WOOD, 1); save(compo, "compartment_open")

globe = new(32, 48); d = ImageDraw.Draw(globe)
d.ellipse([3, 2, 28, 27], fill=(40, 70, 90)); d.arc([3, 2, 28, 27], 120, 250, fill=(90, 130, 140))
d.polygon([(10, 8), (16, 6), (18, 13), (12, 17)], fill=(110, 100, 60)); d.polygon([(19, 16), (24, 17), (22, 23)], fill=(110, 100, 60))
d.arc([0, 0, 31, 30], 30, 330, fill=BRASS[2]); d.rectangle([14, 29, 17, 40], fill=WOOD[2]); d.rectangle([7, 40, 24, 46], fill=WOOD[1])
save(globe, "globe")

# door 72x128 closed / open
door = wood_face(72, 128, 51, WOOD, 3); d = ImageDraw.Draw(door)
for (x0, y0, x1, y1) in [(10, 10, 61, 56), (10, 66, 61, 117)]:
    d.rectangle([x0, y0, x1, y1], outline=WOOD[0]); d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], outline=WOOD[4])
d.ellipse([58, 62, 64, 68], fill=BRASS[3]); d.rectangle([59, 71, 62, 77], fill=BRASS[1]); d.rectangle([60, 73, 61, 76], fill=INK)
save(door, "door")
dopen2 = new(72, 128, (6, 6, 10)); d = ImageDraw.Draw(dopen2)
for i in range(0, 60, 6): d.rectangle([20 + i // 6, 30 + i, 52 - i // 6, 34 + i], fill=(20 + i, 18 + i, 24 + i))
d.rectangle([0, 0, 71, 127], outline=WOOD[0]); d.rectangle([0, 0, 6, 127], fill=WOOD[2])
save(dopen2, "door_open")

coatrack = new(24, 96); d = ImageDraw.Draw(coatrack)
d.rectangle([11, 6, 12, 92], fill=DARKW[3]); d.rectangle([4, 92, 19, 95], fill=DARKW[2])
d.polygon([(6, 12), (17, 12), (20, 56), (3, 56)], fill=(40, 34, 44)); d.ellipse([7, 2, 16, 10], fill=(30, 26, 32))
save(coatrack, "coatrack")

sampler = new(48, 32); d = ImageDraw.Draw(sampler)
d.rectangle([0, 0, 47, 31], fill=DARKW[2]); d.rectangle([3, 3, 44, 28], fill=IVORY[1])
rnd = random.Random(3)
for y in range(7, 26, 4):
    for x in range(7, 41, 2):
        if rnd.random() < 0.7: d.point((x, y), fill=VELVET[2])
save(sampler, "sampler")

window = new(64, 128); d = ImageDraw.Draw(window)
d.rectangle([0, 0, 63, 127], fill=WOOD[1])
for y in range(4, 124):
    c = SKY[0] if y < 50 else SKY[1] if y < 95 else SKY[2]
    d.line([4, y, 59, y], fill=c)
rnd = random.Random(9)
for _ in range(60): d.point((rnd.randint(5, 58), rnd.randint(5, 122)), fill=(220, 225, 235))
d.ellipse([38, 14, 50, 26], fill=(230, 230, 200))
d.rectangle([30, 4, 33, 123], fill=WOOD[2]); d.rectangle([4, 62, 59, 65], fill=WOOD[2])
d.rectangle([4, 118, 59, 123], fill=(200, 210, 225))
save(window, "window")

portrait = new(64, 80); d = ImageDraw.Draw(portrait)
d.rectangle([0, 0, 63, 79], fill=BRASS[1]); d.rectangle([4, 4, 59, 75], fill=(30, 26, 22))
d.ellipse([20, 14, 43, 42], fill=(170, 140, 110)); d.rectangle([16, 44, 47, 75], fill=(26, 24, 30))
d.polygon([(26, 44), (37, 44), (31, 56)], fill=IVORY[2])
d.rectangle([24, 25, 28, 27], fill=INK); d.rectangle([35, 25, 39, 27], fill=INK); d.line([27, 35, 36, 35], fill=(110, 80, 60))
d.arc([18, 10, 45, 30], 180, 360, fill=(200, 200, 200))
save(portrait, "portrait")

# the reliquary cabinet: 56x96 black lacquer, nine seals, three cracked (Wren opened three)
cab = wood_face(56, 96, 61, [(10, 8, 12), (18, 14, 20), (26, 22, 30), (40, 34, 46), (60, 52, 66)], 2)
d = ImageDraw.Draw(cab)
for i in range(9):
    cx, cy = 12 + (i % 3) * 16, 22 + (i // 3) * 20
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=VELVET[1], outline=BRASS[1])
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=VELVET[2])
    if i < 3: d.line([cx - 5, cy - 3, cx + 1, cy + 1], fill=INK); d.line([cx + 1, cy + 1, cx + 4, cy + 5], fill=INK)
d.rectangle([4, 84, 51, 90], fill=BRASS[0])
save(cab, "cabinet_front")

# ---------------- room 2 pieces ----------------
save(bookshelf(71, 104, 256, DARKW, gap_box=[(30, 130, 70, 161), (78, 136, 98, 161)]), "stack_a")
save(bookshelf(73, 104, 256, DARKW, gap_box=[(56, 50, 64, 81)]), "stack_b")
plain = {"book_ochre": (110, 84, 40), "book_plum": (70, 40, 80), "book_slate": (60, 70, 76), "book_wren": (90, 60, 40)}
for nm, col in plain.items():
    save(special_book(col, False), nm); save(special_book(col, True), nm + "_pulled")
niche = wood_face(24, 24, 74, DARKW); d = ImageDraw.Draw(niche); d.rectangle([10, 10, 13, 13], fill=BRASS[1]); save(niche, "niche")
nio = new(24, 24, (8, 6, 8)); bevel(nio, DARKW, 1); save(nio, "niche_open")

def lens_mark(n=None, letter=None):
    img = new(12, 16); d = ImageDraw.Draw(img)
    col = (120, 255, 220)
    if n: roman(img, 6 - n, 4, n, col, 2) if n < 3 else roman(img, 1, 4, n, col, 2)
    if letter: glyph(img, 1, 4, letter, col, 2) if False else glyph(img, 1, 5, letter, col, 2)
    return img
for n in (1, 2, 3): save(lens_mark(n), "lensmark_%d" % n)
wm = new(12, 16); glyph(wm, 1, 5, "W", (120, 255, 220), 2); save(wm, "lensmark_w")

lect = wood_face(48, 80, 81, DARKW, 2); d = ImageDraw.Draw(lect)
d.rectangle([8, 10, 39, 70], outline=DARKW[0]); d.rectangle([20, 30, 27, 52], fill=DARKW[3])
save(lect, "lectern_front")
chain = new(32, 48); d = ImageDraw.Draw(chain)
for y in range(0, 48, 5):
    d.ellipse([12, y, 19, y + 6], outline=(140, 140, 150)); d.point((15, y + 3), fill=(60, 60, 70))
d.rectangle([9, 18, 22, 30], fill=(90, 90, 100), outline=(40, 40, 46)); d.arc([11, 11, 20, 22], 180, 360, fill=(160, 160, 170))
d.rectangle([14, 22, 17, 26], fill=INK)
save(chain, "chain")

arch = new(64, 112); d = ImageDraw.Draw(arch)
d.rectangle([0, 32, 63, 111], fill=STONE[2]); d.pieslice([0, 0, 63, 63], 180, 360, fill=STONE[2])
d.rectangle([4, 32, 59, 107], fill=SKY[1]); d.pieslice([4, 4, 59, 59], 180, 360, fill=SKY[1])
for y in range(6, 108, 9): d.line([4, y, 59, y], fill=STONE[1])
for x in range(4, 60, 11): d.line([x, 6, x, 107], fill=STONE[1])
d.ellipse([20, 14, 32, 26], fill=(150, 200, 190))
save(arch, "arch_window")

ldesk = wood_face(96, 48, 91, DARKW, 2); d = ImageDraw.Draw(ldesk)
d.rectangle([6, 8, 89, 20], outline=DARKW[0]); d.rectangle([44, 12, 51, 15], fill=BRASS[1])
save(ldesk, "ldesk_front")
lcase = new(24, 12); d = ImageDraw.Draw(lcase)
d.rounded_rectangle([0, 1, 23, 11], 3, fill=VELVET[1], outline=VELVET[0]); d.rectangle([10, 5, 13, 7], fill=BRASS[3])
save(lcase, "lens_case")
lco = new(24, 12); d = ImageDraw.Draw(lco); d.rounded_rectangle([0, 1, 23, 11], 3, fill=VELVET[0], outline=VELVET[0])
save(lco, "lens_case_open")

catalog = wood_face(80, 96, 95, WOOD, 2); d = ImageDraw.Draw(catalog)
for r in range(6):
    for c in range(4):
        x0, y0 = 6 + c * 18, 6 + r * 14
        d.rectangle([x0, y0, x0 + 15, y0 + 11], outline=WOOD[0]); d.rectangle([x0 + 5, y0 + 3, x0 + 10, y0 + 5], fill=IVORY[1])
        d.point((x0 + 7, y0 + 8), fill=BRASS[3])
save(catalog, "catalog_front")
sdoor = wood_face(72, 128, 97, DARKW, 3); d = ImageDraw.Draw(sdoor)
d.rectangle([12, 12, 59, 115], outline=DARKW[0]); d.ellipse([58, 62, 64, 68], fill=BRASS[1])
save(sdoor, "stacks_door")

# ---------------- hero box 2: the book-box (6w x 7h x 3d) ----------------
def bookbox_cover():
    img = new(96, 112); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 95, 111], fill=(52, 20, 22)); bevel(img, [(24, 8, 10), (40, 14, 16), (52, 20, 22), (90, 40, 40), (120, 60, 56)], 3)
    d.rectangle([8, 8, 87, 103], outline=BRASS[1]); d.rectangle([10, 10, 85, 101], outline=BRASS[0])
    for (cx, cy) in [(12, 12), (83, 12), (12, 99), (83, 99)]: d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=BRASS[2])
    return img
save(bookbox_cover(), "bookbox_front")
bb = new(96, 112, (44, 18, 20)); bevel(bb, [(24, 8, 10), (40, 14, 16), (52, 20, 22), (90, 40, 40), (120, 60, 56)], 3); save(bb, "bookbox_back")
spine = new(48, 112, (40, 14, 16)); d = ImageDraw.Draw(spine)
for y in (14, 30, 82, 98): d.rectangle([2, y, 45, y + 3], fill=BRASS[1])
save(spine, "bookbox_left")
pages = new(48, 112, IVORY[2]); d = ImageDraw.Draw(pages)
for x in range(0, 48, 2): d.line([x, 0, x, 111], fill=IVORY[1])
d.rectangle([0, 0, 47, 111], outline=(40, 14, 16))
save(pages, "bookbox_right")
ptop = new(96, 48, IVORY[2]); d = ImageDraw.Draw(ptop)
for y in range(0, 48, 2): d.line([0, y, 95, y], fill=IVORY[1])
d.rectangle([0, 0, 95, 47], outline=(40, 14, 16))
save(ptop, "bookbox_top")
paper = new(96, 112, IVORY[1]); d = ImageDraw.Draw(paper)
for y in range(8, 104, 6): d.line([10, y, 85, y], fill=IVORY[0])
save(paper, "bookbox_liner")

def ring(size, inner, notch_col, seed):
    img = new(size, size); d = ImageDraw.Draw(img)
    d.ellipse([0, 0, size - 1, size - 1], fill=BRASS[1]); d.ellipse([1, 1, size - 2, size - 2], fill=BRASS[2])
    d.arc([1, 1, size - 2, size - 2], 200, 290, fill=BRASS[4])
    d.ellipse([inner, inner, size - 1 - inner, size - 1 - inner], fill=(0, 0, 0, 0))
    d.ellipse([inner - 1, inner - 1, size - inner, size - inner], outline=BRASS[0])
    c = size // 2
    d.rectangle([c - 1, 1, c, inner - 1], fill=notch_col)  # notch at the top
    rnd = random.Random(seed)
    for k in range(10):
        a = k * math.pi / 5 + 0.3
        r = (size / 2 + inner / 2) / 2
        d.point((round(c - 0.5 + r * math.cos(a) * 0.98), round(c - 0.5 + r * math.sin(a) * 0.98)), fill=BRASS[0])
    return img
save(ring(64, 11, INK, 1), "ring_outer"); save(ring(44, 11, INK, 2), "ring_mid")
core = new(24, 24); d = ImageDraw.Draw(core); d.ellipse([0, 0, 23, 23], fill=BRASS[3]); d.ellipse([2, 2, 21, 21], fill=BRASS[2])
d.rectangle([11, 1, 12, 10], fill=INK); save(core, "ring_core")
ghost = new(72, 72); d = ImageDraw.Draw(ghost); gc = (120, 255, 220)
# target notches: outer -> right, middle -> down, core -> left
d.rectangle([68, 35, 71, 36], fill=gc); d.rectangle([35, 58, 36, 61], fill=gc); d.rectangle([26, 35, 29, 36], fill=gc)
d.arc([2, 2, 69, 69], 0, 360, fill=(60, 140, 120))
save(ghost, "ring_ghost")
clasp = new(12, 24); d = ImageDraw.Draw(clasp); d.rectangle([0, 0, 11, 23], fill=BRASS[1]); d.rectangle([2, 2, 9, 21], fill=BRASS[2]); d.rectangle([4, 10, 7, 13], fill=INK)
save(clasp, "clasp")
co = new(12, 24); d = ImageDraw.Draw(co); d.rectangle([0, 0, 11, 5], fill=BRASS[1]); d.rectangle([0, 18, 11, 23], fill=BRASS[1]); save(co, "clasp_open")

# ---------------- reliquary (nested in the book) ----------------
def bone_face(seed, plate=False):
    pal = [(60, 54, 44), (120, 110, 92), (176, 164, 136), (210, 200, 172), (236, 228, 204)]
    img = grain(96, 96, pal, seed); bevel(img, pal, 4)
    d = ImageDraw.Draw(img)
    for (cx, cy) in [(6, 6), (89, 6), (6, 89), (89, 89)]: d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=SILVER[2], outline=SILVER[0])
    return img
for nm, s in [("front", 1), ("back", 2), ("left", 3), ("right", 4), ("top", 5), ("bottom", 6)]:
    save(bone_face(100 + s), "reliq_" + nm)
plate = new(64, 20); d = ImageDraw.Draw(plate); d.rectangle([0, 0, 63, 19], fill=SILVER[1], outline=SILVER[0]); d.line([1, 1, 62, 1], fill=SILVER[3])
save(plate, "reliq_plate")
pname = new(64, 20); d = ImageDraw.Draw(pname)
# "THORNE" in a 3x5 pixel font, lens colour
F = {"T": ["111", "010", "010", "010", "010"], "H": ["101", "101", "111", "101", "101"], "O": ["111", "101", "101", "101", "111"],
     "R": ["110", "101", "110", "101", "101"], "N": ["101", "111", "111", "111", "101"], "E": ["111", "100", "110", "100", "111"],
     "L": ["100", "100", "100", "100", "111"], "I": ["111", "010", "010", "010", "111"], "A": ["010", "101", "111", "101", "101"],
     "S": ["111", "100", "111", "001", "111"]}
def word(img, x, y, txt, col, s=1):
    d = ImageDraw.Draw(img)
    for ch in txt:
        if ch == " ": x += 3 * s; continue
        for r, row in enumerate(F[ch]):
            for c, b in enumerate(row):
                if b == "1": d.rectangle([x + c * s, y + r * s, x + c * s + s - 1, y + r * s + s - 1], fill=col)
        x += 4 * s
word(pname, 4, 2, "ELIAS", (120, 255, 220)); word(pname, 4, 11, "THORNE", (120, 255, 220))
save(pname, "reliq_name")
btn = new(12, 12); d = ImageDraw.Draw(btn); d.ellipse([0, 0, 11, 11], fill=(40, 120, 110)); d.ellipse([3, 3, 8, 8], fill=(120, 255, 220)); save(btn, "phantom_button")
bliner = new(96, 96, (20, 14, 18)); d = ImageDraw.Draw(bliner)
for i in range(0, 96, 8): d.line([0, i, 95, i], fill=(30, 20, 26))
save(bliner, "reliq_liner")

# ---------------- walnut inner box extras ----------------
wax = new(24, 24); d = ImageDraw.Draw(wax)
d.ellipse([1, 1, 22, 22], fill=(140, 20, 24)); d.ellipse([3, 3, 20, 20], fill=(170, 30, 34)); glyph(wax, 7, 9, "W", (100, 10, 14), 2) if False else glyph(wax, 7, 9, "W", (100, 10, 14))
save(wax, "wax_seal")
waxb = new(24, 24); d = ImageDraw.Draw(waxb)
d.pieslice([1, 1, 22, 22], 200, 330, fill=(140, 20, 24)); d.pieslice([1, 1, 22, 22], 20, 120, fill=(140, 20, 24))
save(waxb, "wax_broken")

# ---------------- items: 24x24 tray icons ----------------
def icon():
    return new(24, 24)
it = {}
k = icon(); d = ImageDraw.Draw(k)
d.ellipse([2, 7, 11, 16], fill=BRASS[2], outline=BRASS[0]); d.ellipse([5, 10, 8, 13], fill=T)
d.rectangle([11, 11, 21, 12], fill=BRASS[2]); d.rectangle([17, 13, 18, 16], fill=BRASS[1]); d.rectangle([20, 13, 21, 15], fill=BRASS[1])
it["brass_key"] = k
k = icon(); d = ImageDraw.Draw(k)
d.rectangle([2, 8, 9, 15], fill=(80, 80, 88), outline=(40, 40, 46)); d.rectangle([4, 10, 7, 13], fill=T)
d.rectangle([9, 11, 21, 12], fill=(90, 90, 100)); d.rectangle([16, 13, 21, 16], fill=(70, 70, 80)); d.rectangle([18, 13, 19, 14], fill=T)
it["iron_key"] = k
k = icon(); d = ImageDraw.Draw(k)
d.rectangle([3, 7, 20, 16], fill=(180, 60, 40), outline=(90, 30, 20)); d.rectangle([5, 9, 18, 14], fill=IVORY[2])
for x in (7, 11, 15): d.line([x, 10, x, 13], fill=(140, 40, 30))
it["matches"] = k
k = icon(); d = ImageDraw.Draw(k)
d.rectangle([2, 4, 21, 19], fill=IVORY[2]); d.rectangle([4, 6, 19, 17], fill=(60, 54, 46))
for x, c in [(7, GRN), (11, BLU), (15, RED)]: d.rectangle([x, 9, x + 2, 15], fill=c)
it["photo"] = k
k = icon(); d = ImageDraw.Draw(k)
d.ellipse([5, 7, 18, 20], outline=BRASS[2], width=2); d.rectangle([8, 2, 15, 8], fill=VELVET[2], outline=BRASS[1])
glyph(k, 10, 3, "W", BRASS[3]) if False else None
it["ring"] = k
k = icon(); d = ImageDraw.Draw(k)
d.ellipse([1, 6, 12, 17], fill=(40, 34, 30), outline=BRASS[1]); d.ellipse([4, 9, 9, 14], fill=T)
d.rectangle([12, 11, 22, 12], fill=(60, 50, 44)); d.rectangle([18, 13, 22, 17], fill=(60, 50, 44)); d.rectangle([19, 14, 20, 15], fill=T)
it["door_key"] = k
k = icon(); d = ImageDraw.Draw(k)
d.ellipse([3, 3, 18, 18], fill=(60, 120, 110), outline=BRASS[2], width=2); d.ellipse([7, 6, 11, 10], fill=(180, 255, 230))
d.line([16, 16, 21, 21], fill=BRASS[1], width=2)
it["lens"] = k
k = icon(); d = ImageDraw.Draw(k)
d.rectangle([3, 9, 8, 14], fill=(140, 140, 150)); d.rectangle([8, 11, 20, 12], fill=(140, 140, 150)); d.rectangle([17, 13, 20, 15], fill=(110, 110, 120))
it["chain_key"] = k
k = icon(); d = ImageDraw.Draw(k)
d.polygon([(12, 1), (21, 8), (18, 21), (6, 21), (3, 8)], fill=(40, 34, 48), outline=(90, 200, 180))
stamp(k, 6, 7, sym_mask("eye"), (120, 255, 220))
it["seal_stone"] = k
for n, img in it.items(): save(img, "item_" + n)

# examine views 96x72
ph = new(96, 72, IVORY[2]); d = ImageDraw.Draw(ph)
d.rectangle([4, 4, 91, 67], fill=(70, 62, 52))
for x in range(8, 88, 5): d.rectangle([x, 26, x + 3, 50], fill=(100, 90, 76))
d.rectangle([6, 50, 89, 53], fill=(120, 108, 90))
order = [(30, GRN, "1"), (44, BLU, "2"), (58, RED, "3")]
for x, c, n in order:
    d.rectangle([x, 22, x + 5, 50], fill=c)
    glyph(ph, x + 1, 12, n, (250, 245, 230))
d.ellipse([68, 10, 84, 30], fill=(150, 130, 110)); d.rectangle([66, 30, 86, 50], fill=(40, 36, 40))
save(ph, "examine_photo")
print("room art written to", os.path.abspath(OUT))

# ---------------- small in-world sprites (drawn at 1:1 so they stay crisp) ----------------
sm = new(12, 8); d = ImageDraw.Draw(sm)
d.rectangle([1, 1, 10, 6], fill=(180, 60, 40), outline=(90, 30, 20)); d.rectangle([3, 2, 8, 5], fill=IVORY[2])
save(sm, "drawer_matches")
sp = new(12, 8); d = ImageDraw.Draw(sp)
d.rectangle([0, 0, 11, 7], fill=IVORY[2]); d.rectangle([1, 1, 10, 6], fill=(60, 54, 46))
for x, c in [(3, GRN), (5, BLU), (7, RED)]: d.rectangle([x, 2, x, 5], fill=c)
save(sp, "drawer_photo")
sk = new(12, 8); d = ImageDraw.Draw(sk)
d.ellipse([0, 1, 5, 6], fill=BRASS[2], outline=BRASS[0]); d.point((2, 3), fill=T); d.point((3, 4), fill=T)
d.rectangle([5, 3, 11, 4], fill=BRASS[3]); d.rectangle([9, 5, 10, 6], fill=BRASS[1])
save(sk, "small_brass_key")
sr = new(12, 12); d = ImageDraw.Draw(sr)
d.ellipse([2, 4, 9, 11], outline=BRASS[2]); d.ellipse([3, 5, 8, 10], outline=BRASS[1]); d.rectangle([4, 1, 7, 4], fill=VELVET[2], outline=BRASS[1])
save(sr, "small_ring")
print("small sprites done")

save(new(16, 16), "clear")

# ---------------- the globe, four quarter-turns (milestone 2 gate puzzle) ----------------
def globe_view(turn, open_drawer=False):
    img = new(32, 48); d = ImageDraw.Draw(img)
    d.ellipse([3, 2, 28, 27], fill=(40, 70, 90))
    rnd = random.Random(turn)
    lands = [[(9, 8), (15, 6), (17, 13), (11, 17)], [(18, 16), (23, 17), (21, 23)], [(6, 18), (10, 16), (12, 22)]]
    for poly in lands:
        pts = [(4 + ((x - 4 + turn * 6) % 24), y) for x, y in poly]
        if max(p[0] for p in pts) - min(p[0] for p in pts) < 12:
            d.polygon(pts, fill=(110, 100, 60))
    if turn == 2:
        d.line([14, 18, 18, 22], fill=(200, 40, 40)); d.line([18, 18, 14, 22], fill=(200, 40, 40))
    d.arc([3, 2, 28, 27], 120, 250, fill=(90, 130, 140))
    d.arc([0, 0, 31, 30], 30, 330, fill=BRASS[2]); d.rectangle([14, 29, 17, 37], fill=WOOD[2])
    d.rectangle([6, 37, 25, 46], fill=WOOD[1]); d.rectangle([12, 40, 19, 43], outline=WOOD[0]); d.point((15, 41), fill=BRASS[3])
    if open_drawer:
        d.rectangle([11, 39, 20, 44], fill=INK); d.rectangle([12, 40, 19, 42], fill=IVORY[2])
    return img
for t in range(4):
    save(globe_view(t), "globe_%d" % t)
save(globe_view(2, True), "globe_open")
print("globe views done")

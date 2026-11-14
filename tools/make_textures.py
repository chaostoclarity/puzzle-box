"""Generates every pixel art texture for the prototype.
Rule: 16 texels per world unit. A 6-unit box face is 96x96.
Run: python3 tools/make_textures.py  (writes into assets/)
"""
import math, os, random
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

WOOD   = [(40,22,17),(64,37,25),(86,52,32),(110,68,41),(138,90,54)]
BRASS  = [(64,40,16),(118,82,30),(172,130,48),(220,180,84),(250,228,152)]
IVORY  = [(104,92,74),(176,164,136),(232,222,196)]
VELVET = [(34,9,16),(58,15,27),(86,24,40)]
EBONY  = [(16,14,20),(28,25,34),(42,38,50),(60,56,70)]
SILVER = [(66,70,84),(116,122,138),(172,178,192),(228,232,240),(250,252,255)]
INK    = (22,12,10)

def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))

def grain(w, h, pal, seed):
    rnd = random.Random(seed)
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            v = math.sin((x + 2.2 * math.sin(y * 0.13 + seed) + 0.6 * math.sin(y * 0.41)) * 0.85)
            i = 1 + (v > 0.35) + (v > 0.85)
            if rnd.random() < 0.025:
                i = max(0, i - 1)
            px[x, y] = pal[i] + (255,)
    return img

def bevel_frame(img, pal, band=4, caps=None):
    w, h = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w-1, h-1], outline=pal[0])
    for i in range(1, band+1):
        d.line([i, i, w-1-i, i], fill=pal[3] if i < band else pal[4])
        d.line([i, i, i, h-1-i], fill=pal[3] if i < band else pal[4])
        d.line([i, h-1-i, w-1-i, h-1-i], fill=pal[1])
        d.line([w-1-i, i, w-1-i, h-1-i], fill=pal[1])
    d.rectangle([band+1, band+1, w-2-band, h-2-band], outline=pal[0])
    if caps:
        for cx, cy in [(0,0),(w-7,0),(0,h-7),(w-7,h-7)]:
            d.rectangle([cx, cy, cx+6, cy+6], fill=caps[2], outline=caps[0])
            d.line([cx+1, cy+1, cx+5, cy+1], fill=caps[3])
            d.point((cx+3, cy+3), fill=caps[4])

def sym_mask(sym, n=12):
    m = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(m)
    c = n / 2 - 0.5
    if sym == "sun":
        d.ellipse([3, 3, 8, 8], fill=255)
        for a in range(8):
            ang = a * math.pi / 4
            d.point((round(c + 5.4 * math.cos(ang)), round(c + 5.4 * math.sin(ang))), fill=255)
    elif sym == "moon":
        d.ellipse([1, 1, 10, 10], fill=255)
        d.ellipse([4, 0, 12, 8], fill=0)
    elif sym == "star":
        pts = []
        for k in range(10):
            r = 5.6 if k % 2 == 0 else 2.3
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((c + r * math.cos(a), c + 0.5 + r * math.sin(a)))
        d.polygon(pts, fill=255)
    elif sym == "eye":
        d.ellipse([0, 3, 11, 8], outline=255)
        d.ellipse([4, 3, 7, 8], fill=255)
    return m

def engrave(img, x, y, sym, col, shadow, n=12):
    m = sym_mask(sym, n)
    img.paste(Image.new("RGBA", m.size, shadow + (255,)), (x+1, y+1), m)
    img.paste(Image.new("RGBA", m.size, col + (255,)), (x, y), m)

def wood_face(seed, pal=WOOD, caps=BRASS):
    img = grain(96, 96, pal, seed)
    bevel_frame(img, pal, 4, caps)
    return img

SYMS = ["sun", "moon", "star", "eye"]
RING = {10: "star", 1: "moon", 4: "eye", 7: "sun"}  # read from 10 o'clock clockwise: star, moon, eye, sun

# ---- outer box faces ----
front = wood_face(1)
d = ImageDraw.Draw(front)
d.rectangle([14, 14, 81, 81], outline=WOOD[1])
d.rectangle([15, 15, 82, 82], outline=WOOD[4])
engrave(front, 42, 22, "eye", BRASS[3], WOOD[0])
save(front, "outer_front")

back = wood_face(2)
d = ImageDraw.Draw(back)
# A brass ring like a clock face, twelve ticks, four symbols at 10, 1, 4 and 7 o'clock.
# The sampler says to read it from "our hour" (10, from Wren's watch) as the hands go.
d.ellipse([18, 18, 77, 77], fill=IVORY[1], outline=INK)
d.ellipse([22, 22, 73, 73], outline=IVORY[0])
for k in range(12):
    a_ = k * math.pi / 6
    d.point((round(47.5 + 27 * math.sin(a_)), round(47.5 - 27 * math.cos(a_))), fill=INK)
for hour, sym in RING.items():
    a_ = hour * math.pi / 6
    engrave(back, round(47.5 + 17 * math.sin(a_)) - 6, round(47.5 - 17 * math.cos(a_)) - 6, sym, INK, IVORY[0])
d.ellipse([45, 45, 50, 50], fill=BRASS[1])
save(back, "outer_back")

left = wood_face(3)
d = ImageDraw.Draw(left)
for cx in (16, 37, 59, 80):   # four dial sockets, uv x -2.0, -0.7, 0.7, 2.0
    d.ellipse([cx-11, 37, cx+11, 59], fill=WOOD[0])
    d.ellipse([cx-10, 38, cx+10, 58], fill=INK)
d.rectangle([39, 70, 56, 81], fill=WOOD[0])   # catch socket at uv (0, -1.75)
save(left, "outer_left")

right = wood_face(4)
d = ImageDraw.Draw(right)
d.rectangle([31, 39, 64, 72], fill=INK)
d.rectangle([32, 40, 63, 71], fill=VELVET[0])
d.line([32, 40, 63, 40], fill=INK); d.line([32, 41, 63, 41], fill=INK)
for y in (20, 24, 28):
    d.line([42, y, 53, y], fill=WOOD[1])
save(right, "outer_right")

top = wood_face(5)
d = ImageDraw.Draw(top)
d.polygon([(48, 18), (78, 48), (48, 78), (18, 48)], outline=BRASS[2])
d.polygon([(48, 22), (74, 48), (48, 74), (22, 48)], outline=BRASS[1])
engrave(top, 42, 42, "sun", BRASS[3], BRASS[0])
save(top, "outer_top")

bottom = wood_face(6)
d = ImageDraw.Draw(bottom)
d.ellipse([40, 40, 55, 55], outline=BRASS[1])
engrave(bottom, 42, 42, "star", BRASS[2], WOOD[0])
save(bottom, "outer_bottom")

# ---- liner (inside of the outer box) ----
liner = Image.new("RGBA", (96, 96), VELVET[1] + (255,))
px = liner.load()
for y in range(96):
    for x in range(96):
        if (x + y) % 12 == 0 or (x - y) % 12 == 0:
            px[x, y] = VELVET[0] + (255,)
        elif (x + y) % 12 == 1:
            px[x, y] = VELVET[2] + (255,)
save(liner, "liner")

# ---- parts ----
panel = grain(32, 32, WOOD, 9)
bevel_frame(panel, WOOD, 2)
d = ImageDraw.Draw(panel)
for y in (11, 16, 21):
    d.line([8, y, 23, y], fill=WOOD[0]); d.line([8, y+1, 23, y+1], fill=WOOD[4])
save(panel, "panel")

key = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(key)
d.ellipse([2, 10, 14, 22], fill=BRASS[0])
d.ellipse([3, 11, 13, 21], fill=BRASS[2])
d.ellipse([6, 14, 10, 18], fill=(0, 0, 0, 0))
d.rectangle([13, 14, 29, 18], fill=BRASS[0])
d.rectangle([13, 15, 29, 16], fill=BRASS[3])
d.rectangle([13, 17, 29, 17], fill=BRASS[1])
for x0 in (22, 26):
    d.rectangle([x0, 18, x0+2, 22], fill=BRASS[0]); d.rectangle([x0, 18, x0+1, 21], fill=BRASS[2])
d.point((5, 13), fill=BRASS[4]); d.point((4, 14), fill=BRASS[4])
save(key, "key")

def lock(open_):
    img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(7,0),(16,0),(23,7),(23,16),(16,23),(7,23),(0,16),(0,7)], fill=BRASS[0])
    d.polygon([(7,1),(16,1),(22,7),(22,16),(16,22),(7,22),(1,16),(1,7)], fill=BRASS[2])
    d.line([7, 1, 16, 1], fill=BRASS[4]); d.line([1, 7, 7, 1], fill=BRASS[3])
    for p in ((4, 11), (19, 11)):
        d.point(p, fill=BRASS[0])
    if not open_:
        d.ellipse([9, 6, 14, 11], fill=INK)
        d.polygon([(10, 10), (13, 10), (14, 17), (9, 17)], fill=INK)
    else:
        d.ellipse([9, 9, 14, 14], fill=INK)
        d.polygon([(13, 10), (13, 13), (18, 14), (18, 9)], fill=INK)
        d.rectangle([5, 10, 10, 13], fill=BRASS[1])
    return img
save(lock(False), "lock")
save(lock(True), "lock_open")

for i, s in enumerate(SYMS):
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, 19, 19], fill=BRASS[0])
    d.ellipse([1, 1, 18, 18], fill=BRASS[2])
    d.ellipse([3, 3, 16, 16], fill=BRASS[1])
    d.arc([1, 1, 18, 18], 200, 290, fill=BRASS[4])
    d.rectangle([9, 0, 10, 2], fill=INK)
    engrave(img, 4, 4, s, IVORY[2], BRASS[0])
    save(img, "dial_" + s)

# ---- inner box (the next box down) ----
def ebony_face(seed, emblem=None):
    img = grain(96, 96, [EBONY[0], EBONY[1], EBONY[2], EBONY[3], SILVER[0]], seed)
    bevel_frame(img, [EBONY[0], EBONY[1], EBONY[2], SILVER[1], SILVER[2]], 4, SILVER)
    if emblem:
        d = ImageDraw.Draw(img)
        d.ellipse([30, 30, 65, 65], outline=SILVER[2])
        d.ellipse([33, 33, 62, 62], outline=SILVER[0])
        m = sym_mask(emblem).resize((24, 24), Image.NEAREST)
        img.paste(Image.new("RGBA", m.size, SILVER[0] + (255,)), (37, 37), m)
        img.paste(Image.new("RGBA", m.size, SILVER[3] + (255,)), (36, 36), m)
    return img

for name, seed, emblem in [("front", 11, "eye"), ("back", 12, None), ("left", 13, "moon"),
                           ("right", 14, "sun"), ("top", 15, "star"), ("bottom", 16, None)]:
    save(ebony_face(seed, emblem), "inner_" + name)

print("textures written to", os.path.abspath(OUT))

catch = Image.new("RGBA", (16, 12), (0, 0, 0, 0)); d = ImageDraw.Draw(catch)
d.rectangle([0, 0, 15, 11], fill=BRASS[0]); d.rectangle([1, 1, 14, 10], fill=BRASS[2]); d.rectangle([5, 4, 10, 7], fill=BRASS[3]); d.line([1, 1, 14, 1], fill=BRASS[4])
save(catch, "catch")

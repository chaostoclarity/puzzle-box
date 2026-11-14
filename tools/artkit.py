"""Shared pixel-art helpers and palettes for the art scripts. 16 texels per world unit."""
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


# 3x5 pixel font, capitals and digits
FONT = {
 "A":["010","101","111","101","101"],"B":["110","101","110","101","110"],"C":["011","100","100","100","011"],
 "D":["110","101","101","101","110"],"E":["111","100","110","100","111"],"F":["111","100","110","100","100"],
 "G":["011","100","101","101","011"],"H":["101","101","111","101","101"],"I":["111","010","010","010","111"],
 "J":["001","001","001","101","010"],"K":["101","101","110","101","101"],"L":["100","100","100","100","111"],
 "M":["101","111","111","101","101"],"N":["101","111","111","111","101"],"O":["111","101","101","101","111"],
 "P":["110","101","110","100","100"],"Q":["010","101","101","110","011"],"R":["110","101","110","101","101"],
 "S":["111","100","111","001","111"],"T":["111","010","010","010","010"],"U":["101","101","101","101","111"],
 "V":["101","101","101","101","010"],"W":["101","101","111","111","101"],"X":["101","101","010","101","101"],
 "Y":["101","101","010","010","010"],"Z":["111","001","010","100","111"],".":["000","000","000","000","010"],
 "0":["111","101","101","101","111"],"1":["010","110","010","010","111"],"2":["110","001","010","100","111"],
 "3":["110","001","010","001","110"],"4":["101","101","111","001","001"],"5":["111","100","110","001","110"],
 "6":["011","100","111","101","111"],"7":["111","001","010","010","010"],"8":["111","101","111","101","111"],
 "9":["111","101","111","001","110"],"-":["000","000","111","000","000"],"'":["010","010","000","000","000"],
}
def text(img, x, y, txt, col, s=1):
    d = ImageDraw.Draw(img)
    for ch in txt:
        if ch == " ": x += 3 * s; continue
        for r, row in enumerate(FONT[ch]):
            for c, b in enumerate(row):
                if b == "1": d.rectangle([x + c * s, y + r * s, x + c * s + s - 1, y + r * s + s - 1], fill=col)
        x += 4 * s
    return x

def text_w(txt, s=1):
    return sum(3 * s if ch == " " else 4 * s for ch in txt) - s

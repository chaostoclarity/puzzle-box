"""Art pipeline: keep every texture on the game's palette and pixel grid.

  python3 tools/art_lint.py check                 # report any texture off palette or off grid
  python3 tools/art_lint.py snap in.png out.png W H  # resize to WxH texels (nearest), snap to palette
  python3 tools/art_lint.py palette               # rebuild assets/palette.png from the reference set

Rules (see CLAUDE.md): 16 texels per world unit; sizes in quarter units (multiples of 4 texels);
alpha is either fully on or fully off (except glow*); every opaque pixel is a palette color.
The palette is locked from the reference art. When final art arrives, point REFERENCE at it and rebuild.
"""
import glob, os, sys, warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
PALETTE = os.path.join(ROOT, "assets", "palette.png")
REFERENCE = [os.path.join(ROOT, "assets", "rooms", "*.png"), os.path.join(ROOT, "assets", "*.png")]
EXEMPT = ("glow", "palette", "examine_", "icon", "seg_")   # seg_: beam segments sized to half a cell


def load_palette():
    img = Image.open(PALETTE).convert("RGB")
    return sorted(set(img.getdata()))


def build_palette():
    cols = set()
    for pat in REFERENCE:
        for f in glob.glob(pat):
            if os.path.basename(f).startswith(EXEMPT):
                continue
            for r, g, b, a in Image.open(f).convert("RGBA").getdata():
                if a >= 128:
                    cols.add((r, g, b))
    cols = sorted(cols)
    w = 16
    h = (len(cols) + w - 1) // w
    img = Image.new("RGB", (w, h), cols[0])
    for i, c in enumerate(cols):
        img.putpixel((i % w, i // w), c)
    img.save(PALETTE)
    print("palette: %d colors -> %s" % (len(cols), PALETTE))


def nearest(c, pal):
    return min(pal, key=lambda p: (p[0] - c[0]) ** 2 * 3 + (p[1] - c[1]) ** 2 * 4 + (p[2] - c[2]) ** 2 * 2)


def snap(src, dst, w, h):
    pal = load_palette()
    img = Image.open(src).convert("RGBA").resize((w, h), Image.NEAREST)
    out = Image.new("RGBA", (w, h))
    cache = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = img.getpixel((x, y))
            if a < 128:
                out.putpixel((x, y), (0, 0, 0, 0))
                continue
            k = (r, g, b)
            if k not in cache:
                cache[k] = nearest(k, pal)
            out.putpixel((x, y), cache[k] + (255,))
    out.save(dst)
    print("snapped %s -> %s (%dx%d, %d palette colors)" % (src, dst, w, h, len(pal)))


def check():
    pal = set(load_palette())
    bad = 0
    files = sorted(f for pat in REFERENCE for f in glob.glob(pat))
    for f in files:
        name = os.path.basename(f)
        if name.startswith(EXEMPT):
            continue
        img = Image.open(f).convert("RGBA")
        problems = []
        if img.width % 4 or img.height % 4:
            problems.append("size %dx%d is not in quarter units (multiples of 4 texels)" % img.size)
        off = soft = 0
        for r, g, b, a in img.getdata():
            if 0 < a < 255:
                soft += 1
            if a >= 128 and (r, g, b) not in pal:
                off += 1
        if off:
            problems.append("%d pixels off palette" % off)
        if soft:
            problems.append("%d half-transparent pixels" % soft)
        if problems:
            bad += 1
            print("%s: %s" % (name, "; ".join(problems)))
    print("art check: %d files, %d with problems" % (len(files), bad))
    return bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "palette":
        build_palette()
    elif cmd == "snap":
        snap(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    else:
        sys.exit(1 if check() else 0)

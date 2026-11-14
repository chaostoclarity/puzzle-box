import json
def J(path, room):
    json.dump(room, open(path, "w"), indent=1, ensure_ascii=False)
def say(t, secs=None):
    a = {"say": t}
    if secs: a["secs"] = secs
    return a
def bind(target, when, then, els=None, **kw):
    b = {"target": target, "when": when, "then": then}
    if els is not None: b["else"] = els
    b.update(kw); return b
def vis(target, when):
    return bind(target, when, {"visible": True, "tappable": True}, {"visible": False, "tappable": False})
def tex(target, when, a, b):
    return bind(target, when, {"texture": a}, {"texture": b})
def tap(id_, do, when=None, **kw):
    it = {"on": "tap", "id": id_, "do": do}
    if when is not None: it["when"] = when
    it.update(kw); return it
def taps(ids, do, when=None):
    it = {"on": "tap", "ids": ids, "do": do}
    if when is not None: it["when"] = when
    return it
def use(item, id_, do, when=None):
    it = {"on": "use", "item": item, "id": id_, "do": do}
    if when is not None: it["when"] = when
    return it
def uses(item, ids, do, when=None):
    it = {"on": "use", "item": item, "ids": ids, "do": do}
    if when is not None: it["when"] = when
    return it
def step(id_, done, hints, solve, said):
    return {"id": id_, "done": done, "hints": hints, "solve": solve, "said": said}
def part(face, uv, size, tex_, id_, **kw):
    p = {"face": face, "uv": uv, "size": size, "tex": tex_, "id": id_}; p.update(kw); return p
def sprite(wall, id_, center, size, tex_, **kw):
    s = {"type": "sprite", "wall": wall, "id": id_, "center": center, "size": size, "tex": tex_}; s.update(kw); return s
def journal(k, t, x): return {"journal": [k, t, x]}

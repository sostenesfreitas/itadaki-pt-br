# python -I tools/check.py NNN [NNN...] : validates pt/NNN.json against batches/NNN.json and units.json.
# Fails on missing/extra ids, changed <tags>, different number of line breaks / NULs, field overflow,
# or a line more than 15% longer than the longest English line (multi-line strings only).
import json, re, sys, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
TAG = re.compile(r"<[^<>]*>")
units = json.load(open(os.path.join(ROOT, "units.json"), encoding="utf-8"))


def check(n):
    en = {k: v for g in json.load(open(os.path.join(ROOT, "batches", f"{n}.json"), encoding="utf-8")).values() for k, v in g.items()}
    pt = json.load(open(os.path.join(ROOT, "pt", f"{n}.json"), encoding="utf-8"))
    bad = [f"missing {k}" for k in en if k not in pt] + [f"extra {k}" for k in pt if k not in en]
    for k, s in en.items():
        t = pt.get(k)
        if t is None: continue
        if not isinstance(t, str) or not t.strip(): bad.append(f"empty {k}"); continue
        if sorted(TAG.findall(s)) != sorted(TAG.findall(t)): bad.append(f"tags {k}: {TAG.findall(s)} vs {TAG.findall(t)}")
        if TAG.match(s) and not t.startswith(TAG.match(s).group()): bad.append(f"leading tag moved {k}")
        for c, name in (("\n", "line breaks"), ("\0", "NULs")):
            if s.count(c) != t.count(c): bad.append(f"{name} {k}: {s.count(c)} vs {t.count(c)}")
        cap = units[k]["cap"]
        if len(t) > cap: bad.append(f"too long {k}: {len(t)} > {cap} chars (field limit)")
        if "\n" in s:
            lim = int(max(len(TAG.sub("", l)) for l in s.split("\n")) * 1.15) + 1
            for l in t.split("\n"):
                if len(TAG.sub("", l)) > lim: bad.append(f"line too long {k}: {len(TAG.sub('', l))} > {lim}: {l!r}")
    for b in bad[:40]: print(b)
    print(f"{n}: {len(en)} ids, {len(bad)} problems")
    return not bad


ok = all([check(n) for n in sys.argv[1:]])
sys.exit(0 if ok else 1)

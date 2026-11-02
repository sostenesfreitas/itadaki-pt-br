# python -I tools/build.py [--no-accents] : writes out/base and out/dlc (same layout as the EN patch) with pt/*.json applied.
# Untranslated units keep the English text. --no-accents strips diacritics (if the game font lacks them).
import json, os, sys, glob, shutil, unicodedata, collections
sys.path.insert(0, os.path.dirname(__file__))
import itd

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "out")
NOACC = "--no-accents" in sys.argv

pt = {}
for f in sorted(glob.glob(os.path.join(ROOT, "pt", "*.json"))): pt.update(json.load(open(f, encoding="utf-8")))
units = json.load(open(os.path.join(ROOT, "units.json"), encoding="utf-8"))

edits = collections.defaultdict(dict)  # rel -> {off: text}
for uid, u in units.items():
    t = pt.get(uid)
    if not t: continue
    if NOACC: t = "".join(c for c in unicodedata.normalize("NFD", t) if not unicodedata.combining(c))
    for rel, off in u["at"]: edits[rel][off] = t

shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(itd.SRC, OUT)
done = bad = 0
for rel, ed in edits.items():
    env, obj = itd.load(rel)
    b = bytearray(itd.script(obj))
    caps = {off: cap for off, cap, _ in itd.fields(bytes(b))}
    for off, t in ed.items():
        try: e = itd.encode(t, caps[off])
        except ValueError as x: print(f"TOO LONG {rel}@{off}: {x}: {t!r}"); bad += 1; continue
        b[off:off + caps[off] + 2] = e + b"\0" * (caps[off] + 2 - len(e))
        done += 1
    data = obj.read()
    data.m_Script = bytes(b).decode("utf-8", "surrogateescape")
    data.save()
    open(os.path.join(OUT, rel), "wb").write(env.file.save(packer="original"))
print(f"{done} strings written, {bad} too long, {len(edits)} files -> out/")
sys.exit(1 if bad else 0)

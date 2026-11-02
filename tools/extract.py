# python -I tools/extract.py : builds units.json (id -> where it is used) and batches/NNN.json ({id: English}).
# A unit is one English string per speaker: the same line spoken by two characters is two units (PT gender/voice).
import json, os, sys, hashlib, collections
sys.path.insert(0, os.path.dirname(__file__))
import itd

ROOT = os.path.join(os.path.dirname(__file__), "..")
PER_SPEAKER = {b"AACP", b"APCP", b"THCP", b"OCMD"}  # field index = speaker
PER_RECORD = {b"CHMP"}  # record id = speaker
BATCH = 450

names = {}
for rel in itd.files():
    _, o = itd.load(rel)
    b = itd.script(o)
    if b[:4] == b"CNPD" and "/base/" in "/" + rel:
        for off, _, t in itd.fields(b): names[(off - 6) // 258] = t

units = collections.OrderedDict()  # (group, speaker, en) -> {"en", "group", "speaker", "at": [[rel, off]]}
for rel in sorted(itd.files(), key=lambda r: ("/dlc/" in "/" + r, r)):
    _, o = itd.load(rel)
    b = itd.script(o)
    magic, sch = b[:4], itd.SCHEMA.get(b[:4])
    group = os.path.basename(rel).lower()
    for off, cap, en in itd.fields(b):
        spk = ""
        if magic in PER_SPEAKER:
            col = ((off - 4) % sch[0] - 2) // 512
            spk = names.get(col + 1, f"#{col + 1}")
        elif magic in PER_RECORD:
            spk = names.get(int.from_bytes(b[4 + (off - 4) // sch[0] * sch[0]:][:2], "little"), "")
        if "/map/" in rel.lower(): group = "map"
        k = (group, spk, en)
        u = units.setdefault(k, {"en": en, "group": group, "speaker": spk, "at": []})
        u["at"].append([rel, off])
        u["cap"] = min(u.get("cap", 1 << 20), cap // 2)  # chars

out, batches, cur = {}, [], []
last = None
talk = lambda g: g.startswith(("talk", "outercharacter"))
order = sorted(units.items(), key=lambda kv: (talk(kv[0][0]), kv[0][1] if talk(kv[0][0]) else ""))  # stable: talk grouped per speaker
for (g, s, en), u in order:
    uid = hashlib.sha1(f"{g}\t{s}\t{en}".encode()).hexdigest()[:10]
    out[uid] = u
    if talk(g): g = "talk"  # one batch per speaker across all talk files
    if cur and (len(cur) >= BATCH * (1.5 if g == "talk" else 1) or (g, s) != last and (g == "talk" or len(cur) >= BATCH * 0.6)):
        batches.append(cur); cur = []
    cur.append(uid); last = (g, s)
if cur: batches.append(cur)

json.dump(out, open(os.path.join(ROOT, "units.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for i, ids in enumerate(batches):
    d = collections.OrderedDict()
    for uid in ids:
        u = out[uid]
        d.setdefault(f"{u['group']} | {u['speaker'] or '-'}", {})[uid] = u["en"]
    json.dump(d, open(os.path.join(ROOT, "batches", f"{i:03d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "units,", sum(len(u["at"]) for u in out.values()), "uses,", len(batches), "batches")
print(collections.Counter(u["group"] for u in out.values()).most_common())

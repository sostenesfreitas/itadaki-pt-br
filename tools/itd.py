# Read/write the game's text tables (Unity 5.4 TextAsset, UTF-16LE, fixed-size fields).
# Message tables: 4-byte magic + records [u16 id][fields...]; schema below.
# Map/prize tables: binary records with 256-byte name fields; strings found by scanning (see scan()).
import os, re, struct, UnityPy

SRC = os.path.join(os.path.dirname(__file__), "..", "src")

# magic: (record size, field sizes after the u16 id)
SCHEMA = {
    b"BGDD": (258, [256]), b"BGND": (258, [256]), b"BGMN": (258, [256]), b"CNPD": (258, [256]),
    b"CUND": (258, [256]), b"CCMP": (1538, [512] * 3), b"CDMP": (2050, [1024] * 2),
    b"CHMP": (1858, [64] * 29), b"MDMP": (3586, [512] * 7), b"STPD": (514, [256] * 2),
    b"MSRD": (514, [256] * 2), b"MTPD": (260, [2, 256]), b"MUTP": (770, [256] * 3),
    b"TOMP": (770, [256] * 3), b"OCMD": (14850, [512] * 29),
    b"AACP": (13314, [512] * 26), b"APCP": (13314, [512] * 26), b"THCP": (13314, [512] * 26),
    **{m: (322, [64, 256]) for m in (b"CSMP", b"ISMP", b"MGBT", b"MGCB", b"MGMT", b"MGST", b"OSMP", b"TMCC")},
}
IDENT = re.compile(r"^[A-Z0-9_]+$")
LETTERS = re.compile(r"[A-Za-z]{2}")
RUN = re.compile(rb"(?:[\x20-\x7e\x0a\xa0-\xfe]\x00){2,}")


def files():
    """All text-table files under src/, as paths relative to src/."""
    for root, _, fs in os.walk(SRC):
        for f in fs:
            p = os.path.relpath(os.path.join(root, f), SRC).replace("\\", "/")
            if "/parameter/" in p.lower(): yield p


def load(rel):
    env = UnityPy.load(os.path.join(SRC, rel))
    obj = next(o for o in env.objects if o.type.name == "TextAsset")
    return env, obj


def script(obj):
    return obj.read().m_Script.encode("utf-8", "surrogateescape")


def fields(b):
    """Yield (offset, capacity_bytes, text) for every translatable string. Capacity excludes the NUL terminator."""
    sch = SCHEMA.get(b[:4])
    if sch:
        size, sizes = sch
        assert (len(b) - 4) % size == 0, (b[:4], len(b))
        for r in range(4, len(b), size):
            off = r + 2
            for fs in sizes:
                raw = b[off:off + fs].decode("utf-16le", "surrogatepass").rstrip("\0")
                if LETTERS.search(raw) and not IDENT.match(raw): yield off, fs - 2, raw
                off += fs
        return
    # ponytail: map/prize tables scanned for ASCII runs; field = up to next non-zero wchar, max 256 bytes.
    # Upgrade to a real schema if a table ever has a string field followed by an all-zero numeric field.
    for m in RUN.finditer(b):
        s, t = m.start(), m.group().decode("utf-16le")
        if s % 2 or not re.search(r"[a-z]{2}", t): continue
        end = s + len(m.group())
        while end < len(b) and end - s < 256 and b[end:end + 2] == b"\0\0": end += 2
        if end - s < 64: continue  # real name fields are 256 bytes; short gaps are binary noise
        yield s, end - s - 2, t


def encode(text, cap):
    e = text.encode("utf-16le", "surrogatepass")
    if len(e) > cap: raise ValueError(f"{len(e) // 2} chars > {cap // 2}")
    return e

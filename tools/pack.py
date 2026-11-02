# python -I tools/pack.py <ver> : builds both variants and writes dist/itadaki-ptbr-v<ver>.zip and -sem-acentos.zip
import os, sys, subprocess, zipfile, shutil
ROOT = os.path.join(os.path.dirname(__file__), "..")
os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
for flag, suffix in (([], ""), (["--no-accents"], "-sem-acentos")):
    subprocess.run([sys.executable, "-I", "-X", "utf8", os.path.join(ROOT, "tools", "build.py"), *flag], check=True)
    out = os.path.join(ROOT, "out")
    for f in ("base/README.txt", "dlc/README-DLC.txt"):
        if os.path.exists(os.path.join(out, f)): os.remove(os.path.join(out, f))
    shutil.copy(os.path.join(ROOT, "LEIA-ME.txt"), out)
    z = os.path.join(ROOT, "dist", f"itadaki-ptbr-v{sys.argv[1]}{suffix}.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, fs in os.walk(out):
            for f in fs:
                p = os.path.join(root, f)
                zf.write(p, os.path.relpath(p, out).replace("\\", "/"))
    print(z)

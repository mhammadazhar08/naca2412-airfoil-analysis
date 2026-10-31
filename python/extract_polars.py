import csv
import re
import struct
import sys
from pathlib import Path

COLS = ["alpha", "Cd", "Cdp", "Cl", "Cm", "XTr_top",
        "XTr_bot", "HMom", "Cpmin", "Re", "XCp"]


def extract(xfl_path, out_dir):
    b = Path(xfl_path).read_bytes()
    # Strings are UTF-16 but may start at an odd byte offset, so decode both alignments
    text = b.decode("utf-16-be", errors="ignore") + \
        b[1:].decode("utf-16-be", errors="ignore")
    names = sorted(
        set(re.findall(r"T\d_Re\d+\.\d{3}_M\d\.\d{2}_N\d+\.\d", text)))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    foil = re.search(r"NACA\s?\d{4}", text).group(0).replace(" ", "").lower()
    for name in names:
        re_val = float(re.search(r"Re(\d+\.\d{3})", name).group(1)) * 1e6
        i = b.find(name.encode("utf-16-be"))
        j = b.find(struct.pack(">d", re_val), i)
        n = struct.unpack(">i", b[j + 48:j + 52])[0]
        p = j + 52
        rows = [struct.unpack(">11d", b[p + 88 * k:p + 88 * (k + 1)])
                for k in range(n)]
        out = out_dir / f"{foil}_polar_Re{re_val / 1e6:g}M.csv"
        with open(out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(COLS)
            w.writerows([[round(v, 6) for v in r] for r in rows])
        print(f"{name}: {n} points -> {out}")


if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")

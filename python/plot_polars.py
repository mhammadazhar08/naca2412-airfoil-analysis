import matplotlib.pyplot as plt
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")


def main(data_dir, out_png, foil="naca2412"):
    files = sorted(Path(data_dir).glob(f"{foil}_polar_Re*M.csv"),
                   key=lambda p: float(p.stem.split("Re")[1].rstrip("M")))
    shades = plt.cm.Blues(np.linspace(0.45, 1.0, len(files)))
    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    for f, c in zip(files, shades):
        d = np.genfromtxt(f, delimiter=",", names=True)
        a, cl, cd, cm = d["alpha"], d["Cl"], d["Cd"], d["Cm"]
        re_m = f.stem.split("Re")[1]
        lab = f"Re = {re_m.rstrip('M')}×10$^6$"
        lin = (a >= -4) & (a <= 6)
        k, c0 = np.polyfit(a[lin], cl[lin], 1)
        i, j = np.argmax(cl), np.argmax(cl / cd)
        print(f"{f.stem}: slope {k:.4f}/deg, alpha_L0 {-c0 / k:.2f} deg, "
              f"Clmax {cl[i]:.3f} at {a[i]:g} deg, Cdmin {cd.min():.5f}, "
              f"best Cl/Cd {cl[j] / cd[j]:.1f} at {a[j]:g} deg")
        ax[0, 0].plot(a, cl, "-o", ms=2.5, c=c, label=lab)
        ax[0, 1].plot(cd, cl, "-o", ms=2.5, c=c, label=lab)
        ax[1, 0].plot(a, cl / cd, "-o", ms=2.5, c=c, label=lab)
        ax[1, 1].plot(a, cm, "-o", ms=2.5, c=c, label=lab)
    aa = np.linspace(-5, 15, 10)
    ax[0, 0].plot(aa, 2 * np.pi * np.radians(aa + 2.08),
                  "k--", lw=1, label="Thin-airfoil theory")
    titles = [("Lift curve", "α (deg)", "$C_l$"), ("Drag polar", "$C_d$", "$C_l$"),
              ("Lift-to-drag ratio", "α (deg)", "$C_l/C_d$"), ("Pitching moment (c/4)", "α (deg)", "$C_m$")]
    for a_, (t, xl, yl) in zip(ax.flat, titles):
        a_.set(title=t, xlabel=xl, ylabel=yl)
        a_.grid(alpha=.3)
        a_.legend(fontsize=8)
        a_.axhline(0, c="k", lw=.5)
    fig.suptitle(
        f"{foil.upper().replace('NACA', 'NACA ')} — XFLR5/XFoil polars, M = 0.2, $N_{{crit}}$ = 9, 200 panels", fontsize=13)
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    print("saved", out_png)


if __name__ == "__main__":
    main(*sys.argv[1:4])

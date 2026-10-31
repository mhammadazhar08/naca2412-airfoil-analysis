import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COL = ["#1f5fbf", "#d9822b"]
RES = [1, 3, 6, 9]

def load(d, foil, re):
    return np.genfromtxt(Path(d) / f"{foil}_polar_Re{re}M.csv", delimiter=",", names=True)

def name(f): return f.upper().replace("NACA", "NACA ")

def key_values(d):
    a, cl, cd, cm = d["alpha"], d["Cl"], d["Cd"], d["Cm"]
    lin = (a >= -4) & (a <= 6)
    k, c0 = np.polyfit(a[lin], cl[lin], 1)
    i, j = np.argmax(cl), np.argmax(cl / cd)
    return dict(slope=k, aL0=-c0 / k, clmax=cl[i], astall=a[i], cdmin=cd.min(), ld=cl[j] / cd[j], ald=a[j], cm=cm[lin].mean())

def main(data_dir, f1, f2, re, out_dir):
    out = Path(out_dir)
    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    for f, c in zip([f1, f2], COL):
        d = load(data_dir, f, re)
        ax[0, 0].plot(d["alpha"], d["Cl"], "-o", ms=2.5, c=c, label=name(f))
        ax[0, 1].plot(d["Cd"], d["Cl"], "-o", ms=2.5, c=c, label=name(f))
        ax[1, 0].plot(d["alpha"], d["Cl"] / d["Cd"], "-o", ms=2.5, c=c, label=name(f))
        ax[1, 1].plot(d["alpha"], d["Cm"], "-o", ms=2.5, c=c, label=name(f))
    T = [("Lift curve", "α (deg)", "$C_l$"), ("Drag polar", "$C_d$", "$C_l$"),
         ("Lift-to-drag ratio", "α (deg)", "$C_l/C_d$"), ("Pitching moment (c/4)", "α (deg)", "$C_m$")]
    for a_, (t, xl, yl) in zip(ax.flat, T):
        a_.set(title=t, xlabel=xl, ylabel=yl); a_.grid(alpha=.3); a_.legend(fontsize=9); a_.axhline(0, c="k", lw=.5)
    ax[0, 1].set_xlim(0, 0.04)
    ax[1, 1].set_ylim(-0.08, 0.06)
    fig.suptitle(f"{name(f1)} vs {name(f2)} — Re = {re}×10$^6$, M = 0.2, $N_{{crit}}$ = 9, 200 panels", fontsize=13)
    fig.tight_layout(); fig.savefig(out / f"compare_{f1}_{f2}_Re{re}M.png", dpi=200); plt.close(fig)

    # Key values across Reynolds number
    kv = {f: [key_values(load(data_dir, f, r)) for r in RES] for f in [f1, f2]}
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
    for f, c in zip([f1, f2], COL):
        ax[0].plot(RES, [k["clmax"] for k in kv[f]], "-o", c=c, label=name(f))
        ax[1].plot(RES, [k["ld"] for k in kv[f]], "-o", c=c, label=name(f))
        ax[2].plot(RES, [k["astall"] for k in kv[f]], "-o", c=c, label=name(f))
    for a_, t in zip(ax, ["Maximum lift $C_{l,max}$", "Best lift-to-drag ratio", "Stall angle (deg)"]):
        a_.set(title=t, xlabel="Reynolds number (millions)", xticks=RES); a_.grid(alpha=.3); a_.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(out / f"compare_{f1}_{f2}_vs_Re.png", dpi=200); plt.close(fig)

    print(f"{'':6}{'airfoil':10}{'slope':>8}{'aL0':>7}{'Clmax':>7}{'stall':>7}{'Cdmin':>9}{'L/D':>7}{'at':>6}{'Cm':>8}")
    for f in [f1, f2]:
        for r, k in zip(RES, kv[f]):
            print(f"{r}M    {f:10}{k['slope']:8.4f}{k['aL0']:7.2f}{k['clmax']:7.3f}{k['astall']:7.1f}{k['cdmin']:9.5f}{k['ld']:7.1f}{k['ald']:6.1f}{k['cm']:8.4f}")

if __name__ == "__main__":
    main(*sys.argv[1:4], int(sys.argv[4]), sys.argv[5])

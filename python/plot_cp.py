import matplotlib.pyplot as plt
import re
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")


def main(path, out_png):
    header = open(path).read().splitlines()[3]
    alpha = float(re.search(r"Alpha\s*=\s*(-?[\d.]+)", header).group(1))
    d = np.loadtxt(path, skiprows=6)
    x, cpi, cpv = d[:, 0], d[:, 1], d[:, 2]
    # leading edge splits upper / lower
    le = int(np.argmin(x))
    up, lo = slice(0, le + 1), slice(le, len(x))
    trap = getattr(np, "trapezoid", None) or np.trapz
    cn = trap(cpv[lo], x[lo]) - trap(cpv[up][::-1], x[up][::-1])
    print(
        f"alpha = {alpha} deg, Cl from Cp integration = {cn * np.cos(np.radians(alpha)):.3f}")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x[up], cpv[up], c="#1f6fb2", lw=2, label="Upper surface (viscous)")
    ax.plot(x[lo], cpv[lo], c="#d1495b", lw=2, label="Lower surface (viscous)")
    ax.plot(x[up], cpi[up], "--", c="#1f6fb2", lw=1,
            alpha=.6, label="Upper (inviscid)")
    ax.plot(x[lo], cpi[lo], "--", c="#d1495b", lw=1,
            alpha=.6, label="Lower (inviscid)")
    ax.invert_yaxis()
    ax.axhline(0, c="k", lw=.6)
    ax.grid(alpha=.3)
    ax.set(xlabel="x/c", ylabel="$C_p$",
           title=f"{open(path).read().splitlines()[1]} pressure distribution, α = {alpha:g}°")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    print("saved", out_png)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

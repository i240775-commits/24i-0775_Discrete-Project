
"""
CS1005 Discrete Structures - Fall 2026 - Network motifs in email-Eu-core
FILE 3 of 3: null_model.py   (tasks T5, T6 and T7; runs the whole pipeline)

Group roll numbers: 0775, 1050, 1052
R = 775 + 1050 + 1052 = 2877
  pair number = 27 -> (1, 10); Department A = top-20[1], Department B = top-20[10]
  random networks = 45; swap attempts = 8 x |E|; seed = 2877

Run:  python null_model.py     (needs data_prep.py and triads.py in the same folder)
Output: tables of counts and Z-scores, motif / anti-motif lists, and
        zscores_R2877.png in --out-dir.
"""
import math
import os
import random

from data_prep import R, N_RANDOM, SWAP_MULT, SEED, get_args, setup
from triads import count_triads


# ------------------------------------------------------------------- T5
def randomize(edges, attempts, seed):
    """Double-edge swaps. `seed` may be an int or a random.Random instance.
    Rejected attempts still count. Always starts from the given edge list."""
    rng = seed if isinstance(seed, random.Random) else random.Random(seed)
    E = list(edges)
    S = set(E)
    m = len(E)
    for _ in range(attempts):
        i = rng.randrange(m)
        j = rng.randrange(m)
        if i == j:                       # same edge picked twice -> reject
            continue
        a, b = E[i]
        c, d = E[j]
        if a == d or c == b or (a, d) in S or (c, b) in S:
            continue
        S.discard((a, b)); S.discard((c, d))
        E[i], E[j] = (a, d), (c, b)
        S.add((a, d)); S.add((c, b))
    return E


def degrees(edges):
    ind, outd = {}, {}
    for u, v in edges:
        outd[u] = outd.get(u, 0) + 1
        ind[v] = ind.get(v, 0) + 1
    return ind, outd


# ------------------------------------------------------------------- T6
def zscores(real, samples):
    z = []
    n = len(samples)
    for k in range(13):
        vals = [s[k] for s in samples]
        mu = sum(vals) / n
        sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / n)   # population std
        z.append(0.0 if sd == 0 else (real[k] - mu) / sd)
    return z


def analyse(name, edges, rng):
    real = count_triads(edges)
    ind0, out0 = degrees(edges)
    attempts = SWAP_MULT * len(edges)
    samples = []
    for _ in range(N_RANDOM):
        g = randomize(edges, attempts, rng)
        ind, outd = degrees(g)
        assert ind == ind0 and outd == out0, "degree sequence changed!"
        assert len(set(g)) == len(g) and all(u != v for u, v in g), "not simple"
        samples.append(count_triads(g))
    print(f"{name}: degree-preservation assertions passed for {N_RANDOM} graphs")
    return real, zscores(real, samples)


# ------------------------------------------------------------------- T7
def plot(zA, zB, labelA, labelB, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    x = list(range(1, 14))
    w = 0.38
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar([i - w / 2 for i in x], zA, w, label=labelA)
    ax.bar([i + w / 2 for i in x], zB, w, label=labelB)
    for y in (2, -2):
        ax.axhline(y, ls="--", color="k", lw=1)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xticks(x)
    ax.set_xlabel("Triad class")
    ax.set_ylabel("Z-score")
    ax.set_title(f"Motif Z-scores, departments {labelA} vs {labelB}  (R = {R})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    args = get_args("T5-T7: null model, Z-scores, chart")
    A, B, subA, subB = setup(args.data_dir)

    rng = random.Random(SEED)
    final = {"A": analyse("A", subA, rng), "B": analyse("B", subB, rng)}

    print("\nclass | N_A | Z_A | N_B | Z_B")
    for k in range(13):
        print(f"{k+1:5d} | {final['A'][0][k]:5d} | {final['A'][1][k]:7.2f} | "
              f"{final['B'][0][k]:5d} | {final['B'][1][k]:7.2f}")
    for name in ("A", "B"):
        mot = [k + 1 for k, z in enumerate(final[name][1]) if z > 2]
        anti = [k + 1 for k, z in enumerate(final[name][1]) if z < -2]
        print(f"Dept {name}: motifs {mot}, anti-motifs {anti}")

    os.makedirs(args.out_dir, exist_ok=True)
    out = os.path.join(args.out_dir, f"zscores_R{R}.png")
    plot(final["A"][1], final["B"][1], f"A (dept {A})", f"B (dept {B})", out)
    print("chart saved to", out)


if __name__ == "__main__":
    main()


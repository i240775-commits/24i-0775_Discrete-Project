
"""
CS1005 Discrete Structures - Fall 2026 - Network motifs in email-Eu-core
FILE 1 of 3: data_prep.py   (tasks T1 and T2)

Group roll numbers (last 4 digits): 0775, 1050, 1052
R = 775 + 1050 + 1052 = 2877
  pair number       = R mod 190 = 27  -> (i, j) = (1, 10)
  random networks   = 20 + R mod 31 = 45
  swap attempts     = (5 + R mod 6) * |E| = 8 * |E|
  random seed       = 2877

Run on its own:  python data_prep.py
Reads the SNAP files from the data/ folder (nothing is downloaded).
"""
import argparse
import gzip
import os

ROLLS = [775, 1050, 1052]
R = sum(ROLLS)
N_RANDOM = 20 + (R % 31)
SWAP_MULT = 5 + (R % 6)
SEED = R

EDGE_NAME = "email-Eu-core.txt.gz"
DEPT_NAME = "email-Eu-core-department-labels.txt.gz"


# ------------------------------------------------------------ file reading
def _open(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def find_file(data_dir, name):
    """Look only in the data folder (relative to where you run, or next to this
    script). Accepts the .txt.gz or the plain .txt version. Nothing is downloaded."""
    here = os.path.dirname(os.path.abspath(__file__))
    folders = [data_dir]
    if not os.path.isabs(data_dir):
        folders.append(os.path.join(here, data_dir))
    for folder in folders:
        for fname in (name, name[:-3]):
            p = os.path.join(folder, fname)
            if os.path.exists(p):
                print("using local file:", p)
                return p
    raise FileNotFoundError(
        f"Could not find '{name}' (or '{name[:-3]}') in the '{data_dir}' folder. "
        f"Put the SNAP files in a folder called '{data_dir}' next to the scripts.")


# ------------------------------------------------------------------- T1
def load(data_dir):
    edges = set()
    with _open(find_file(data_dir, EDGE_NAME)) as f:
        for line in f:
            p = line.split()
            if len(p) >= 2 and p[0] != p[1]:          # drop self-loops
                edges.add((int(p[0]), int(p[1])))      # set drops duplicates
    dept = {}
    with _open(find_file(data_dir, DEPT_NAME)) as f:
        for line in f:
            p = line.split()
            if len(p) >= 2:
                dept[int(p[0])] = int(p[1])
    return sorted(edges), dept


def top20(edges, dept):
    internal = {}
    for u, v in edges:
        if u in dept and v in dept and dept[u] == dept[v]:
            internal[dept[u]] = internal.get(dept[u], 0) + 1
    ranked = sorted(internal, key=lambda d: (-internal[d], d))
    return ranked[:20], internal


def pair_from_number(n):
    pairs = [(i, j) for i in range(20) for j in range(i + 1, 20)]
    return pairs[n]


# ------------------------------------------------------------------- T2
def subgraph(edges, dept, d):
    members = {n for n, x in dept.items() if x == d}
    return members, [(u, v) for u, v in edges if u in members and v in members]


# ------------------------------------------------------------ shared setup
def get_args(description="motif project"):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out-dir", default=".")
    return ap.parse_args()


def setup(data_dir, verbose=True):
    """Runs T1 + T2. Returns (A, B, subA, subB) where subX is the edge list of
    the induced department subgraph."""
    edges, dept = load(data_dir)
    nodes = {x for e in edges for x in e}
    top, internal = top20(edges, dept)
    pair = R % 190
    i, j = pair_from_number(pair)
    A, B = top[i], top[j]
    subs = {}
    if verbose:
        print(f"nodes in edges: {len(nodes)}, simple edges: {len(edges)}")
        print("top-20 departments (index: dept id, internal edges):")
        for k, d in enumerate(top):
            print(f"  {k:2d}: dept {d:3d}  {internal[d]}")
        print(f"R = {R}; pair number = {pair} -> ({i}, {j}); "
              f"Department A = {A}, Department B = {B}")
        print(f"random networks = {N_RANDOM}; swap attempts = {SWAP_MULT} x |E|; seed = {SEED}")
    for name, d in (("A", A), ("B", B)):
        members, sub = subgraph(edges, dept, d)
        used = {x for e in sub for x in e}
        subs[name] = sub
        if verbose:
            print(f"Dept {name} ({d}): {len(members)} members, "
                  f"{len(used)} with at least one internal edge, {len(sub)} edges")
    return A, B, subs["A"], subs["B"]


if __name__ == "__main__":
    args = get_args("T1 + T2: load, clean, parameters, department subgraphs")
    setup(args.data_dir)

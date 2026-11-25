"""
CS1005 Discrete Structures - Fall 2026 - Network motifs in email-Eu-core
FILE 2 of 3: triads.py   (tasks T3 and T4)

Group roll numbers: 0775, 1050, 1052   |   R = 2877
  Departments A, B = top-20[1], top-20[10] (pair 27)
  45 random networks, 8 x |E| swap attempts, seed 2877

Run on its own:  python triads.py
Prints the hand-worked example and the 13-class triad census of both departments.
Needs data_prep.py in the same folder.
"""
import itertools

from data_prep import R, get_args, setup

# ------------------------------------------------------------------- T3
# bit k of the code <-> k-th edge below
EDGE_BITS = {(0, 1): 0, (0, 2): 1, (1, 0): 2, (1, 2): 3, (2, 0): 4, (2, 1): 5}
CLASS_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {c: k + 1 for k, c in enumerate(CLASS_CODES)}


def canonical_code(has_edge, nodes):
    """Minimum 6-bit code over all 6 orderings of the 3 nodes.
    has_edge(u, v) -> bool tells whether u->v is present."""
    best = 64
    for order in itertools.permutations(nodes):
        code = 0
        for (i, j), bit in EDGE_BITS.items():
            if has_edge(order[i], order[j]):
                code |= 1 << bit
        if code < best:
            best = code
    return best


def triad_class(a, b, c, out):
    """Class 1..13 of the triad {a,b,c}; `out` maps node -> set of out-neighbours.
    Returns None if the triad is not connected."""
    code = canonical_code(lambda u, v: v in out[u], (a, b, c))
    return CODE_TO_CLASS.get(code)


# ------------------------------------------------------------------- T4
# Precomputed table: 64 labelled configurations -> class (None if disconnected)
_CODE_CLASS = {}
for _cfg in range(64):
    _best = 64
    for _perm in itertools.permutations(range(3)):
        _code = 0
        for (_i, _j), _bit in EDGE_BITS.items():
            if _cfg >> EDGE_BITS[(_perm[_i], _perm[_j])] & 1:
                _code |= 1 << _bit
        _best = min(_best, _code)
    _CODE_CLASS[_cfg] = CODE_TO_CLASS.get(_best)


def count_triads(edges):
    """Triad census N[1..13] (list index 0..12). Each connected triple is counted
    exactly once: it is counted at the smallest-id node among the nodes that are
    adjacent to both others (its 'centres'), so no set of triples is needed."""
    out, nbr = {}, {}
    for u, v in edges:
        out.setdefault(u, set()).add(v)
        nbr.setdefault(u, set()).add(v)
        nbr.setdefault(v, set()).add(u)
        out.setdefault(v, set())
    N = [0] * 13
    for v, nb in nbr.items():
        for a, b in itertools.combinations(sorted(nb), 2):
            # a and b adjacent -> all three are centres; count only at the minimum
            if b in nbr[a] and not (v < a):
                continue
            t = (v, a, b)
            cfg = 0
            for (i, j), bit in EDGE_BITS.items():
                if t[j] in out[t[i]]:
                    cfg |= 1 << bit
            N[_CODE_CLASS[cfg] - 1] += 1
    return N


if __name__ == "__main__":
    args = get_args("T3 + T4: triad classes and census")
    # hand example: cycle 0->1->2->0 has bits 0,3,4 -> code 1+8+16 = 25 -> class 9
    demo = {0: {1}, 1: {2}, 2: {0}}
    print("hand example: 0->1,1->2,2->0 gives class", triad_class(0, 1, 2, demo),
          "(expected 9, code 25)\n")
    A, B, subA, subB = setup(args.data_dir)
    NA, NB = count_triads(subA), count_triads(subB)
    print(f"\nTriad census (R = {R})")
    print("class | Dept A (%d) | Dept B (%d)" % (A, B))
    for k in range(13):
        print(f"{k+1:5d} | {NA[k]:10d} | {NB[k]:10d}")
    # optional sanity check against networkx (different class order!) - checking only
    try:
        import networkx as nx
        for name, sub, N in (("A", subA, NA), ("B", subB, NB)):
            tc = nx.triadic_census(nx.DiGraph(sub))
            tot = sum(v for k, v in tc.items() if k not in ("003", "012", "102"))
            print(f"[check] Dept {name}: networkx connected-triad total = {tot} vs mine {sum(N)}")
    except ImportError:
        pass


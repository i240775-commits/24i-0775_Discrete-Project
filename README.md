# 24i-0775_Discrete-Project
24i-0775_ 25i-1050_ 25i-1052       Discrete-Project

## Contributions

### Member 1: 24i-0775 [Abdul Ahad Shakeeb] – `data_prep.py` (T1, T2)
- Loaded the SNAP edge and department-label files from the `data/` folder.
- Cleaned the data: removed 642 self-loops and duplicate edges so the graph is simple (24,929 edges).
- Ranked departments by internal edges (ties broken by smaller ID) and built the top-20 list.
- Derived R = 2877 and all parameters: pair 27 → (1, 10), 45 random networks, 8 × edges swap attempts, seed 2877.
- Built the induced subgraphs of Department A (dept 4, 1,167 edges) and Department B (dept 19, 306 edges).
- Wrote the command-line options (`--data-dir`, `--out-dir`) and the parameter printout.

### Member 2: 25i-1050 [M.Akibur Islam] – `triads.py` (T3, T4)
- Implemented the 6-bit edge encoding and the canonical code (minimum over all 6 orderings).
- Wrote `triad_class(a, b, c)` and the precomputed 64 → 16 → 13 class table.
- Worked the hand example (cycle 0→1→2→0: code 25, class 9).
- Implemented `count_triads`, which counts each connected triple exactly once, using neighbour pairs instead of all C(n,3) subsets.
- Verified the counts against `nx.triadic_census` (check only) and against a brute-force count on test graphs.

### Member 3: 25i-1052 [Tohidur Rehman] – `null_model.py` (T5, T6, T7)
- Implemented `randomize` (double-edge swaps with the rejection rules; rejected attempts still count).
- Added the assertions that every node's in- and out-degree is unchanged and the graph stays simple.
- Computed Z-scores with the population standard deviation (Z = 0 if σ = 0) and classified motifs and anti-motifs.
- Produced the grouped bar chart with dashed lines at ±2 and R in the title.

### All members
- Reviewed and tested each other's code so everyone can explain every file.
- Recorded the video presentation and wrote the README.
- Wrote the T8 comparison paragraph together.


## R and derived parameters
R = 775 + 1050 + 1052 = **2877**

| Parameter | Formula | Value |
|---|---|---|
| Department pair number | R mod 190 | 27 → pair (1, 10) |
| Department A | top-20[1] | **Department 4** (1,167 internal edges, 109 members) |
| Department B | top-20[10] | **Department 19** (306 internal edges, 29 members) |
| Random networks | 20 + (R mod 31) | 45 |
| Swap attempts per network | (5 + (R mod 6)) × edges | 8 × edges (9,336 for A, 2,448 for B) |
| Random seed | R | 2877 |

Preprocessing: 25,571 edge lines in the raw file → 24,929 simple edges after removing 642 self-loops (no non-loop duplicates). 1,005 people, of which 986 appear in at least one edge.

## How to run
1. Install Python 3 and the plotting library: `pip install matplotlib` (optional: `pip install networkx`, used only to check the T4 counts).
2. Put the project in one folder like this:
```
data_prep.py
triads.py
null_model.py
data/
    email-Eu-core.txt
    email-Eu-core-department-labels.txt
```
(the `.txt.gz` versions of the two data files also work; nothing is downloaded by the code)
3. Run `python null_model.py`. It runs the full pipeline and saves `zscores_R2877.png`.

Each file can also be run on its own:
- `python data_prep.py` – T1, T2: loading, cleaning, parameters, department subgraphs
- `python triads.py` – T3, T4: hand example and the 13-class triad census of both departments
- `python null_model.py` – T5, T6, T7: randomization, Z-scores, chart

- ## Results (R = 2877)
Motifs (Z > 2) and anti-motifs (Z < −2):
- Department A (dept 4): motifs 8, 13; anti-motifs 1, 2, 4, 5, 6, 7, 9, 10, 11
- Department B (dept 19): motifs 8, 13; anti-motifs 1, 2, 5, 6, 9, 10, 11, 12

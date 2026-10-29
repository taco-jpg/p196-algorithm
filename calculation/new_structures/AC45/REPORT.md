# AC45: carry MDD control (UNDECIDED)
Label: **UNDECIDED** for PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH.
The actual pi185 120-time-layer symbolic product, free J and palindromic C, has **not** been constructed or decided. No decimal Lychrel existence or exclusion is claimed.

This is a reusable exact **one-spatial-layer** two-port carry MDD skeleton: state (l,h), coefficient x in [0,18], and outgoing high-port hp in {0,1}, constrained by floor((x+hp)/10)=h and l'=floor((x+l)/10). The two boundary hypotheses must be constrained by the full physical product. Its four-state bound must **not** be confused with a bound on the 120-time-layer reachable set.

`python3 calculation/new_structures/AC45/symbolic.py` exhaustively checks 27,432 small canonical pairword inputs against an independent Python integer reverse/add and replays 120 exact ordinary decimal steps at (q,k)=(14,100),(20,160),(40,320),(80,640),(160,1280), with U=(9,0,18), J=[5,9,1,4,3,0,6], C=[8,8]. All pass. MDD state counts at widths 1,2,4,8,16,32,120 are 4 each; these are **spatial single-step** counts, not pi185 measurements. A zero-step planted identity is a trivial harness sanity control, not a planted 120-step return.

Needed next: temporally coupled 120-column coefficient/carry relation with exact gamma lag, central realization, simultaneous source/target template constraints and endpoint-only W9 restoration, then a full nonemptiness/emptiness decision. The current output has no exhaustive seam search and no CELL status.

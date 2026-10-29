# N26: an apparent two-sector moving-frame front in decimal p8
**Label: COMPUTED**, for the explicitly listed seeds and 105 finite snapshots. Not a proof of an infinite decimal orbit and NOT a closed renormalisation fixed point.

## Coordinate frame
Use the exact decimal seed family N_c from AgentN26DecimalP8Shield, built from the reachable period-8/period-20 rec0 pairword lattice with c repeated spatial cells. Set t_c(r) = 88c+4+r for -16<=r<=88 and take the lower-half pairword window G_c(r,j)=P^{(c)}_{t_c(r)}[38+j]. Thus increasing c by one adds 20 columns to the spatial band and moves the observation time forward 88 real reverse-and-add steps, aligning the temporal p8 phase. This is a *moving-frame*, rather than a stationary short-centre, test.

## Observed two-sector structure
A separate least-significant-first digit-list replay computes each G_c from an ordinary decimal seed. For every one of 105 frames, the c=40 and c=42 windows agree in their first **252 coefficients** (and first 270 at r=0), while c=40 and c=41 agree in only the first **144 coefficients** uniformly (164 at r=0). For c=50 and c=60 the same bounds persist: two extra copies produce better spatial alignment than one extra copy. At c=30 the two-copy common prefix is only 191 in the worst frame, indicating a finite transient before the 252-column observation.
This is evidence for a *two-sector / 176-step* (two-copy) renormalisation coordinate, not a single 88-step fixed point. Crucially, the match breaks: even c=40 versus c=42 differs beyond coefficient 251 in at least one time frame; no all-width or all-copy equality has been established. The finite mismatch is the target for a symbolic interface/wake transducer, rather than another stationary-centre no-go.

## Data and reproduction
All coefficients are pair sums d_j+d_{n-1-j}, indexed from the least-significant end. Input is the compact exact p8/rec0 data file created with the first result. This program imports that result's independent `check_digits.py` *digit-list* update only; it never uses the coefficient normalisation map as its evolution rule.

    cd calculation/new_structures/agent-N26
    python3 glider_renorm.py p8_rec0_rows.txt --c 20 --width 300
    python3 glider_renorm.py p8_rec0_rows.txt --c 30 --width 300
    python3 glider_renorm.py p8_rec0_rows.txt --c 40 --width 300
    python3 glider_renorm.py p8_rec0_rows.txt --c 50 --width 300

The exact output table (minimum, at r=0, at r=88, maximum common-prefix lengths across 105 frames) is in `glider_renorm_observations.csv`. For c=60..80 the table records additional computed runs of the same code. Causality and long-range finite-memory effects explain why finite windows may stabilise without any infinite-periodicity certificate: this observation alone cannot establish the required invariant for arbitrary c.

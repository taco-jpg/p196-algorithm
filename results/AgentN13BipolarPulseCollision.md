# Agent N13: a decimal two-front lattice pulse and its centre-wave collision
**COMPUTED**, finite base-10 statement (6,000 steps); no infinite Lychrel certificate.
Start with a 10,400-digit seed from the reachable p8/m20 exterior and change only paired coefficients `j=2000..2099`; compare with its unperturbed orbit, and also compare the unperturbed orbit with a 24,000-digit clean-exterior control.
The left edge `L(t)` of the isolated defect satisfies `L(t+22)=L(t)-5` for **every t=18..5978** (5,961 comparisons).
Its right edge `R(t)` satisfies `R(t+22)=R(t)+15` for **every t=10..3405** (3,396 comparisons), an inward-moving front opposite to the first edge.
The independent centre-origin front `C(t)` satisfies `C(t+22)=C(t)-5` for **every t=52..5978** (5,927 comparisons).
The two moving fronts meet at **t=3426** (`R=4434, C=4433`); the predicted right-edge 22-step translation first disagrees with the observed orbit at **t=3428**.
The pulse expansion thus has two distinct ballistic speeds before collision; its later failure is a concrete *interaction with the centre-origin wave*, not evidence against unrelated glider constructions.
A separate Python arbitrary-precision three-orbit reverse-and-add replay agrees with **all 801 time rows t=0..800** (first/last defect, changed-pair count, centre front, length).
Reproduce: `bash calculation/new_structures/agent-N13/pulse_run.sh`, using `pulse_collision.cpp`, `pulse_check.py`, `pulse_independent.py`, `pulse_keyframes.csv` in that directory.
Details: `reports/AgentN13BipolarPulseCollision.md`. Neither perpetual fronts nor an indefinitely maintained exterior is claimed.

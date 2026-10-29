# Y45: primitive p24 fixed-seam charge obstruction

**Scope: PAPER PROOF; negative result for one template class only.** Let (g) be a primitive base-10 overflow word of period (p=24), and let
[
P(q)=E,W^q,J,C,J^{\mathrm{rev}}\,(W^{\mathrm{rev}})^q\,E^{\mathrm{rev}}
]
be a canonical symmetric pair-coefficient family with fixed (E,W,J,C), (m=|W|\ge1), and target (P(q+\Delta q)), (\Delta q>0), after one 120-step epoch.

The exact F1 cycle-mean bounds give (p/4\le G\le p/2), where (G=|g|_1); equality occurs only for repetitions of (0001) or (01). Primitivity therefore forces (G\in\{7,8,9,10,11\}). Since 120 steps contain five periods, the digit-length gain is (5G), while the fixed-interface template gains (2m\Delta q) coefficients. Hence
[
2m\Delta q=5G.
]
Also (N_{t+1}=N_t+\operatorname{rev}(N_t)\equiv2N_t\pmod9), and (2^{120}\equiv1\pmod9). The sum of the pair coefficients is congruent to (2N_t\pmod9), so a 120-step return requires
[
\Delta q\sum W\equiv0\pmod9.
]
If \(\sum W\not\equiv0\pmod9\), then (9\mid\Delta q). For odd (G\in\{7,9,11\}), the length equation is impossible by parity. For (G=8) or (10), it forces (m\Delta q=20) or (25), so \(\Delta q\) divides 20 or 25 and cannot be divisible by 9. Therefore **no primitive-p24, fixed-seam, fixed-centre, one-band 120-step return exists when \(\sum W\not\equiv0\pmod9\)**.

For a return after (r\) epochs with nonzero band charge, (9\mid\Delta q) and (2m\Delta q=5rG), so (r) must be a multiple of
[
\frac{18m}{\gcd(18m,5G)}.
]
This is a necessary condition, not a seam-survival estimate.

**Not excluded:** charge-zero bands \(\sum W\equiv0\pmod9\), moving or cyclic seams, changing centres, other template formats, existence of a p24 exterior, or decimal Lychrel existence. This redirects the p24 search to the charge-zero band case or a genuinely moving/cyclic interface; it is not a global no-go.

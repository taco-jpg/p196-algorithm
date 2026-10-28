# Agent9F1AllPeriodRecurrence
**PAPER PROOF + exact finite-state integer check.** Let a(n) be the number of
length-n time-rooted base-10 overflow words accepted by the first-coordinate F1 NFA.
For all n>=10, a(n)=a(n-2)+a(n-3)+a(n-4)+a(n-5)+a(n-7)+2a(n-9).
Initial a(0..9)=[1,0,2,3,6,10,11,28,30,75].
The generating function is (1+z²+2z³+3z⁴+4z⁵+6z⁷+16z⁹)/
(1-z²-z³-z⁴-z⁵-z⁷-2z⁹), as a formal power series.
Proof certificate: the 18-state F1 NFA yields 434 reachable Boolean relations;
for their full integer vector F of diagonal-nonempty states, q(T)F=0 pointwise,
q(T)=T^10-T^8-T^7-T^6-T^5-T^3-2T, T=append both labels.
Minimal order 10: integer Hankel determinant -17378887139328 is nonzero.
Reproduce: `python3 calculation/decimal_frontier/exterior_census/py/f1_rooted_recurrence.py`.
**Not claimed:** exact full B-cycle enumeration, a Lychrel number, or a decimal certificate.

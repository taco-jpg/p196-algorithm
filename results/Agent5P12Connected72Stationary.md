# Agent5P12Connected72Stationary

**COMPUTED.** Exact 72-step counterexample to universal strictly outward
first-defect motion for connected decimal p=12/m=9 bulk perturbations.

Start from the published lattice at phase t=2, n=800. Replace EVERY
lower-half coefficient at indices 180..190 with
(6,1,0,1,11,14,10,6,11,16,1), also replacing the reflected mates.
Both symmetric pair words yield canonical decimal seeds.
After 72 ordinary integer reverse-and-add steps both have 818 digits;
the nonzero successor pair-word difference still begins at index 180.

Reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/k2_connected72_counterexample.py`.
Independent schoolbook and big-integer arithmetic agree at all 72 steps.
Not claimed: minimal width, all-width bounds, a periodic centre, or Lychrel existence.
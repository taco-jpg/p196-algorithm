# Scalar clock exclusion and weighted path formalization

- [All-width scalar clock bound](2026-10-14-scalar-clock/SCALAR_CLOCK_BOUND.md).
- [Independent scalar arithmetic and weighted-rank audit](2026-10-14-scalar-clock/INDEPENDENT_SCALAR_AUDIT.md).
- [Fifteen Lean generic weighted path theorems](2026-10-14-scc-bound-formal/README.md).
- [Frozen source and artifact review](2026-10-14-scalar-clock-root-review.json).
- [Shared handoff, capped-probe and recovery scope](../coordination/2026-10-14-scalar-clock-results.md).

The exclusion requires the complete outer sequence (4,8,16,7,15,6,13),
not just an outer 4 at seven-step endpoints. Its conservative period
bound is min(236,232+max(0,ceil((14-L)/3))). Different capped scalar
probes remain UNKNOWN. Numerical graph certification remains separate
from the generic Lean theorem.

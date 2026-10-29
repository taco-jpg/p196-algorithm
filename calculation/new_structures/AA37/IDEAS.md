# AA37 ideas that currently fail

- **Residue-only 2-adic pruning from the pairword:** dead end in its current form. The pairword stores P_i=d_i+d_{n-1-i}, not d_i itself. A mod-2^r calculation on P alone does not identify the physical low-end residue unless the canonical source realization and carry state are retained. Do not use this as a hard SAT/MDD gate.
  - Redirect: formulate the state as (rooted physical boundary digits, low/high carries, clock phase, seam state) and prove a closed cocycle first. Until then, no pruning claim.

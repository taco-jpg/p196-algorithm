# AgentX07CollisionRepair

- **PAPER PROOF:** A complement-nine piston with zero central gap and outgoing low-half carry 1 remains a protected zero-gap piston with complementary high digits, preserved mod-9 charge 8, and guaranteed nonpalindromicity; no claim that the carry remains 1 forever.
- **COMPUTED:** Exhaustive real base-10 reverse-and-add census of the 1,000 guarded width-4 and 100,000 guarded width-6 zero-gap boundary words, through step 200 and stopping on palindromes, finds **136 genuine post-loss regenerations** of a central 9-run: width 4 has 26 with regenerated length 1 (steps 17–20); width 6 has 73 with length 1 and 37 with length 2 (steps 6–9).
- Explicit decimal controls: `94780521` loses protection at t=1, returns at t=19 as `838016291619837` with `L=1`; `996508003491` loses at t=1, returns at t=7 as `75454399245456` with `L=2`.
- **COMPUTED independent check:** Python ordinary big-integer replay at every step t=0..200 for all 136 listed witnesses (zero palindromes; exact return claims); both explicit controls pass 4,000 independent steps. No second positive repair among the 136 in the first 200 steps.
- Source: `calculation/new_structures/agent-X07/renewal_census.cpp`, `independent_renewal.py`; all 136 events: `renewal_events.json`; reproduce: `sh calculation/new_structures/agent-X07/renewal_run.sh`.
- Details and finite scope: `reports/AgentX07CollisionRepair.md`. **Not** an infinite decimal Lychrel certificate, a Lean verification, or a general no-go for repeated repairs; next target is a two-defect relay.

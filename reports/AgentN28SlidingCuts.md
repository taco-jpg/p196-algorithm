# N28: relocating periodic insertion cuts when joints drift

Label: COMPUTED for the 384-step and 757-step decimal family trajectories; PAPER PROOF for the elementary cut-shift lemma. Not LEAN-VERIFIED, not an infinite certificate.

This extends the sound paired-insertion pump format in reports/AgentN28PairedInsertion.md. A pump representation places one insertion cut inside each periodic bulk domain. The same decimal pairword family can have several equivalent cuts. **Cut-shift lemma**: if positions a through b+m-1 of a coefficient word have period m, then inserting q copies of the m-word at cut a or cut b yields the same coefficient word for every q>=0, with the inserted word rotated appropriately at b. Proof: both resulting words agree outside the periodic interval and both equal the same prefix of its bi-infinite period inside; alternatively slide a single m-word through the periodic interval one digit at a time, then induct on q. Reflecting the period gives the corresponding equality at the paired high cut. For multiple disjoint bands the substitutions commute. This is a representation change, not an alteration of the underlying initial number.

Algorithm: at the first failure of a fixed carry-loop contract, inspect alternative cut coordinates within +/-400; require the exact m-periodicity of every position between old and new cuts, preservation of band ordering, and all carry-loop and gamma-offset edge checks at the candidate. Choose the midpoint in the interval of passing candidates. The equality of the expanded family for 1,2,3 inserted copies is independently asserted as a control. Continue the finite-edge computation from the same baseline P without resetting any orbit.

Computed for the three bands (2), (6,12), (18), centre 8 and outer prefix (18,7,18,12), with independent expansion counts k_j>=k:
- k=240: 232 -> 384 certified transitions; 8 relocations. Initial cuts (124,484,844), final cuts (209,484,925). Baseline length 2094 pair coefficients at t=384. The next proposed contract fails PERIOD_BREAK on band 0, so there is no justified continuation of this witness.
- k=480: 442 -> 757 certified transitions; 7 relocations. Initial cuts (244,964,1684), final cuts (403,964,1827). Baseline length 4164 at t=757. The next contract fails GAMMA_SHIFT_INCOMPATIBLE on band 0.

Every successful step carries a fixed nonpalindrome witness outside all insertion cuts. By the paired-pumping theorem plus the cut-shift lemma, **each stated finite prefix is valid simultaneously for all three independent band counts at least k**, not only the sampled numerals. Independent Python arbitrary-precision replay for five count-increment vectors gives 1925 (k=240) and 3790 (k=480) pairword equalities, with no palindrome in the checked prefixes. The earlier independent 20,000-step digit-list replay of the k=240 baseline remains a *finite* observation, not an extension of the all-length format to 20,000 steps.

Reproduce from repository root:
1. python3 calculation/new_structures/agent-N28/reanchor.py --k 240 --steps 800 --check
2. python3 calculation/new_structures/agent-N28/reanchor.py --k 480 --steps 900 --check
3. python3 calculation/new_structures/agent-N28/reanchor.py --k 120 --steps 400

Observations are also recorded under calculation/new_structures/agent-N28/reanchor_observations.json. Next constructive direction: replace exhausted periodic bulk with a regenerated periodic wake or a renormalized packet. Moving cuts postpone collision but by themselves do not supply an infinite certificate.

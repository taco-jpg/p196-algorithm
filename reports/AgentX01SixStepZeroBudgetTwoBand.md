# X01: a zero-budget six-step decimal two-band relay that fails at the next renewal

**COMPUTED only.** A finite zero-loss macro transition, NOT an infinite decimal Lychrel certificate and NOT a Lean proof.

## Candidate
Let H0(k)=[9]++[14]^k++[5,5,5]++[4]^k++[13] in LSD-first pair coefficients, P0=H0++reverse(H0), k>=30 in the checked sample. Every pair coefficient belongs to 0..18. Reconstruct a true decimal seed: split each x in H0 into low=max(0,x-9), high=x-low, then take the least-significant-first digit list low++reverse(high). This realizes the given symmetric pairword with nonzero leading digit. The central odd 5s exclude palindrome at t=0.

The exact decimal pairword step is to normalize P by full ordinary base-10 carries (append leading carry if nonzero), then pair opposite resulting digits. For checked k=30,80,200,1000, six applications yield folded bulk run species 14 and 4 with the **same two lengths k,k as at t=0**. At k=200: t=0 pair runs (14,start1,length200),(4,start204,length200); t=6 (14,start5,length200),(4,start206,length200). The number grows from 810 to 813 digits while the junction absorbs the three digit increase without consuming either counter. This is a six-step budget-neutral *event*, not a true closed template edge.

At the NEXT clock, t=12 the two runs have lengths (k-5,k-3); at k=200 t=60 gives (163,182), t=120 (125,163), t=240 (46,124), and by t=480 there is no long 14-run. The absorbing bulks return by species in six steps, but their boundary words do NOT; this is the exact regenerative obstruction. A successful next construction must synthesize a phase-matched rewrite of the enlarged outer/junction region, not merely repeat the 555 block.

## Search and independent controls
The exhaustive fixed-scope 19^3 scan at k=50 fixes the two bulk letters (14,4), exterior endpoints (9,13), and all three junction coefficients in 0..18. Of 6859 words, 6744 retain two >=k/2 ordered long runs and at least one odd pair coefficient through the six-step clock. Exactly four retain BOTH original maximum run lengths at t=6: (5,5,5), (5,5,14), (5,14,5), (5,14,14). This count is relative to each candidate's *actual initial run lengths*, including any extension by junction digits; simply comparing to k would falsely count four more.

Independently from the pairword normalization, relay3.py computes actual unbounded Python integers at every step via decimal-string reversal and addition, recomputes all pair coefficients from their digits and asserts exact equality with the propagated pairword. It also checks actual decimal nonpalindromicity and odd-pair guards. All t=0..T states pass for (k,T)=(30,90),(80,240),(200,500),(1000,500), with minimum one odd pair. These are finite tests, not a universal all-k statement.

Reproduce from repo root: python3 calculation/new_structures/agent-X01/scan_3core.py and python3 calculation/new_structures/agent-X01/relay3.py. Data summary: calculation/new_structures/agent-X01/relay3.json. Full repository verify.py --changed was unavailable without a local GitHub checkout. No Lean sources are introduced.

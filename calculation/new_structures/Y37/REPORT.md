# Y37 report: P8 REC0 emitter cost refund, variant 3/4

**Status: PARTIAL (5/5 owned rotations exhausted; no refund found).** The global emitter/recharger problem remains open. This is a scoped all-width endpoint result that redirects the next search, not a finite-survival claim and not a decimal Lychrel certificate.

## Exact result

For the canonical T14 source H=B W^q E J V_s^k with E[9]=10, J=(18,0,1,1), C=(5,5), and q,k>=20 independently, Y37's ordered ledger entries 3,7,11,15,19 correspond to V_s rotations s=2,6,10,14,18. For every owned s, the 160-step endpoint is

H' = B W^(q-1) J'_s V_s^(k-8) D'_s, centre C'_s,

with |J'_s|=164 and |D'_s|=80. Centres are (6,6), (2,2), (2,2), (4,4), (9,9) in shift order. The checker emits the complete literal J'_s,D'_s words and hashes into daughters.json.

## Evidence and all-width scope

verify_rotation_shard.py performs actual unbounded-integer additions n+reverse(n), reconstructing each folded pairword from decimal digits. For each owned rotation it checks full-pairword insertion identities at all 161 states t=0..160 for one W insertion at cut 239, one V_s insertion at cut 663, and the commuting double-insertion square at cuts 239/683. The inserted blocks return to W and V_s at t=160. All four anchor seeds have the same true (10)^80 overflow clock and no palindrome in the checked interval. The generic symmetric paired-insertion lemma then lifts the endpoint to all independent q,k>=20.

The independent integer controls include 45 q,k pairs across diagonal widths 20,40,80,160 and mixed pairs (20,40),(40,20),(23,26),(80,160),(160,80). All five rotations give q_out=q-1, k_out=k-8, collar length 244. The checker also reproduces T14's shift-7 t=80/160/240/320 ledger at q=k=20,40,80,160. No Lean verification is claimed.

## Exact remaining lemma

The known shift-7 emitter already has q+1,k-4,c+80 after 80 steps. A second 80-step edge that keeps q fixed and restores collar length must gain five V copies and shrink the collar by 80, while restoring the exact physical seam/centre and both carry ports. T14's actual second edge instead has q fixed, k-4, collar +100, and centre (2,2)->(10,10). The next useful search is a genuinely different phase-dependent seam/recharger, not another E/J edit scan.

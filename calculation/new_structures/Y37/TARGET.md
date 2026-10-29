# Y37 target

Let B and W be the rooted p8/rec0 phase-0 rows; let R0 be phase 0 of the second 20-cell SCC cycle. Define V_s = rotate_left(R0,s) and the canonical T14 source H = B W^q E J V_s^k, with E=W except E[9]=10, J=(18,0,1,1), centre C=(5,5), and independent q,k>=20.

The ordered emitter ledger is the 20 rotations s=0..19. Y37 owns one-based entries i=3 mod 4, so s={2,6,10,14,18}. The target was a distinct physical W emitter or cross-epoch refund in this slice.

Exact scoped endpoint found for each owned s:

H' = B W^(q-1) J'_s V_s^(k-8) D'_s, centre C'_s, after 160 genuine reverse-add steps. The fixed collars have lengths |J'_s|=164 and |D'_s|=80; their literal words are generated into daughters.json by verify_rotation_shard.py. This is an all-independent-width endpoint lift, not a global no-go and not a Lychrel certificate.

Remaining repair target: from the known shift-7 T14 t=80 intermediate, a second 80-step edge that keeps q fixed and restores the original collar length must have Δk=+5 and Δc=-80. It must also restore the exact seam, centre, two carry ports, and phase clock. The actual second edge has Δk=-4, Δc=+100, centre (2,2)->(10,10).

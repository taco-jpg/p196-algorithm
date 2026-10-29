# AC40 phase-7, six-coefficient junction endpoint census

**Label: COMPUTED (exact finite reference-width cell); all-time T* return remains UNDECIDED.**

## Exact scope

Canonical rooted decimal p12/m9 exterior at clock phase 7 (0-based):
`B7=(5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17)` and `W7=(11,9,12,2,9,2,4,0,17)`.
For each `J=(0,j1,j2,j3,j4,j5)`, `j_i in 0..18`, take U=(9,0,18), C=(4,4) or C=(4,14,4), q=14 and k=100. Initial palindromic pairword is `P=B7++W7^q++J++U^k++C++reverse(B7++W7^q++J++U^k)`, indexed least-significant first. It admits a positive decimal realization, and the target after exactly 120 decimal reverse-and-add steps is the same P with k=105.

## Outcome

See the machine-readable 25-block summary below. All **2 * 19^5 = 4,952,198** concrete endpoint tests are exact and unpruned (two palindromic centres, all junction continuations with J[0]=0). Every required return has target coefficient **9 at index 137**, because `137-34=103` and `W7[103 mod 9]=W7[4]=9`. The enumeration checks that the physically computed endpoint coefficient at site 137 is never 9. Therefore **no tested initial pairword returns** after 120 steps. This is a completed subcell of the 1.41-billion-J/U six-site phase-7 problem, NOT an exclusion for all U, all J[0], or all palindromic centres.

## Soundness of the engine

Given a palindromic pairword `P_i=d_i+d_(n-1-i)`, `n+reverse(n)=sum_i P_i*10^i` holds exactly. At each step `exhaust.cpp` normalizes all coefficients LSD-first with carry `c_{i+1}=floor((P_i+c_i)/10)`, appends the final leading carry if any, and pairs the resulting decimal digit list with its reverse to obtain the successor pairword. Induction gives the actual decimal orbit for all 120 steps. The index-to-junction decode is a bijection `0..19^5-1 -> (j1,...,j5) in {0..18}^5`. No strict intermediate W9 preservation, odd-centre-only mod-11 filter, probabilistic pruning, or inferred midpoint locality is used. Each input is realizable because all coefficients are in 0..18, B7[0]>0, and the odd-length centre midpoint is even.

`independent.py` separately realizes ordinary Python integers and applies `n += int(str(n)[::-1])` for 120 steps. This is independent of the C++ pairword recurrence, and its first mismatch and clock agree for 100 width/cap controls, including (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640). Independent tests are spot checks, NOT an independent exhaustive enumeration.

## Reproduce

From repo root:

```sh
g++ -O3 -std=c++17 -fopenmp calculation/new_structures/AC40/exhaust.cpp -o /tmp/ac40-exhaust
for i in $(seq 0 24); do a=$((100000*i)); b=$((100000*(i+1))); [ "$b" -le 2476099 ] || b=2476099; /tmp/ac40-exhaust "$a" "$b" 5; done
python3 calculation/new_structures/AC40/independent.py
```

A completed `CELL` claim means only the exact fixed-centre, reference-width domain above. Applying T12 to wider widths would additionally require proving its protected-cut/reset-cone premises for this predicate. A negative finite cell does not furnish the periodic repair, growing seam, or positive all-time base-10 Lychrel certificate.

## Completed census data (25 disjoint 100,000-J chunks)

- Junction identifiers enumerated: `0..2476098` inclusive, with exact base-19 expansion `j1..j5`; all 2,476,099 distinct J.
- Physical 120-step endpoint computations: **4,952,198**, including both fixed centres.
- Required endpoint coefficient at LSD index 137: **9**. Actual histogram:
  `{3:223490, 7:763102, 10:315118, 11:2046788, 15:546650, 16:462312, 17:594738}`.
- Count at site 137 equal to 9: **0**. Count with non-30 total overflows: **0**.
- Source site-136 equal to required value 2: **3,965,606**; this weaker site alone does not exclude all candidates.
- Total C++ compute time reported across 25 chunks: **350.26 seconds** (five OpenMP threads).
- SHA256 of concatenated `chunk_00.json` ... `chunk_24.json` (newline retained): `463a8ff1eb4a5fa4a8f6fd15c3c6e0ba38923b9f59737d3f13bd52930580109d`. Raw 25 chunks are local ephemeral computations, not part of the commit; reproduce with the commands above. No input was pruned.

**Exact missing-lemma contribution:** this establishes a completed, independently spot-validated physical reference-width obstruction for one entire first-symbol slice of `PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH` in phase 7, restricting any fixed-seam T* candidate to other slices, U words, or centres. It does NOT produce a positive growth-cycle certificate or prove a universal all-time no-go.
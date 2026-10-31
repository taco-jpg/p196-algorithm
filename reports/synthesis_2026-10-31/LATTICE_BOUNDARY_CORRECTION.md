# Omitted physical edge in the old lattice-wall graph

Recovered in the 2026-10-31 synthesis audits, then independently reproduced during publication using literal decimal integers 和 a separate schoolbook-carry calculation.

**Status: COMPUTED physical counterexample to completeness of the old graph; PAPER PROOF scope correction. No stationary cycle or decimal Lychrel certificate follows.**

## Exact omitted edge

Use phase-0 B34/W9 from [lat_p12m9.txt](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt). Set the zero-based cut to `c=79`. Let `A=B0++W0^5++[10,0,0,0,0]` 和 form the odd symmetric pairword `P=A++reverse(A[:-1])`. Split mirrored coefficients into legal decimal digits, with an even midpoint.

| Quantity | Exact result |
|---|---|
| Source / successor decimal lengths | 167 / 168 |
| Actual overflow | 1 |
| Successor coefficients below cut 79 | Exactly `B1++W1^5` |
| Two defect coefficients | `(10,0) -> (6,1)` |
| Actual descending carry at cut | 1 |
| Old nominal bulk carry | 0 |

In [latcell2.py](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/hybrid_centres/latcell2.py), the unconditional test

```python
if (1 if v0 + din0 >= b else 0) != G[t]: continue
```

rejects the genuine edge. With `v0=10,v1=0`, the descending carry out of `v0` equals 1, whereas the periodic bulk requires `G[0]=0`. Nevertheless all lower lattice coefficients remain exact after the physical step.

At overflow, the mirror digit shifts by one position. A non-nine coefficient below the cut can reset the carry discrepancy while its changed digit contributes to the first defect cell. Therefore preservation of the lower lattice does 不 imply unconditional equality of the two cut carries.

## Scope requiring correction

The lattice-wall claims in [HYBRID §7b](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/hybrid_centres/HYBRID.md) cannot obtain a universal physical exclusion solely from emptiness of the old under-approximating graph.

The existing [corrected boundary implementation](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_check.py) requires nominal descending-carry agreement only when the overflow equals zero **or** the preceding lattice coefficient equals 9. Its separate 400-digit p8 example records the same mechanism.

- The 167-digit example establishes a missing physical edge, without establishing a stationary wall cycle.
- The neutral-nine wire still requires complementary carries; a carry discrepancy propagates through nines.
- The newer [EdgeRelaxW9NoCentre](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/results/EdgeRelaxW9NoCentre.md) uses a different physical relation 和 retains its own bounded-centre scope. The old-graph defect does 不 refute that later result.
- Moving/growing interiors 和 physical root reachability remain separate obligations.

## Standalone reproduction

The following Python arithmetic ran successfully during publication. The whole-integer calculation 和 independently calculated carry vector agreed; a separate JavaScript BigInt implementation also agreed.

```python
B0=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
B1=[1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5]
W0=[5,18,4,8,1,15,4,0,5]
W1=[10,14,13,12,9,7,10,4,5]
half=B0+W0*5+[10,0,0,0,0]
P=half+half[-2::-1]
d=[0]*len(P)
for i in range(len(P)//2):
    d[-1-i]=min(9,P[i])
    d[i]=P[i]-d[-1-i]
d[len(P)//2]=P[len(P)//2]//2
n=int(''.join(map(str,d[::-1])))
s=n+int(str(n)[::-1])
e=list(map(int,str(s)[::-1]))
Q=[x+y for x,y in zip(e,e[::-1])]
c=[0]
for x in P:
    c.append((x+c[-1])//10)
assert (len(str(n)),len(str(s)))==(167,168)
assert Q[:79]==B1+W1*5
assert (P[79:81],Q[79:81])==([10,0],[6,1])
assert c[len(P)-79]==1
assert W0[0]==5  # nominal descending carry resets to 0
```

The publication adds documentation 和 small Python controls. No Lean source changed; no fresh Lean verification claim.

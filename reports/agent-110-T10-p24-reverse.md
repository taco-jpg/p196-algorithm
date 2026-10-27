# Agent 110 — Independent backward exterior closure for the P24 target

## Scope 和 attribution

**PAPER PROOF + COMPUTED; no new Lean theorem.** This report concerns exactly

```
base = 10
e = 010100110100101011001011
g = 110001001000110001001000
```

The backward construction excludes a finite exterior B return after these
24 phases, at every spatial width 和 with arbitrary natural exterior trims.
The independent closure audit passes as recorded in Section 4.
Joint rotations describe the same cyclic problem. A return after 24k phases,
k>1, is a different problem; no multi-lap, other-driver, or global decimal
impossibility is inferred.

Agent 101 owns the actual P24 center target, with
`C0=[9,14,13,18,13,14,9]`, `v=100001000000100001000000`.
Agent 117 owns the primary exterior lift/inverse work
([PR409](https://github.com/taco-jpg/p196-algorithm/pull/409));
Agent 108 owns the separate forward block-MDD engine
([PR405](https://github.com/taco-jpg/p196-algorithm/pull/405)).
Their stronger completed result excludes **every e** for this particular g.
This work supplies a different backward construction 和 a separately checked
fixed-e invariant; it does not reattribute their discovery.
Agent 4 retains the broader SQ5 census. Agents 106/116/111, 109, 和 115 retain
the distinct regular-language, bounded-width/all-lap, 和 two-lap scopes.

The common-width reduction credits Agents 7/109/107; Agent 114's subsequent
registered formalization is [PR400](https://github.com/taco-jpg/p196-algorithm/pull/400).
The positional exterior equations are those of the unchanged baseline
`calculation/neutral_band/structure/bauto.cpp` 和 Python mirror.
Correlated decision-diagram motivation credits Agents 108/118; this reverse
implementation derives its own tiles 和 imports none of their search code.

## 1. Reduction from natural trims to fixed width

Put h=b−1, 和 let F_t be the raw exterior map with incoming reverse carry
1−e_t. Neutral suffix padding satisfies

\[
F_t(Bh^a)=F_t(B)h^a.
\]

Normalization through the appended h's preserves e_t 和 the reverse carry;
the added forward/reverse digits are h(1−e_t) 和 he_t. This also preserves
g_t, including the overflow shift. For a closed original exterior itinerary
`F_t(B_t)=B_(t+1) h^(u_t)`, choose M>=max(1,max_t|B_t|) 和 a_t=M−|B_t|.
The length identity gives a_(t+1)=a_t+u_t−g_t, hence

\[
F_t(B_t h^{a_t})=(B_{t+1}h^{a_{t+1}})h^{g_t}.
\]

Thus all words have width M 和 all new trims are u'_t=g_t. Empty original
words are covered: their padded first coefficient is h>0. Conversely, a
fixed-width witness is an allowed original itinerary. A known decimal p11
control has original u=[0,0,0,0,0,0,0,4,0,0,0], exercising trims above one.

## 2. Exact spatial relation 和 boundaries

At a cut record the complete temporal state
`(L_t,H_t,Y_t at g_t=1)`: low forward carries, high reverse carries, 和 the
lagged reverse digit needed at overflow. The physical source is

\[
S=(0,g,1),\qquad T_e=(e,1-e,he|_{g=1}).
\]

For column coefficients x_t in 0..2b−2, old cut (L,H,Y), 和 new cut
(L',H',Y'), the literal equations are

\[
L'_t=\lfloor(x_t+L_t)/b\rfloor,\quad
H_t=\lfloor(x_t+H'_t)/b\rfloor,
\]
\[
d_t=(x_t+L_t)\bmod b,\quad r_t=(x_t+H'_t)\bmod b,
\quad x_{t+1}=d_t+\begin{cases}Y_t&g_t=1,\\r_t&g_t=0.\end{cases}
\]

At overflow additionally Y'_t=r_t. Require x_24=x_0. The FIRST relation
from S requires **every** x_t>0; interior columns may contain zero.
Positive-FIRST successors, rather than the unqualified source tuple, are
intersected with backward reachable states. Every accepted path reconstructs
all B_t columns, terminal carries, overflow suffixes, 和 raw exterior edges.

The eight overflow blocks start at [0,1,5,8,12,13,17,20], with lengths
[1,4,3,4,1,4,3,4]. A block of length d has symbol
`Lbits | (Hbits<<d) | (Y<<(2*d))`, in chronological bit order.
Every decision-diagram level is explicit. There are no dropped carries,
independence approximations, or skipped variables.

Given a target block, the primary inverse derivation conditions on the
first overflow equation, enumerates entering coefficients/old low carries
和 old lag digits, then propagates coefficients forward in temporal order,
checking every target carry. The inversion is in the spatial direction.
Boundary cases x=b−1 are retained. Exact
preimage recursion remembers the target MDD node, current coefficient port,
和 initial coefficient port; the final port must equal the initial one.
Equal predecessor labels are joined with exact structural union, retaining
the complete correlated target path. Hash interning compares full level/arc
vectors after a hash match; a hash match alone never establishes equality.

## 3. Complete backward computation

Let R0={T_e}, R_(n+1)=Pre_INTERIOR(R_n). The all-h column supplies T_e a
self-loop, so these sets are nested. The engine also checks exact inclusion
`union(old,new)==new` after every complete image. At canonical-root equality
the finite represented set is a true fixed point, with no depth assumption.

| Depth | Complete R_n size | Newly added |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 2,304 | 2,303 |
| 2 | 62,001 | 59,697 |
| 3 | 259,645 | 197,644 |
| 10 | 25,170,422 | 4,669,564 |
| 20 | 95,866,156 | 7,384,504 |
| 40 | 206,295,476 | 28,419,952 |
| 60 | 431,825,864 | 6,863,216 |
| 80 | 704,606,242 | 922,692 |
| 81 | 705,153,218 | 546,976 |
| 82 | 705,175,506 | 22,288 |
| 83 | 705,176,594 | 1,088 |
| 84 | 705,176,634 | 40 |
| 85 | Same exact root as R84 | 0 |

The complete positive-FIRST set has 64 states, all outside R84.
The primary run finished EXHAUSTED/exit0 in20.223176s, peak714,004KiB:
855,863 allocated MDD nodes, 50,951 inverse tiles, 189,727,839 charged
operations, 8,525,214 image-cache entries, 和 458,990 union-cache entries.
All arithmetic counts are exact unsigned128, with a checked addition 和 an
input guard bounding the complete cut-universe cardinality by2^120.
IDs are immutable/nonreused; persistent preimage memoization is exact.

The exported finite-state certificate contains only the root-reachable DAG:
301,476 nodes including reject/accept, root301475, 29,181,727 bytes.
SHA256: `425e468184ef79c6cd79e1cacb96a4547e27649ca9074c964162fea9c6d7b503`.
This is scientific state-set data, regenerated below, not an execution log.
Search flags, counts, hash values, 和 fixed-point metadata are untrusted by
the separate checker.

## 4. Independent closed-superset certificate

For any supplied set K, it suffices to check

\[
T_e\in K,\qquad \operatorname{Pre}(K)\subseteq K,\qquad
\operatorname{FIRST}(S)\cap K=\varnothing.
\]

Induction gives every finite predecessor of T_e in K; hence no positive
FIRST path reaches it. Minimality, claimed search depth, exact R_n sizes,
generator canonicalization, 和 search-history metadata are unnecessary.

The Python checker independently enumerates local coefficient trajectories
**forward in time conditioned on the target block**, using literal integer
carry equations. Its product search follows a target path in K 和 a source
membership path, keeping both coefficient ports. A closed path ending with
source rejection is exactly a witness to Pre(K) not contained in K. It
validates explicit node levels/labels/children 和 counts with Python integers.
Missing source edges enter an absorbing reject state. Memo keys encode the
complete product state; no merely numerical count comparison is used.

**Full independent audit: PREDECESSOR_CLOSED_NO_EXTERIOR, exit0.**
It verifies all three conditions, independently recounts705,176,634 states,
和 finds FIRST64 disjoint. Completion uses7,824,347 product states, 2,525
local tile queries, 和130,963,184 operations;64.587204s including input
parsing/validation, peak1,115,600KiB. No resource limit is reached.
An independently enumerated unconstrained forward table agrees on14,492
target symbols/96,140 tiles, including **all** decimal targets for every
block length1,3,4 used here. Further checks compare73 FIRST languages/208
states, 383 known path blocks, ten terminal encodings, 和155 arbitrary
small set diagrams:67 predecessor-closed sets 和88 independently replayed
violations. These67 closed sets are not claimed as67 exclusion certificates.
A different checker exhausts512 subset queries over the full base2/P1 cut
universe, replaying312 returned counterexamples. Ten known-positive rotated
drivers exercise missing predecessors 和 true FIRST overlaps. All44 malformed
schema cases reject, two untrusted metadata/cardinality controls pass, 和
five in-process/eight real CLI cap/input-error controls pass, normal 和 -O.
The initial unoptimized500-million-operation audit correctly returned
UNDECIDED/exit2 after98.209306s. That capped attempt supplied no exclusion.

## 5. Reproduction 和 independent controls

From the repository root:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  calculation/agent-110/p24_reverse_mdd.cpp -o /tmp/agent110-p24-reverse-mdd
/tmp/agent110-p24-reverse-mdd --layers 1000 --seconds 30 \
  --memory-mib 1024 --nodes 1000000 --operations 200000000
python3 calculation/agent-110/p24_reverse_reference.py --selftest --seconds 180
python3 -O calculation/agent-110/p24_reverse_reference.py --selftest --seconds 180
python3 calculation/agent-110/p24_reverse_reference.py --selftest \
  --mdd /tmp/agent110-p24-reverse-mdd --seconds 180
python3 calculation/agent-110/p24_reverse_controls.py \
  --mdd /tmp/agent110-p24-reverse-mdd \
  --reference calculation/agent-110/p24_reverse_reference.py --seconds 45 --guards
python3 calculation/agent-110/p24_reverse_certificate_controls.py --seconds 120
python3 calculation/agent-110/p24_certificate_controls.py
python3 -O calculation/agent-110/p24_certificate_controls.py
```

The primary command above returns EXHAUSTED with the exact counts in Section3.
The explicit Python reference has separate inverse algebra. Its normal/-O
selftests pass26 drivers, 5,152 state/mode queries, 3,989 directed edges,
five source fixtures/40 integer B steps, 和 four cap-after-witness controls.
Against the MDD it compares **2,452 complete singleton preimage sets** across
19 supported small drivers 和19 complete FIRST sets, with no mismatch.
All complete P24 R0,R1,R2,R3 和 FIRST states agree, not merely their counts.
Reference R3 contains259,645 states in20.021814s, canonical SHA256
`cee9fe6bf09c255045be0904acaa4e837f44348f9de24ab3ba6788aa192f8a59`.
The full R3 set comparison can be repeated directly:

```sh
python3 - <<'PY'
import json, subprocess
ref=['python3','calculation/agent-110/p24_reverse_reference.py',
     '--export-layer','3','--states','400000','--seconds','180']
mdd=['/tmp/agent110-p24-reverse-mdd','--export-layer','3',
     '--export-cap','400000','--seconds','60']
a=json.loads(subprocess.check_output(ref,text=True,timeout=190))
b=json.loads(subprocess.check_output(mdd,text=True,timeout=70))
if a!=b: raise SystemExit('full frontier mismatch')
print('PASS full R3',len(a))
PY
```

The third checker independently replays the actual C24: G=8,V=4,widths6/7,
和 C_(t+12)=18−C_t. It compares272 complete singleton inverse sets/2,428
states across both engines, covering136 known spatial columns. All ten B
positives reconstruct: base2/4/8/16/32 widths2; base26 width8; base11 width7;
base17 width29; decimal p11 width29; decimal p12 width53.
The eight nondecimal fixtures rejoin their original centers 和 pass complete
mirror cycleOK. Decimal fixtures remain B-only. Further controls cover24
padded full cycles/448 columns, 2,108 covariance cases including empty B,
3,432 local inverse cases, ten status controls, 和 four bad-coefficient cases.
All seven actual depth/operation/node/wall/memory/export/malformed guards
return UNDECIDED/exit2. The combined third run passed in15.427913s.

To regenerate only the finite-state certificate, discard progress records:

```sh
python3 - <<'PY'
import json, pathlib, subprocess
cmd=['/tmp/agent110-p24-reverse-mdd','--layers','1000','--seconds','60',
     '--memory-mib','1024','--nodes','1000000','--operations','250000000',
     '--dump-root']
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,text=True)
written=False
for line in p.stdout:
    if '"type":"CERTIFICATE"' in line[:100]:
        pathlib.Path('/tmp/agent110-p24-reverse-closure.json').write_text(line)
        written=True
    elif '"type":"RESULT"' in line[:100]:
        print(line.strip())
if p.wait()!=0 or not written: raise SystemExit('certificate generation incomplete')
PY
python3 calculation/agent-110/p24_reverse_certificate.py \
  /tmp/agent110-p24-reverse-closure.json --seconds 1500 --memory-mib 3072 \
  --operations 2000000000
```

Compiler warnings are empty. UBSan with libstdc++ assertions reproduces
P24 R3 和 the base17 width29 positive with empty diagnostics.
Literal `python3 tools/verify.py --changed`: **ALL CHECKS PASSED**,5217 Lean
files/301 projects;0 changed Lean modules 和0 endpoints to audit.
All files are new Agent110-owned paths; no baseline,
README, RESULTS, registry, or other agent source is modified.

The result is computational exterior exclusion for this fixed24-phase
driver, supported by the paper reduction. No Lean exclusion theorem or
decimal cycleOK certificate is claimed. General repeated-lap feasibility,
other g streams, 和 the complete decimal neutral-band route remain open.

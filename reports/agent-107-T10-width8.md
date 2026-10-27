# Agent 107 — independent width8 exterior-cycle verification

**Status: PAPER PROOF + COMPUTED independent corroboration.**
No decimal exterior cycle has every canonical width at most8, at any period
or natural trim schedule. Equivalently, every such cycle has a phase of
canonical width at least9. Agent109 retains primary width8 discovery credit.
**Decimal width8 color payload: 365,674,947 bytes; queue payload: 0 bytes.**
These are exact storage calculations, not measured peak memory.

Coordination: [T10.B-width8-charge-independent claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433263203).
The full independent traversal completed with every vertex finished, exit0,
and an empty cycle witness. The computation is not a Lean negative theorem.

## Attribution 和 precise scope

Agent109's [primary PR390](https://github.com/taco-jpg/p196-algorithm/pull/390)
reports an exact digit-MDD sink-peeling exclusion at width8. Its report 和
engine were inspected at `f2d88bc915d04694695783a5b1cd4a4f124b20f1`.
No transition-bridge or sink-termination defect was found. Agent9 retains the explicit
bounded-width census in [issue295](https://github.com/taco-jpg/p196-algorithm/issues/295).
The present assignment independently checks the same cycle question using
whole-word arithmetic 和 a queue-free functional-graph traversal.

The mathematical ingredients credit Agent7's neutral-padding 和
canonicalization work, including [PR315](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [PR326](https://github.com/taco-jpg/p196-algorithm/pull/326), 和 the prior
Agent2/3/5 alternating-moment algebra. Agent107's
[PR363](https://github.com/taco-jpg/p196-algorithm/pull/363) supplies the
strong neutral exterior residue filter. Agent108's
[PR360](https://github.com/taco-jpg/p196-algorithm/pull/360) supplies its
decimal Lean bridge under the stated positive-overflow hypothesis.
The all-base reductions below are PAPER PROOF; no new Lean theorem is claimed.

The independent engine reconstructs transitions from exact coefficient
normalization. It imports none of Agent109's MDD transition, preimage, or
sink-peeling code. It depends only on the ranker in
[PR383](https://github.com/taco-jpg/p196-algorithm/pull/383), its PR base.
Agent114 separately reports a Lean common-width bridge in
[PR400](https://github.com/taco-jpg/p196-algorithm/pull/400); the present
engine 和 computation are not Lean-verified.

## 1. The autonomous exterior map

Fix `b>=2`, a width cap `M>=1`, 和 put `q=b-1`. A legal exterior B is a finite word over
`0..2q`, with a positive first coefficient when B is nonempty. Coefficients
are listed least significant first. Empty B is initially permitted.

Let `norm_b(W,c)` return the normalized digits 和 exit carry. Set

\[
(D,e)=\operatorname{norm}_b(B,0),\qquad
(R,g)=\operatorname{norm}_b(B^{\rm rev},1-e),\qquad x=q(1-e).
\]

The raw exterior map is

\[
F_b(B)=
\begin{cases}
D+R^{\rm rev},&g=0,\\
(D\mathbin{++}[x])+([1]\mathbin{++}R^{\rm rev}),&g=1,
\end{cases}
\]

where `+` denotes coordinatewise addition. Its length is `|B|+g`.
A legal exterior edge is an exact equality

\[
F_b(B_t)=B_{t+1}\mathbin{++}q^{u_t},\qquad u_t\in\mathbb N. \tag{1}
\]

Thus the unrestricted trim choice is explicit. This is only the B side;
a B cycle still needs a compatible center before it can be a certificate.

## 2. Neutral suffix covariance

Write `P_a(B)=B++q^a`. A neutral coefficient transmits either entering
carry unchanged. Put `y=qe`, so `x+y=q`.
Normalizing `P_a(B)` produces `D++x^a` with exit e; normalizing its reversal
with entry `1-e` produces `y^a++R` with exit g. Therefore e 和 g are unchanged.

If g=0, the two raw arms acquire suffixes `x^a` 和 `y^a`.
If g=1, use `x^a++[x]=[x]++x^a` to obtain the same suffixes after
the original overflow arms. Coordinatewise addition proves

\[
F_b(P_a(B))=P_a(F_b(B)). \tag{2}
\]

This identity holds for arbitrary nonnegative a, including a=0.

## 3. Closed cycles with ordinary widths at most M

Suppose (1) forms a nonempty closed cycle 和 `n_t=|B_t|<=M` at each phase.
Length balance on each edge gives

\[
n_{t+1}=n_t+g_t-u_t.
\]

Pad phase t by `a_t=M-n_t`, obtaining `V_t=P_(a_t)(B_t)` of length M.
Equation (2) gives

\[
F_b(V_t)=B_{t+1}q^{u_t+a_t}
        =V_{t+1}q^{g_t}, \tag{3}
\]

because `u_t+a_t=a_(t+1)+g_t`. Hence the padded cycle uses exactly
`u_t=g_t`: no trim on a non-overflow edge 和 one neutral suffix coefficient
on an overflow edge. The driver streams 和 coefficient bounds are unchanged.

Conversely, a closed length-M sequence satisfying (3) is already a legal
exterior cycle of (1). A nonempty closed walk is sufficient: if padding
identifies some phases, the resulting closed walk still contains a cycle.

## 4. The stronger canonical-width scope

Let `core(B)` remove the maximal neutral suffix from B. Suppose only
`|core(B_t)|<=M`; actual phase widths may exceed M. Choose

\[
N=\max\{M,\max_t|B_t|\}.
\]

First pad every phase to width N. Section3 gives a closed map with trim g.
Every padded phase equals `core(B_t)++q^(N-|core(B_t)|)`, so it has a common
suffix `q^k`, where `k=N-M`. Write the padded phase as `V_t++q^k`, with
`|V_t|=M`. Applying (2) to its edge gives

\[
F_b(V_t)q^k=V_{t+1}q^kq^{g_t}
          =(V_{t+1}q^{g_t})q^k.
\]

Right cancellation yields (3). Carries 和 overflows are preserved when the
common suffix is removed, by the same normalization identities.

Section5 excludes an empty canonical core (an empty or entirely neutral exterior),
so these V words have positive first coefficients. Conversely, every
length-M cycle has canonical widths at most M. Thus the fixed-width map
decides the existence of B cycles whose canonical widths remain at most M,
with arbitrary periods 和 natural trim counts in the original representation.

## 5. Residue restriction 和 exact domain size

For `A(B)=sum_j((-1)^j*B_j)` 和 `s(B)=(-1)^|B|`, put

\[
R_b(B)=A(B)-s(B)\pmod{b+1}.
\]

PR363 proves that R doubles on a non-overflow edge 和 becomes zero on an
overflow edge; every permissible neutral suffix trim preserves R.
Every legal closed exterior cycle contains an overflow: empty B emits g=1;
otherwise, on a non-overflow edge with a nonempty successor, its positive
first coefficient changes from x to `2x+h`, with `h` a carry bit. A closed
cycle consisting solely of these strict increases is impossible. Consequently its
phases 都 have R=0, 和 the zero class is forward invariant.

The exactly suffix-invariant integer charge is
`J_b(B)=A(B)-1` at even length 和 `A(B)-b` at odd length.
It satisfies `J_b(B)=R_b(B) mod(b+1)` 和 `J_b(q^n)=J_b([])=-1`.
Thus empty 和 entirely neutral words cannot occur on a closed cycle.

The traversal domain consists exactly of positive-head words of length M
with R=0. If N_M counts the legal zero-residue words of widths at most M,
then the domain size is `N_M-N_(M-1)`. The cap-stable rank helper represents
this domain by the contiguous global-ID interval `[N_(M-1),N_M)`.
The neutral padding in Sections2–4 is distinct from the helper's indexing
convention: actual transitions always use the decoded coefficient word.

For decimal M=8,

\[
N_8=1,543,960,696,\quad N_7=81,260,909,\quad
V=N_8-N_7=1,462,699,787.
\]

Two bits per vertex occupy `ceil(V/4)=365,674,947` bytes. No FIFO is needed.
This excludes indexing tables, word buffers, a bounded path buffer, 和 runtime overhead.

## 6. The partial function 和 traversal proof

At a length-M state, compute F 和 g exactly. If g=0, its full output is the
only successor. If g=1, a successor exists exactly when the last coefficient
is q; remove that coefficient. Equation (3) supplies no additional choice.
An unexpected coefficient bound, length, residue, rank, or integer-overflow
failure must abort the check, not silently discard an edge.

The successor head remains positive: at g=0, `x+h<b` gives head `2x+h>0`;
at g=1, the head is `(x mod b)+1>0`. Trimming the last g coefficients leaves
M>=1 entries, so preserves this head. The zero residue is forward invariant.

Use two bits to encode white, gray 和 black. The unused fourth value is an
error state. Before each new walk, every previously explored path is black;
no gray vertex remains from an earlier completed walk.

Start at a white vertex 和 follow the partial function, marking newly seen
vertices gray. Reaching an undefined successor or a black vertex completes
an acyclic path. The implementation records at most 65,536 IDs (524,288 bytes)
to accelerate blackening. Longer paths are replayed from their start, marking
gray vertices black; `--path-cap 0` selects pure replay. No unbounded path stack
or FIFO is required. Every completed path must blacken exactly its new vertices.

Reaching gray means reaching an earlier vertex of the current walk, because
previous walks contain no gray vertices. The segment between its two visits
is an actual directed cycle. This handles self-loops as well as longer cycles.

If traversal finishes with V black vertices 和 no gray encounter, the
entire domain is acyclic. Sections3–5 then transfer this negative result to
the stated exterior-cycle scope. Resource/replay limits give UNDECIDED (exit3);
input, representation, or internal failures give ERROR (exit2). External interruption
may leave no record. None supports a negative. No longest path is computed.

## 7. Independent controls 和 computed result

The final source passed all eight independent tests in 10.081 seconds:

- Whole-integer normalization reconstructs 17 original variable-width graphs,
  including every legal natural trim, empty words 和 nonzero-residue states:
  9,511 states / 6,492 arcs, with 1,087 exact fixed-width adjacency comparisons.
- Eight source certificates / 56 edges produce 16 padded cycles / 112 exact
  integer checks at maximum supplied ordinary width 和 that width plus one.
  Native replay covers 100 edges; the remaining 12 base17 edges at widths29/30
  exceed the ranker's uint64 range 和 are explicitly checked only by integer arithmetic.
- Positive exterior cycles, empty domains, acyclic graphs, explicit cap/input
  guards 和 zero-buffer replay pass. Deadline0 is exercised; later deadline
  checks are source-reviewed. No generic injected toy-graph test is claimed.
- An independent meet-in-the-middle count verifies the width8 domain size.

Agent109's primary graph contains all `18*19^7=16,089,691,302` positive-head
width8 words. Our restricted graph contains 1,462,699,787 words. The residue
theorem equates their cycle-existence questions, not their state counts.
The primary report's `S36=14, S37=empty` longest-path result is not rechecked here.

Exact source identities:

```text
charge_graph.cpp: 729a9a209526a9d4d0536089ee8a9fa30b135ed8c2eb56993782cab504fa0771
charge_index.hpp: ca3c29df8d4629e1f4621c1b4d0884938c81953be8f4eb5b8f6e736db4d8b5fa
```

Commands from the repository root, with the unchanged PR383 header:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Wpedantic calculation/agent-107/charge_graph.cpp -o /tmp/agent107-charge-graph
python3 -O calculation/agent-107/test_charge_graph.py
python3 - <<'PY'
import json, resource, subprocess, time
def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))
start = time.perf_counter()
r = subprocess.run(['/tmp/agent107-charge-graph', '10', '8', 'census',
    '--seconds', '1150', '--memory-mib', '4096',
    '--state-cap', '1462699787', '--path-cap', '65536'],
    timeout=1200, preexec_fn=limits)
print(json.dumps({'exit': r.returncode, 'wall_seconds': time.perf_counter()-start,
    'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}))
raise SystemExit(r.returncode)
PY
python3 tools/verify.py --changed
```

Completed final-source pilots (all states visited 和 finished):

| Width | States | Edges | Exits | Engine seconds | Peak child KiB |
|---:|---:|---:|---:|---:|---:|
| 6 | 4,051,881 | 2,025,968 | 2,025,913 | 1.92247391 | 8,576 |
| 7 | 76,983,951 | 38,491,912 | 38,492,039 | 43.2660587 | 20,480 |
| 8 | 1,462,699,787 | 731,350,046 | 731,349,741 | 383.353148 | 358,656 |

All return `ACYCLIC`, exit0, with no fallback paths. Width7 wall time was
43.317614984 seconds; width8 wall time was 383.381710564 seconds.

The complete width8 output records:

```text
status=ACYCLIC reason=all_states_finished found_cycle=false witness=[]
total=visited=finished=successor_calls=1462699787
edges=731350046 exited=731349741 fallback_paths=0
color_bytes=365674947 planned_bytes=366281995
runner_exit=0 max_child_rss_kib=358656
```

The recorded source hashes match the final files. A preceding uncollected run
was explicitly stopped after its environment handle was lost; it contributes
no evidence. The completed rerun's structured result was retained independently
of the tool session. No timeout or resource cap was reached.

Actual `python3 tools/verify.py --changed`: **PASS**, 5,217 Lean files / 301
projects checked, zero changed Lean modules / audited endpoints. No center result,
decimal certificate, unrestricted-width exclusion, or longest-path claim follows.

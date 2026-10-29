# X17: a charge-controlled branching folded pump for decimal reverse-and-add

**Label: COMPUTED.** This is an exact, explicitly bounded *finite-horizon* folded digit-pair renormalization with a two-branch charge-controlled gate. It is not a base-10 Lychrel certificate, a closed invariant, a universal-length theorem, or a Lean proof.

## Folded pumping relation

Let `P_n` be the decimal palindrome of odd length `n` with least-significant-first reflected motif `88283583`. A central mask `m in {0,...,255}` adds digit `+1` at the off-centre places `floor(n/2)-k`, where `k=1,...,8` and bit `k-1` of `m` is set. Let `A_{n,m}(t)` be the exact decimal reverse-and-add orbit. For a canonical decimal digit word `d_0 ... d_{L-1}` (LSD-first), write its folded pairword as `F(d)=((d_0,d_{L-1}),...,(d_{floor(L/2)-1},d_{ceil(L/2)}))`, retaining the middle singleton separately when L is odd.

The positive folded-pump assertion for an orbit pair `(n,n+16)` and time t is that both canonical numbers have equal length parity and identical singleton centre (if any), and **the longer folded pairword is the shorter folded pairword with exactly eight pairs inserted at some cut**. This implies a precise digit-level correspondence, not merely a rough visual similarity or a hash collision. The cut can depend on t and mask unless a stronger uniform assertion is explicitly made.

## 108-state universal-mask pump and the first branch

Independent **Python arbitrary-precision integer** replays of **all 256 masks** at each of the two length pairs `(1001,1017)` and `(2001,2017)` establish this stronger assertion at every `t=0..107`:

- There exists a single cut `j_t` and a single fixed **eight-folded-pair insertion block**, independent of mask, such that the entire longer folded pairword is exactly `F_short[:j_t] ++ block_t ++ F_short[j_t:]` for each of the 256 masks.
- The **leftmost** such common cut `j_t` and the inserted 8-pair word are identical across the two *tested* length pairs for all 108 states; all 108 rows are recorded in `pump_left_108.csv`. At `t=107`, `j_t=61`, and the paired block is `45 90 90 45 54 09 09 54` (concatenated as `4590904554090954`).
- At `t=108`, the mask-independent *single-block* format fails, **but every mask still satisfies an exact individual eight-pair insertion**. The inserted band at the common cut `j=61` for `(2001,2017)` branches into precisely two values, determined *exactly* by the previously computed eight-bit charge function `F(m)` from `AgentX17ProgrammableChargeGate`:

| incoming differential carry `F(m)` | masks | inserted folded 8-pair band at t108 |
|---|---:|---|
| `0` | 86 | `09 09 09 09 09 09 09 09` |
| `1` | 170 | `00 00 00 00 00 00 00 00` |

This is a **constructive controllable band transduction**: eight initial central perturbation bits determine whether a large-width stable `09` paired band or a zero absorbing band is emitted, despite the completely uniform pre-gate insertion law. The exact 256-mask BDD in the previous result is therefore also a compact controller for this branching renormalization. The Python replay verifies the full folded word at `t=108` for every mask, not merely the eight-pair block.

## Later branching and collision measurements

An independent **C++ ordinary-decimal digit-vector** engine enumerates all 256 masks for each length pair and checks the exact individual folded-splice property on complete words at each step. It also groups concurrent masks by `(leftmost valid cut, eight-pair insertion block)` at every state, exposing a small state graph before collision.

- For `(1001,1017)`, **all 256** remain individually pumpable through `t=775`. First two cease to satisfy the fold-splice relation at **t=776**, and **none** satisfies it by **t=813**. The number of observed concurrent `(cut,block)` states is at most **4**.
- For `(2001,2017)`, **all 256** remain individually pumpable through **t=1601**; the first fails at **t=1602**, and **none** remains pumpable at **t=1667**. The number of observed concurrent `(cut,block)` states is at most **5**.
- At `t=108` there are two classes; at `t=111` there are three for the `(2001,2017)` pair, and at `t=118` up to five. Classes later coalesce, but no all-time bound or loop closure is asserted. All stated failures refer to the folded **insertion property**, *not* to palindrome encounters.

The bounded branching, exact full-digit pumping, and explicit formation of `09` versus `00` bands suggest a certificate **format** with a small phase/charge controller and rationally pumped folded exteriors. To become an infinite certificate, it still requires a proof of full-language closure, an indefinitely renewing band or nested regeneration, and a nonpalindrome witness preserved forever. The measured first failures show that simply extrapolating the current finite pump would be invalid.

## Reproduce and soundness boundary

`bash calculation/new_structures/agent-X17/pump_renewal_reproduce.sh` compiles the C++ exact digit-vector engine, runs all 256 masks for both length pairs out to and beyond collision, verifies recorded checkpoints and first-failure times, runs a Python bigint **all-mask** uniform pump through t107 for `(1001,1017)`, and separately verifies the complete 256-mask charge-controlled t108 folded-splice into the two specified blocks for `(2001,2017)`. `DEEP=1` reruns the more expensive Python `(2001,2017)` complete t0..107 uniform mask test. Code: `pump_fold.py`, `pump_gate.py`, `pump_partitions.cpp`, `pump_renewal_reproduce.sh`; data: `pump_left_108.csv`, `pump_gate_2001.csv`, `pump_partition_checkpoints.csv`, under `calculation/new_structures/agent-X17/`. The exact arithmetic engine, not a symbolic assumption, determines every digit. No full checkout/Lean or repository-wide verifier was available here.

### Additional complete-mask length controls (computed addendum)

The same exact C++ folded-splice test was independently extended to `(n,n+16)=(3001,3017)` for all 256 masks through `t=3000`, and to `(4001,4017)` through `t=3800` (still requiring equal central singleton). All 256 masks pump through **t=2425** and **t=3252**, respectively, before the first break at **2426** and **3253**; all insertion relations have failed by **2515** and **3352**. Concurrent `(leftmost cut, band)` classes never exceed **4** and **5** respectively. Full four-pair summary: `pump_multilength_summary.csv`. Run `EXTRA=1 bash calculation/new_structures/agent-X17/pump_renewal_reproduce.sh` to reproduce the additional n3001/4001 first/last failure and bounded-class checks. These four isolated finite lengths do not establish a universal length bound or infinite recurrence.
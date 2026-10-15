# Agent #109 — kernel-checked return certificates for the complementary template

Task record: `proofs/coordination/tasks/agent109-template-return-certificate.json`
(branch `p196/coordination`). Builds on
[`../template-step-bridge/`](../template-step-bridge/) (identity (8) and the
integer bridge).

**Status: LEAN-CHECKED conditional theorem (local fresh build, Lean 4.19.0
`6caaee842e94`). Not independently reviewed. No certificate instance is known,
searched for or claimed here; nothing about 196 follows.**

## Statement

The complementary-bulk note states, as a written conditional criterion, that a
returned finite interface with nonnegative gain in each gap and sufficient
within-cycle band lengths would make the first positive output of a canonical
realization an infinite-safe seed. This package makes that criterion a finite,
kernel-decidable certificate format with a proved soundness theorem.

A `Certificate` is a cyclic list of states `(c,B,A,C)` and `Link`s
`(j,j1,j2,k,lo,lo')`. `check cert = true` requires, at every index `i`
(successor `i+1 mod P`):

* `Phase c`, coefficients of `B,A,C` at most 18;
* the exact successor of identity (8) equals the next state after trimming:
  `2t_c = c'`, `B_r = B' ++ c'^j`, `A_r = c'^j1 ++ A' ++ d'^j2`,
  `C_r = d'^k ++ C' ++ d'^k` (`template_trim` proves these re-segmentations
  leave the template unchanged for every band length);
* `¬ StepPal c B A C` — the next integer is not a palindrome. `step_palindrome_template`
  proves this test is **exact and independent of the band lengths** (via
  `shape_palindrome_iff`: a nine-segment word with mirrored segment lengths is
  a palindrome iff its three finite blocks mirror);
* bounds `lo,lo' ≥ 2` with `lo_{i+1}+2 ≤ lo_i+γ_i+j+j1` and
  `lo'_{i+1}+2 ≤ lo'_i+γ_i+j2+k` (possible only if each cyclic gap gain is ≥ 0).

Proved (all in core Lean + Std; axioms `propext`, `Classical.choice`, `Quot.sound`):

* `Agent109.Cert.certificate_sound`: `check cert = true` and
  `pairWord n = template (st 0) G H`, `G ≥ lo_0`, `H ≥ lo'_0` ⇒ no
  `orbit (step n) k` is a palindrome.
* `Agent109.Cert.template_realized`: every admissible template (phase, bounded
  blocks, `C` mirrored with even middle, positive exterior, `g>0`) is the pair
  word of an ordinary integer.
* `Agent109.Cert.certificate_existence`: with `decide (Admissible0 cert H M)`
  (`C₀ = H ++ M ++ rev H`, `M` empty or one even entry, `B₀` empty or positive
  head) there is an integer with no palindromic iterate.
* `Agent109.CertCompat.certificate_isLychrel` and
  `certificate_existence_lychrel`: the same with the accepted
  `Lychrel196.IsLychrel (Lychrel196.step n)` and
  `Lychrel196.DecimalLychrelExistence`.

So a certificate found by any search becomes, after
`theorem cert_valid : check cert = true := by decide` (ordinary kernel `decide`,
demonstrated on a rejected toy certificate in `CertDemo.lean`), a kernel-checked
decimal Lychrel witness. Its premise is unsupplied: this is a conditional
theorem only.

## Tool and controls

`certificate_tool.py` (independent Python): exact successor, maximal trimming,
cycle detection (`iterate`), minimal feasible band bounds, a mirror of `check`
(`local_ok` per index), and `export`, which accepts either the `iterate` output
(`{"cycle","info"}`, converted with computed bounds) or an explicit
`{"states","links"}` certificate, re-checks it, and exits with status 2 and a
reason when there is no cycle, a palindromic step, a negative gap gain or a failed
check (`--unchecked` emits Lean that only evaluates `check`).
`test_certificate_tool.py` is the regression suite with independently established
expected outcomes (`tool_test_result.json`, also run by `certificate_tool.py
selftest`): CertDemo rejected for the B link, step palindromicity compared with
literal integer reverse-and-add at four band-length pairs, one-step links accepted,
every single mutation rejected with the expected reason, bound feasibility, and a
CLI round trip (`ExportDemo.lean`, which Lean evaluates to `false`). No valid
certificate is known, so no accepting whole-certificate case exists.
`CrossCheck.lean` evaluates Lean's `Br/Ar/Cr/γ/StepPal` on 1,000 random states
and compares them with the Python tool's values: 0 mismatches (compiled `#eval`,
a consistency control, not a proof). The Python formulas were separately checked
against literal integer reverse-and-add in
`../template-step-bridge/controls_result.json`.

Later result: `../template-step-safety/` proves `StepPal` is never true, so the
non-palindrome conjunct of `check` is automatic.

## Verification

`./build.sh <repo-root>` rebuilds everything from source in a fresh temporary
directory (unmodified `LychrelDigitSums.lean`, `PeriodObstructions.lean`, the
bridge modules), prints the axiom reports and runs the token scan;
`build_log.txt` is the retained log.

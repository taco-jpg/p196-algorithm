# Agent #112: actual alternating-overflow strip obstruction

Status: **LEAN-CHECKED by the author; independent review pending.** The source-pinned eight-module closure has passed an empty-directory rebuild with official Lean 4.19.0 (`6caaee842e94`). The author audited all 1,393 kernel-safe module-owned constants, including 1,162 theorems and all 19 new theorem endpoints. Axioms are restricted to `propext`, `Classical.choice`, `Quot.sound`. The 860 compiler-generated unsafe implementation artifacts are separately reported; none is accepted as a mathematical theorem. This is a scoped build, not repository-wide verification or independent peer review.

Mathematical source: `7ef5c5929eadfeee94e4071f5274698bde998724`. Exact files and the complete dependency closure are pinned in `SCOPE.json`. Historical sources belonging to Agents #4, #9 and #104 are imported unchanged and credited below.

## Exact statements

`Agent112.TwoPhase.actual_prefix_transport` discharges Agent104's `ActualPrefixTransportObligation` for the repository's actual `iterPairs` dynamics. It derives every directed-carry and delayed-digit strip equation, including the final-to-first temporal seam when the outside prefix returns.

`Agent112.TwoPhase.uniform_band_tail` discharges the separate `UniformBandTailObligation`. Two adjacent actual columns equal to6 (or12) reset the directed carries at their common finite cut. No canonical-realizability or strip-correspondence premise is hidden.

`Agent112.TwoPhase.no_actual_alternating_prefix_return` combines those facts with Agent4's finite temporal-strip obstruction. For any positive finite cut and any positive number of nonoverflow/overflow pairs, the outside prefix cannot return if those same two columns remain6/12 (or12/6) at every pair of times. The actual carry schedule and common cut are explicit hypotheses.

`Agent112.TwoPhase.no_actual_persistent_alternating_band` uses Agent9's stronger nonperiodic `no_finite_path` theorem. It excludes an actual orbit with all of: indefinitely alternating terminal carries0,1; one fixed positive interior cut; and adjacent constant columns alternating6,12 or12,6 there. **No temporal period or returned prefix is assumed.** The generic abstract boundary obstruction belongs to Agent9; this package supplies the arithmetic bridge.

`Agent112.TwoPhase.Numeric.no_numeric_persistent_alternating_band` states that result for canonical digits of the original natural-number orbit `Lychrel196.orbit`. The numeric/pair-word correspondence is proved in `numeric_representation`, rather than separately assumed. The canonical digit functions may be arbitrary outside their stated widths.

## Controls and limitations

Kernel-checked controls preserve both boundaries of the statement. `finite_scope_control` checks15 ->66 ->132, one actual0/1 overflow pair with6/12 columns but a nonreturned prefix. `phase_alone_not_overflow_alternation` checks1330 ->1661 ->3322: adjacent columns6 then12 coexist with two nonoverflow steps. Both controls have an empty axiom report. Iteration deliberately continues after a palindrome.

**No arbitrary two-phase certificate exclusion, period-at-least12 theorem, concrete accepted return certificate, infinite-safe decimal seed, or result about196 is proved here.** Applying these strip theorems to an arbitrary `Agent109.Cert.Certificate` still requires deriving the stated carry schedule and a common cut. The1330 control shows why phase alternation cannot silently replace that argument.

The new small-period certificate investigation is a separate package and does not change this accepted scope. Initial target comments under `development/` are not imported by `All.lean` and do not assert completed theorems.

## Reproduce

From the repository root, supply a fresh nonexistent output path:

```sh
python3 proofs/contributions/agent-112/two-phase-obstruction/verify.py \
  --repo . --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /tmp/agent112-strip-clean
python3 proofs/contributions/agent-112/two-phase-obstruction/controls.py \
  --max-seed 5000 --pairs 8 --output /tmp/agent112-strip-controls.json
```

Use `--expected-commit <checked-out-sha>` to require exact Git HEAD as well as SHA256/Git-blob identities. The driver creates an empty project object directory, checks import closure and source pins, compiles all eight modules, checks every listed endpoint's type, and audits every module-owned safe constant. It rejects admitted proofs, custom axioms and compiler-evaluation shortcuts. Finite Python controls supplement the Lean proofs and are not an independent review or an infinite-time result.

The original local replay was hash-pinned from GitHub Actions source archives, not a local Git checkout. A separate source-pinned CI author replay records its exact Git HEAD and publishes complete substantive logs below `evidence/ci-<source-sha>/`. Presence of the workflow alone is not a PASS; read its actual receipt. Original sources, substantive logs and controls are retained; duplicate source/object directories and downloaded compiler installations are reproducible infrastructure, not research omissions.

## Coordination

Task `agent112-two-phase-certificate-obstruction` on `p196/coordination`; continuation claim `295c49811d351f9ead2d11d635c846945631d674`. Agent112 is the sole contribution owner. The CI evidence job is a narrowly delegated Git writer and aborts if its expected branch head changes. Agent1 retains default-branch integration ownership. No main update is authorized or performed by this package.

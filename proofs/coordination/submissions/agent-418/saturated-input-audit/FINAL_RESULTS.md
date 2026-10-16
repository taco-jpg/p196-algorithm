# Agent #418: checked assumption corrections and finite realizability

LEAN-CHECKED standalone exact-definition audit, not independently reviewed or integrated. Audited PR71 head: 0a22e6278bd63554d3f7cf5b19122553de5cc0a7. Primary Agent215 extraction ownership is unchanged.

## Proved results

1. SaturatedBlockTarget is false. Four zero odd inputs give controls [1,0,0,0,0,0,1,0], overflow outputs [0,1,0,1,0,1,0,1], total overflow four, odd-input sum zero. The exact counterexample and negated target have empty axiom sets.
2. Every four-bit odd-input choice follows the same abstract eight-state skeleton with overflow total four. The sum-two filter wrongly removes ten of sixteen valid schedules.
3. An arbitrary function may supply the odd inputs of the recursively evaluated abstract trajectory. Its output count through n steps is floor(n/2). This is NOT an infinite ordinary-integer realization.
4. Every one of the sixteen patterns has a twelve-digit ordinary-decimal seed realizing the entire first eight-step block. All canonical widths, prefix/input/output observations, saturation and reset are kernel checked. A separate zero-odd-input witness is 899559344030.
5. Balance does not repair reset persistence. Seed 899550185030 realizes odd inputs (0,0,1,1), returns to (8,12,9) at time eight, but its next required control is zero and its time-nine prefix is (17,4,9), not (17,5,0). balanced_reset_does_not_force_next_edge refutes the universal implication.

## Fresh verification

Lean 4.19.0 release commit 6caaee842e94. All five source modules and the exhaustive audit were compiled from a fresh temporary directory with isolated LEAN_PATH. Six commands exited zero. Finished 2026-10-16T04:28:30.306743+00:00. All 37 declared theorems audited: 26 empty axiom sets, 11 using only propext and/or Quot.sound. The actual finite witnesses and both assumption refutations have empty axiom sets. No native_decide or unsupported axiom.

Exact source definitions were relocated into isolated namespaces with pinned provenance; this is not a full rebuild of PR71 or its imported generic theorem chain. PrefixModel blob 28eaab767b15fd81f73f2dcfc3dfff307eb02307; SaturationTheorem blob f4f8f7da5f2e87f3f0d99503e8f76e6aee4b5f6f; LychrelDigitSums blob 8a865176625283648a8a20dd2411ed77670eb0a2, all read at 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5. The first failed compilation is retained as failed evidence, not promoted: it needed an unfolding before decidability synthesis.

## Boundary and handoff

The isolated finite eight-step realizability premise is now supplied for every four-bit pattern. No accepting ReturnCertificate, all-time palindrome-avoiding integer, or result for 196 is supplied. In particular, neither a first-block reset nor an added input-balance equation proves an invariant full-interface guard.

Claim a7220090e40b6eee91c41ebb1424a655f0d8dd05. Initial checked branch checkpoint 3321cf0d71351ea60024d8f24f4f419b25679e8c. PR71 technical review 5543043036 was actually submitted. No general Discussion delivery is claimed. Full local source/evidence bundle and provenance-bearing integration patch are preserved for the user; remote raw-search transport is separate from this source checkpoint. Main has not been modified.

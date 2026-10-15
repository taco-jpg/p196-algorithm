# Independent semantic review — Agent116

Reviewer: the separate `agent116_claim_audit` agent. Proof development belongs
to the normalization, certificate, and cap-three agents. This review does not
edit their proof sources. Final execution status and exact pins are in
`REVIEW.md` once the complete candidate has been rebuilt.

## Exact statements and correspondence

`ExteriorNormalization.Br_append_phase` states an identity for the original
`Agent109.Br`, under `Phase c` and `Bounded B`, with completely arbitrary A and C.
It appends exactly `tOf c + tOf c` to the raw returned exterior. The proof handles
both overflow branches and keeps the lengths needed for `zipAdd_append` explicit.
It does not assume a positive first coefficient. Iteration gives an arbitrary
constant suffix. The suffix decomposition from `Agent109.Outer.stripSuffix_spec`
then proves input normalization leaves the deterministic `outerNext` unchanged.

`outerNext_of_partial_trim` has the exact `LocalOK` equality, including its trim
amount and successor phase. Thus `CertificateExterior.local_outer_step` proves
the required correspondence rather than assuming a graph edge. `stateOuter`
maximally strips the listed state's exterior even when its original link strips
only part of the constant suffix.

`certificate_outer_orbit` follows the actual cyclic index `n % cert.P` for every
natural n. `Valid` supplies `cert.P > 0`; the proof explicitly uses it for modular
index bounds. The theorem does not replace an infinite path by a sampled trace.

`certificate_phase_index` obtains an even phase for state zero from the last
cyclic link. This is needed because `Phase` by itself also permits odd values.
The proof covers period one and excludes a zero period through `Valid`.

The initial `EscapeAt` interface includes `validOuter`. Its cap-two theorem
therefore retains explicit exterior positivity or `Admissible0`. The latter
really suffices: `CertificateRealization` constructs the first ordinary
realization through the existing exact `template_realized`, propagates it by
`actual_template_step` and `template_trim`, and obtains each nonempty exterior's
positive head from `lastPos_pairWord`. Empty exteriors are allowed. The two
integer operations here are Agent109's existing operations; their previously
reviewed `Compat` package relates them to the repository's canonical operation.
No new claim about an actual infinite integer orbit is made by this package.

The later `BoundedEscapeAt` deliberately drops `validOuter`: its finite theorem
must cover *all* bounded words. `valid_exceeds_cap_unrestricted` consequently
needs only `Valid`. It handles the already-large initial exterior separately;
otherwise it follows the finite escape witness back to a listed cyclic state.

`CertificateCap3.accepted_exceeds_three` has only `check cert = true` as its
premise. Its conclusion is a state index below the period whose maximally
trimmed exterior has at least four coefficients. The finite escape premise is
discharged by `cap3_all_exit_witness`, not supplied as a hypothesis. The two
rejection corollaries correctly cover normalized or raw cap-three candidates,
including empty certificates. They do not assert that an accepted certificate
exists, that exterior size four is sufficient, or that any orbit terminates.

`ActualCap3.lychrel_cap3_exit` uses the genuine `Lychrel196.orbit` and
`Agent8.template` through the unchanged `Compat` identities. It requires a
valid even-phase starting exterior of length at most three, bounded blocks,
an actual pair-word realization, and both bands at least 18. The finite witness
has time at most nine, so the existing actual-outer-orbit theorem's budgets
`2*i <= g,h` are available even at the last endpoint. Its conclusion names the
computed `outerIterate i` exterior; it does not assert that every alternate
representation of the integer has large exterior. The output phase and blocks
are supplied by the same actual orbit invariant.

## Finite graph and endpoint conventions

The decoder enumerates exactly the length layers 0, 1, 2, and 3 with sizes
1, 19, 361, and 6859. `decode_complete` proves coverage for every word with
entries at most 18 and length at most three. It imposes no hidden leading-digit
or suffix constraint. Eight phase indices give 57,920 encoded inputs.

The valid graph uses `staysWithin 3 9`; the unrestricted graph uses
`staysWithin 3 10`. This predicate includes times zero through its final bound.
The recursive witness lemma therefore concludes an exit at a time at most nine
or ten, respectively. It does not exclude only a path of the wrong length.
Each finite batch is proved with `decide +kernel`; the assembled theorem
contains all 57 disjoint ranges, ending with indices 7168 through 7239.

The all-domain ten-step bound is necessary for the claimed scope. Independent
whole-word arithmetic found exactly three maximizers: phase 6 and exteriors
`[0]`, `[0,6]`, `[0,6,6]`. The first stays within cap three through time nine and
has exterior `[18,12,7,5]` at time ten. Canonical nine-step sharpness and this
unrestricted ten-step sharpness are exterior-map facts, not assertions that a
canonical integer realizes the invalid-head maximizer.

## Independent controls and retained correction

`independent_controls.py` does not import author functions. It normalizes the
complete symmetric column word by ordinary integer division and then mirrors
the output digits. All 115,840 bounded sources through exterior length three,
over all 16 permitted phases, passed 231,680 phase-append identities and 115,840
input-strip invariance checks. There are also 3,000 literal canonical integer
controls with randomly chosen interfaces, symmetric centers and band lengths.
These are finite experiments, not substitutes for the Lean proofs.

`unrestricted_cap3_controls.py` independently enumerates every one of the 57,920
unfiltered even-phase inputs. There are no cycles; maximum first exit is ten.
The complete histogram and all three maximizer trajectories are retained.

An initial reviewer hand conjecture that phase 2 with exterior `[0]` formed a
six-cycle was false. The independent arithmetic run rejected it, and the claim
was explicitly withdrawn before acceptance. Its attempted source and rejection
record remain in `development/attempt01-*`. The corrected fixture proves only
that this initial state fails `validOuter`, remains within cap two through time
five, and has exterior `[6,15,1]` at time six. It is not a counterexample to
unrestricted cyclic exclusion. In particular, the final check-only theorem does
not require the earlier admissibility premise.

# Numeric decoder: non-author semantic review

**Verdict: PASS; no source modification requested.**

Reviewer: Agent #105 subagent `/root/structure105`, session `9df76b`.
Reviewed author: `/root`. Reviewed module: `Agent105NumericDecoder9df76b.lean`.
This is a written internal semantic audit of the three numeric-wrapper exports.
The reviewer authored the imported Scan module, but did not author this Numeric
wrapper. It is therefore a non-author review of this module, not an independent
reaudit of every transitive dependency. The separate full-chain clean build is
assigned to `/root/scope105`.

## Frozen inputs and compilation evidence

The reviewer read the entire Numeric wrapper and Target bridge, checked the
actual definitions of `Canonical`, `Admissible`, `decodeAtWidth`, and the fixed
width carry cases, and matched all four source hashes below against local bytes.
The Numeric file also matches `attempt001/source.lean` byte for byte.

| Source | SHA-256 |
|---|---|
| Numeric | `9a63eb03cb04d9e7fb3294216ab770893ac227c089ddba6d864d73d949229db5` |
| Target | `2c2cbf18088e0a281ff78547cc3b2aa465050504c9139fc2839fb70e86db7c9d` |
| Scan | `4e7f3a29e41c3e40adc08326947fe28b5505015f3c68cba67a1cb648318cad1d` |
| Local | `820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872` |

Read evidence: `attempt001/result.json` records Lean 4.19.0 execution with
`--trust=0 -j1 -DElab.async=false`, exit 0, and this exact Numeric hash.
`attempt001/compile.log` prints only `propext`, `Classical.choice`, and
`Quot.sound` for each of the three exports. This review records the author's
actual development compilation; it does not relabel that run as an independent
clean replay.

## Three export checks

| Export | Checked interpretation |
|---|---|
| `decodeNumerical_eq_some_iff_payload` | For an original `Canonical Y e W`, success with this exact list is equivalent to the original admissible pair profile, exact finite output digits and terminal carry, the physical width choice, and list length `L`. |
| `decodeNumerical_eq_some_iff` | The returned list is exactly the within-width `columnSum` profile of some positive ordinary integer with `Canonical n d L` and original `step n = Y`. The reverse direction transports the actual profile to this list in the correct equality direction. |
| `decodeNumerical_isSome_iff` | Executable acceptance at the prescribed width is equivalent to existence of an actual positive canonical predecessor at that same width. The finite-list existential is eliminated in both directions without adding a realizability assumption. |

## Width, digit domain, and boundary audit

- In the same-width branch, `W = L` selects terminal carry 0. In the overflow
  branch, `W = L + 1` selects carry 1 and the function explicitly requires
  `e L = 1`. The branches cannot overlap over `Nat`. Every other width or
  overflow-leading-digit case returns `none`; the Target bridge's actual
  canonical step-width cases justify this exclusion.
- Both successful branches derive `forall i < L, e i <= 9` from the target's
  original `Canonical` digit bound. The necessary relation `i < W` follows
  from the respective width equation. The raw local column solver's all-Nat
  specification is never incorrectly treated as a decimal output theorem.
- `Canonical Y e W` entails positive width, a positive leading digit, and a
  positive target. The theorem does not make a claim for an arbitrarily padded
  target, a zero-width target, or `Y = 0`. No restrictions are imposed on the
  infinite digit-function tail beyond the canonical width.
- A zero source width is rejected by `decodeAtWidth`, including the possible
  outer guard `W = 1`, `L = 0`, `e 0 = 1`. This agrees with both `Admissible 0 q`
  and `Canonical n d 0` being impossible. There is no special unproved
  exception for one-digit source widths.
- Overflow strips only the genuine added leading 1. The remaining low `L`
  digits are not required to be canonical: internal zeros and a zero top
  payload digit remain valid. In particular the ordinary case `5 + 5 = 10`
  has `L = 1`, `W = 2`, low payload digit 0, pair coefficient 10, and carry 1;
  none of the wrapper's guards excludes it.
- Odd source widths retain the Scan center-evenness condition through original
  `Admissible`; even widths retain carry meeting at the empty interior.
  The wrapper introduces no additional parity condition on the target width.
- The precise success theorem records `qs.length = L` and equates every
  coefficient for `i < L`. It does not require equality of irrelevant infinite
  tails. Positive realizability comes from the original `valid_word_realizable`
  bridge, including nonzero exterior coefficient, rather than from a merely
  abstract carry trace.

## Scope

The result is a complete executable decision and exact pair-profile decoder at
a prescribed source width for a canonical numerical target. It does not claim
that the ordinary predecessor is unique: several digit splits can share the
same pair profile. It does not enumerate those digit splits or all source
widths, count fibers, or prove any all-time trajectory assertion. No additional
mathematical source or theorem was created during this review.

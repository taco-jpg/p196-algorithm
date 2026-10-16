# Agent #3: two incoming histories for protected overflow fibers

This active contribution formalizes the preserved construction in
`astra_counting_safe_image_fibers.txt` (Git blob
`30f8ed333edb2e11402569c62d50def2451ffef4`). Its full theorem is **WIP**.

The target is an exact family for every `m >= 0`, `k >= 1`: `2 ^ m`
distinct canonical coefficient words of width `2 * (m + k + 7)` with two
consecutive non-overflow incoming transitions and a shared next overflow
image. The construction appends a state-dependent six-symbol correction
to an arbitrary `m`-symbol word over `5,14`, followed by `k` eighteens.
The earlier protected finite-horizon theorem supplies the common image and
future safety after the two incoming histories have been established.

This does not assert a fixed seed that survives every horizon. It counts
coefficient words, not all individual decimal digit realizations. The
general digit-split multiplicity, odd-width no-overflow maximum, and
unrestricted overflow maximum are separate collaborators' tasks.

## Current checkpoint

`HistoryInterfaces.lean` identifies the exact retained carry in Agent #9's
`scan` with Agent #8's `terminalCarry`, transports an existing accepting
folded inverse `Path` to the original `Agent8.stepWord`, and establishes
canonicality for bounded even mirrored words with positive outer
coefficient. These are compatibility lemmas; the original path-soundness
proof and inverse arithmetic remain Agent #9's contribution.

The finite sixteen-state certificate, arbitrary-word history construction,
family cardinality, and ordinary-integer safety composition remain under
development. Incomplete attempts are kept outside the accepted module set.

## Exact dependencies

The four files in `dependencies/agent9/` are unchanged source copies from
Agent #9's published source commit
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. Their original module and
declaration names are retained. `SOURCE_PINS.json` records paths, Git blobs,
and SHA-256 identities. They import only Std and the original
`PeriodObstructions` module used by the protected-family contribution.

The contribution branch starts at
`6576cee93d18145c638f298b0abcb1cd0a0f451e`, the published source checkpoint
of `../finite-horizon-overflow-20261016/`. The toolchain is Lean 4.19.0,
release commit `6caaee842e94`. Sources are copied under their logical module
names to a fresh build directory. No compiled objects or runtime binaries
are committed.

Claim: `142563ce83e36afe5ddaccb0e93ed821fd40eba0` on `p196/coordination`.
Coordination issue: <https://github.com/taco-jpg/p196-algorithm/issues/61>.
No default-branch integration slot is held.


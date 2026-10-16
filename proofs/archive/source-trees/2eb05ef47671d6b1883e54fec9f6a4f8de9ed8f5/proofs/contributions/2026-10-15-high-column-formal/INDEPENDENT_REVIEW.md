# Independent review of the high-column formal theorem

PASS for the mathematical argument, Lean source, fresh-build checker, and
saved 14-theorem axiom report. No second Lean build was run for this review.
The reviewed source SHA-256 is
`22758aba54f102ba58ccf09bc9409f20c09939cd9cd03f007f2cb86892a524eb`.

The carry induction is valid at the full upper bound thirteen: the initial
coefficient is between ten and thirteen, and every later coefficient plus
the incoming one is between ten and fourteen. Thus every outgoing carry
through the last physical column is exactly one. The exact units formula
uses `q 0 ≥ 10`, and the internal formula uses `q i ≥ 9`, so neither natural
subtraction conceals an underflow.

The formal width is explicitly `L+1`. The extended output includes the
actual terminal one, which is covered by the digit bound four. Its reflected
index uses that new width; the next pair coefficients are therefore bounded
by eight at every physical position. The bound is transferred to the actual
second ordinary output by `iterPairs_low_palindrome`, not by assuming an
abstract normalized word represents the orbit.

Width one is covered without an internal-digit assumption. Canonical width
is positive, so the units and terminal columns are distinct; the latter is
the overflow digit. In a canonical width-one word the coefficient is even,
so the constant-eleven case simply cannot arise. This is consistent with
the immediate-palindrome equivalence rather than an extra exception.

The immediate-palindrome classification is used correctly: the outside
coefficient at least ten excludes the all-small case, and the lower bound
nine excludes zero in the zero/eleven case. Thus every coefficient must be
eleven. The final time-two theorem asserts nonpalindromicity at positive
time one and palindromicity at positive time two only. It makes no claim
that the seed at time zero was nonpalindromic; the checked seed 55 explicitly
preserves this distinction. The upper-bound control using coefficient
fourteen correctly shows why the uniform interval cannot be widened to
include fourteen without further restrictions.

The report matches all fourteen public theorem declarations, the frozen
base dependency, and the current source. Only standard logical axioms are
listed; the four numerical controls are axiom-free. This review does not
extend the decimal formalization to all bases or claim preservation of a
seam certificate.

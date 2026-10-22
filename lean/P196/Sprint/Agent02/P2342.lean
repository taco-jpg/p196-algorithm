import P196.Sprint.Agent02.A124S2K8AllRows
import P196.Sprint.Agent02.A124S2K8Entries
import P196.Sprint.Agent02.Long196

/-!
# Prefix 2342 never occurs in the 196 orbit (sprint agent 02)

2342 is one of the 16 four-digit prefixes that the forward census excludes at width 8 but not at
width 7 (see `sprint/agent-02/REPORT.md`); it is not under any two-digit prefix of `Core`. The
width-8 rank tree `Sprint.Agent02.CertK8.ranks` (17,317 words, ranks ≤ 8; generated with
Agent #124's archived `gen_code4.py`) is checked here against the complete long inverse
(`allRows`), and the entry `([2,3,4,2], 8)` is checked by `entries00_ok`. The short-source premise
is not needed for the orbit of 196 (`Sprint.Agent02.no_196_of_entry_long`).
-/

namespace Sprint.Agent02.P2342

open Lychrel196 Agent124.PrefixL Agent124.CodeCert

/-- **No iterate of 196 is a palindrome beginning with the digits 2342.** -/
theorem no_196_2342 : ∀ t, ¬ PalStartsL [2, 3, 4, 2] (orbit 196 t) := by
  have h := List.all_eq_true.mp CertK8.entries00_ok ([2, 3, 4, 2], 8)
    (by simp [CertK8.entries00])
  exact no_196_of_entry_long (by decide) (by decide) CertK8.allRows ([2, 3, 4, 2], 8) h
    (by decide)

end Sprint.Agent02.P2342

#print axioms Sprint.Agent02.P2342.no_196_2342

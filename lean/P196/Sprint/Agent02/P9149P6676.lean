import P196.Sprint.Agent02.A124S2K8BAllRows
import P196.Sprint.Agent02.A124S2K8BEntries
import P196.Sprint.Agent02.A124S2K8BEntries1
import P196.Sprint.Agent02.Long196

/-!
# Prefixes 9149 and 6676 never occur in the 196 orbit (sprint agent 02)

Two more of the 16 four-digit prefixes that the forward census excludes first at width 8 (neither is
under a `Core` two-digit prefix). One width-8 rank tree `Sprint.Agent02.CertK8B.ranks`
(102,852 words, ranks ≤ 26; Agent #124's archived `gen_code4.py`) is checked against the complete
long inverse (`allRows`); the entries `([9,1,4,9], 11)` and `([6,6,7,6], 26)` are checked by
`entries00_ok` and `entries01_ok` (one module each); the short-source premise is not needed (`Sprint.Agent02.no_196_of_entry_long`).
-/

namespace Sprint.Agent02.P9149P6676

open Lychrel196 Agent124.PrefixL Agent124.CodeCert

/-- **No iterate of 196 is a palindrome beginning with the digits 9149.** -/
theorem no_196_9149 : ∀ t, ¬ PalStartsL [9, 1, 4, 9] (orbit 196 t) :=
  no_196_of_entry_long (by decide) (by decide) CertK8B.allRows ([9, 1, 4, 9], 11)
    (List.all_eq_true.mp CertK8B.entries00_ok _ (by simp [CertK8B.entries00])) (by decide)

/-- **No iterate of 196 is a palindrome beginning with the digits 6676.** -/
theorem no_196_6676 : ∀ t, ¬ PalStartsL [6, 6, 7, 6] (orbit 196 t) :=
  no_196_of_entry_long (by decide) (by decide) CertK8B.allRows ([6, 6, 7, 6], 26)
    (List.all_eq_true.mp CertK8B.entries01_ok _ (by simp [CertK8B.entries01])) (by decide)

end Sprint.Agent02.P9149P6676

#print axioms Sprint.Agent02.P9149P6676.no_196_9149
#print axioms Sprint.Agent02.P9149P6676.no_196_6676

# S38 discarded shortcuts

1. Do not infer a 120-step seam return from the correct 120-bit overflow clock
   or a matching mod-101 checksum. Both are necessary, not sufficient.
2. Do not reuse S12's even-centre physical realization helper unchanged for an
   odd-length pairword: the odd midpoint coefficient must be even and its
   physical source needs the actual central digit C[mid]/2.
3. The earlier generic Lean pumping draft was not compiled and is not part of
   this result; it is not safe to register or push as Lean-verified.

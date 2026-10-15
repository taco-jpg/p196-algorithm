# Agent #13 — folded coefficient-product obstruction

Source `proofs/research/main_existence_attempt/continuation_pass/finite_seed/FOLDED_WEIGHT_OBSTRUCTION.md`, section 2, at `c2b6977e43a79caa5ff3bb88801f3ba896986f38`, SHA-256 `5eef7b1ea7576de8e3ac8246c73673f91693795a0873b9c3ef997d1ef47150f9`. Task `agent13-folded-product-weights` published on coordination at `f12a52c9fdcdc06f83a0bd68377a8f25bd47d5a6`. Branch `formalize/agent-13/s20261015-products` is stacked after the completed folded family, leaving PR29 and PR32 review scopes unchanged.

For every strictly positive real coefficient a_j, j=0..18, and every strictly positive width factor A_L, define the even canonical pair-word weight as A_L times the product of a_j over the first half (each reflected pair counted once). If odd canonical states are included, their weights may be any strictly positive values; their contribution must not decrease the lower bound. Preserve arbitrary width dependence of A_L, not a constant factor restriction.

For every r>=0,k>=1, at the exact target with half R=(11,9^(4*r+1),18^k), prove that the complete safe incoming sum divided by target weight is at least

`(a_5*a_14)/(a_11*a_9) * (1+(a_4*a_14/a_9^2)^2)^r`.

Prove the exact displayed binary family's partial sum and target weight as intermediate identities. The incoming sum itself must range over every admissible safe predecessor under the original actual FoldedDecimal.nextWidth/nextColumns map, not be defined to equal the constructed family's sum. A finite bounded representation must prove it captures all incoming widths and all finite canonical coefficient words, preserves equality, and has the actual arithmetic interpretation. Include r=0 and k=1.

Deduce that for every finite real C there exists a safe target with incoming sum greater than C times target weight. Positivity of the ratio denominator, positivity of the prefactor and strict growth of the exponential base are proof obligations. A binary product expansion or field identity alone is only partial coverage, not completion of either original claim.

Reuse Agent13FoldedFamily at `10aa1bc46c61a801965ffe647590ff17622c5320`, verified in clean CI at `4f154c5917a40db776f6bdb318ac43b82ff8088c`, and original decimal definitions. The finite encoding is only a faithful representation, not a substitute transition system. Keep the same Lean 4.19.0 and isolated pinned Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` with its exact manifest; no foundation migration. Every result needs actual compilation, transitive axiom audit allowing only propext/Classical.choice/Quot.sound, source hashes, and a fresh contribution build. Official library caches remain explicitly labeled. Independent review is separate.

Section 3's finite-window weights, arbitrary position-dependent weights, restricted deeper-image supports, and all-time orbit conclusions are outside this contract. No result about 196, a Lychrel witness, originality, or exhaustive corpus completion is asserted.

# Agent #314 — 6/12 bridge refinement

The first audit identified `hshape` in `ordinary_reverse_add_exterior` as conditional. A second source inspection found a stronger, already formalized bridge in `Agent109.Outer.actual_outer_orbit`.

That theorem proves an actual ordinary reverse-and-add orbit follows `outerIter` while both template bands remain at least two, starting from an ordinary integer satisfying an explicit `pairWord n = template ...` premise. `Agent109.Cert.template_realized` separately proves that admissible templates with a mirrored center are realizable by an ordinary integer.

This changes the exact bottleneck for the requested 6/12 construction:

- The ordinary-arithmetic semantics of the template/exterior machinery are already substantially formalized.
- The remaining gap is not simply ordinary arithmetic being unrelated to the exterior model.
- The critical missing interface is a theorem connecting the specific `Agent9.AlternatingScalarBoundary` Slot/Tile traces (the constants `six`, `twelve`, `root`) to the `Agent109`/`Agent7` exterior state and transition representation used by the ordinary-orbit bridge.

In particular, `no_six_boundary` and `no_twelve_boundary` prove impossibility inside the exact `Slot`/`Tile` relation. Their own module comment explicitly states that connection to an actual exterior is a separate obligation. `actual_outer_orbit` cannot discharge that obligation automatically because its state is `Outer = (phase, B)` and its hypothesis is a full template equality.

Therefore the strongest defensible result at this checkpoint is a precise model-interface diagnosis, not a claim that the 6/12 obstruction already transfers to ordinary 196.

Next concrete investigation: derive the exact map from an `Agent109.Outer` state (phase and B) to the four Slot coordinates `(a,b,c,z)` and check whether the 6/12 constants correspond to any admissible outer states. If they do, formalize that map; if they do not, record the mismatch as a counterexample to the proposed identification.

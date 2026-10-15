# Independent source review of the scalar hierarchy assembly

**Source-level verdict: PASS. Full kernel endpoint: pending at this checkpoint.** This review covers the mathematical interfaces and concrete dispatch in `ScalarHierarchyData.lean` and `ScalarHierarchy.lean`, with the finite graph/rank interfaces and actual-path lift dependencies. The reviewed bytes are copied and hashed in `source_manifest.json`. The active proof package was not edited.

This is not a claim that all generated row proofs have completed kernel checking. It also does not duplicate the independent complete table comparison in the separate scalar-finite-review package. Two generated row modules were read to inspect how finite checks are joined into universal certificate fields; the other generated tables were not manually read row by row.

## Forward realization of the induced lift

A finite graph vertex is valid exactly below its stored size. Edges use a target-plus-one code, with zero representing absence, and explicitly restrict the label to a bit. The lift certificate covers every valid parent vertex in the selected component with a member-table index and a left-inverse identity. Its child size is nineteen times the number of members. Therefore every pair of a selected parent and an actual coefficient in `Fin 19` has a valid encoded child; no actual extension can be lost by filtering the member table.

The field rows preserve phase, the newly exposed coefficient, and the low outgoing carry. The latter is `(coefficient + parent.low)/10`, a carry within the same addition. It is not a carry at the next orbit time. The transition rows require every internally projecting parent edge with a valid target to have the encoded child edge. In the realization proof, target validity comes from the target semantic vertex, and the coefficient bound comes from its `Fin 19` type. Thus the conditional row statement is sufficient; it does not omit a necessary edge because of an unproved target bound. The target-plus-one subtraction is applied only after identifying a genuine edge code.

Only forward completeness is needed. Neither injectivity of the whole semantic encoding nor a converse statement that every finite edge is physically realizable is assumed. Additional graph vertices or edges would only make the required bound harder to prove.

## Actual orbit path construction

`ActualPath` records the actual orbit at every included vertex, its scalar phase, the current exposed coefficient, the actual low carry, and the actual high-side carry label on every included edge. Its path length counts vertices. Restricting an interval shifts both the orbit offset and the phase offset, retaining all endpoints and using edges only when both endpoints are inside the interval.

The analytic one-column lift constructs the next coefficient directly from the actual word. Its label is the actual deeper carry, so temporal correlations survive. The coefficient bound follows from admissibility, and the initial-width lower bound remains valid because widths do not decrease. The bounded wrapper proves actual labels are bits before transporting a path to the stored finite graph. Selecting a component restricts valid vertices while retaining internal edges; the actual constant-component interval therefore lies in exactly the induced source required by the child certificate.

`ActualJobFamily.constructive_child_lift` derives the generic hierarchy's child-path premise from these results. It does not assume that a child path exists. The encoded child interval has exactly the same number of vertices, and arbitrary starting time and starting scalar phase are allowed. The existential offsets in the path family are preserved by restriction and by lifting.

## Rank and concrete job assembly

The rank rows supply two local facts: each component's weight is at most its rank, and every cross-component edge decreases rank by at least the source weight. A component marked acyclic has no internal edge. These certificate conditions are enough for the previously established generic hierarchy theorem; the proof does not need to trust a particular SCC algorithm or a claimed uniform time to reach a recurrent component.

There are sixteen concrete jobs. The child routing, encoder routing, cyclic predicates, and weight identities use the same listed component cases. Their default branches cannot be used to evade a lift obligation: every theorem requiring a child first assumes `cyclic=true`, and all other cases are discharged by that predicate being false. At each listed cyclic case, the generic component weight is exactly the selected child's bound. Early acyclic jobs terminate without a child lift.

The height is `14-width`. Every cyclic child raises width by one and strictly lowers that height. Every cyclic parent has width at most thirteen, so initial physical width at least fourteen supplies both `1<=k` and `k<L` for every required analytic lift. Overlap of reflected prefixes introduces no additional width requirement. No lift is demanded from the terminal width-fourteen job.

`checked`, `realizes`, `vertex_bounds`, and `edge_bounds` dispatch the concrete per-job certificates into the generic hypotheses. The final theorem applies `ActualJobFamily.actual_path_vertices_le` at job zero. Its numerical conclusion is **at most 659 vertices**, conditional on a root `ActualPath` and initial width at least fourteen. The zero-length case is also covered by the generic theorem; it does not require a valid starting vertex when no vertex is included.

## Remaining acceptance and scope obligations

The large finite row proofs, final composition, and their exact provenance/axiom audit must finish before calling the 659-vertex endpoint kernel-accepted. The reviewed package itself marks that status as pending. Ordinary scalar-clock hypotheses must still be connected to the root graph path in the separate composition package. Conversion from vertex counts to period counts, and the small-width preparation argument, are separate obligations; this source review does not infer them merely from the number 659.

No mathematical gap was found in the reviewed assembly. This checkpoint makes no claim about an infinite nonpalindromic orbit or the main P196 existence question.

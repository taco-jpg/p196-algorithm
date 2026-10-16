# Additive clarification of the unsafe implementation ledger

This note clarifies the summary wording in the Agent103 residual-five-fibers
package at `018a49231cd3226506699282f0f173745e6b9f8d`, its PR119 body/review
5554255589, and issue61 comments6225648325/6225696818. It changes no mathematical
source, proof status, original execution log, or historical audit result.

The published `check.py` records `UNSAFE_IMPL` only in its `ConstantInfo.axiomInfo`
branch when `AxiomVal.isUnsafe` is true. Consequently its 33-entry
`UNSAFE_IMPLEMENTATIONS.json` is a ledger of **unsafe implementation axioms**.
It is not a census of every definition whose `DefinitionVal.safety` is unsafe,
nor a claim that there are only 33 unsafe constants of all kinds in the project.
The earlier phrase “33 unsafe implementation helpers” should be read in this
specific sense; using it as a total environment-wide unsafe count is incorrect.

The later, single fresh 27-module first-hit build from frozen source1908a7e9
completed on 2026-10-16 at22:20:36UTC. Its expanded actual origin audit separates
the two categories. It finds the same 33 inherited unsafe implementation axiom
entries and additionally inventories 1,157 `defnInfo`/`opaqueInfo` entries:
216 safe, 917 unsafe, and 24 partial. All 1,157 are definitions, with zero opaque
entries. None belongs to the four new first-hit modules, which contain only
theorem declarations. These counts describe that actual new execution, not an
invented extra run of the earlier package.

The proof acceptance gate is unchanged: the earlier build actually printed the
transitive axioms for all 1,812 theorem constants in its 22-module closure;
the later build actually did so for all 1,881 in its 27-module closure. Every
reported theorem dependency stays within `propext`, `Classical.choice`, and
`Quot.sound`. None of the 33 implementation axioms occurs in those theorem
axiom lists. Implementation inventories are retained explicitly; they are not
being presented as separately kernel-proved executable implementations.

The original checker, raw logs and ledger remain preserved byte-for-byte.
The exact new inventory, its generated audit command source and module-origin
counts are in the first-hit package's full verification record and definition
inventory. The genuine nonauthor runtime specialist checked the classification;
root independently inspected both checker branches and the actual JSON totals.

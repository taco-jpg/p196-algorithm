# Independent scalar-build resume review

The production builder `../2026-10-15-scalar-finite-certificate-formal/verify.py`
was reviewed at SHA-256
`a2f6666a64a664465a33528ab68deb1493496683b90af8ea16ca9520bb01dada`.
This is a source and isolated negative-fixture review of build provenance.
It does not report completion of the separate fresh Lean build, prove the
finite certificate, or replace that build's final axiom report.

The resume predicate accepts a module only when its exact source, compiled
object, log, compiler/settings identity and direct-import fingerprints agree
with a successful record. Missing legacy fields fail closed. The main loop
validates project imports in topological order, so each dependency has already
been rebuilt or validated before a dependent object is considered for reuse.
The copied source snapshot and isolated project search path prevent an old
development object from silently satisfying a project import. Changed source
snapshots force rebuilds even when a stale object remains on disk.

The collector rechecks every successful module, including reused modules,
against its current source, object, log and direct imports before marking a
stage successful. It also checks repository sources, the checker source and
compiler identity again. The final stage derives its public theorem list
from the selected source closure, requires exactly that set of axiom records,
and rejects axioms outside `propext`, `Quot.sound`, and `Classical.choice`.
The `checks` stage alone is deliberately reported as `CHECKS_PASS`, not as
the full proof audit.

`check_resume_fixtures.py` imports the frozen builder without calling its
main routine and creates a temporary synthetic module and dependency. Its
27 checks passed: the unchanged and restored exact records were accepted;
changes to dependency source/object, module source/object/log, source snapshot,
compiler/settings identity, missing record fields, invalid success flags,
missing files and an empty legacy record were rejected. Dependency hashes
were recomputed after each mutation, exactly as the production loop does.
The temporary files were deleted after the test. No production source,
running build, manifest, log or compiled object was modified.

Result: **PASS for the reviewed resume/collection provenance controls.** The
fixture script and `fixture_results.json` retain the exact cases and source
hash. Reproduce with `python3 check_resume_fixtures.py`; this performs no Lean
compilation and starts no long-running work.

# Kernel certificate for decimal palindrome prefix 620

Agent #104, 2026-10-16. Mathematical source is frozen at
`dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`. This package instantiates
Agent #124's original finite inverse-certificate checker and decimal semantics.

## Exact result

`Agent104.Prefix620.ancestry_bound12` proves that, for every positive natural
seed A and natural time t, if the ordinary reverse-add orbit reaches a decimal
palindrome P whose canonical leading digits are 620, then t <= 12.
`no_196_620_palindrome` excludes that particular palindrome family from every
iterate of 196. `palindromeStarts620_iff` exposes the original Canonical numeral,
ordinary Palindrome predicate, width >= 3 and the three most significant digits.
The statements have no remaining certificate-validity hypotheses.

The certificate has 59,189 ranked nodes, 71,560 inverse edges, 10,002 initial
words and 10,467 admissible short source words. Its maximum rank is 11; the
soundness theorem consequently gives 12 additions. The short-width-zero case
is checked explicitly. Certificate SHA256:
`e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5`.

The separate concrete-witness package in PR #128 proves that seed 19014942070
first reaches palindrome 62003033030026 at time 12, and that every uniform bound
for this same family is at least 12. That lower bound has its own source,
replay and review; it is not a premise of this upper-bound certificate.
Neither package settles whether the orbit of 196 ever reaches any palindrome.

## Verification status at this checkpoint

**Author LEAN-CHECKED:** all 510 concrete modules and 13 generic dependencies
have actually compiled using official Lean 4.19.0, explicit `--trust=0`, one
worker and disabled asynchronous elaboration. The final stage compiled 431 new
modules and reused 79 previously checked, byte-matched author objects. It took
1077.408 seconds, with maximum recorded process RSS 3,335,928 KiB. This author
stage is incremental. Full commands, source/object/import hashes, logs and the
completion receipt are in `generator/evidence/` and
`generator/AUTHOR_BUILD_COMPLETE.json`.

The root predicate-fidelity theorem has no axioms; the upper-bound and
196-family-exclusion theorems use only `propext`, `Classical.choice` and
`Quot.sound`. No sorry, new mathematical axiom, native_decide or external
solver premise is used in the accepted proof chain.

**Independent semantic review PASS:** the genuine nonauthor `strategy_review`
specialist checked the ordinary decimal interpretation, every certificate node
and inverse edge, all initial and short domains, independent integer controls,
the generated Lean code tree and each coverage connection. The 12 frozen review
files and their exact pins are listed in `review/PUBLISH_REVIEW_FILES.txt`.
This is same-session, shared-account collaboration, not external peer review.

**Independent complete Lean replay RUNNING at this checkpoint:** the genuine
`runtime_scout` specialist is rebuilding all 523 sources in a new empty build
directory, followed by the complete module-origin theorem axiom audit. No
author compiled objects are reused. Final completion is not asserted here.
The unchanged canonical verifier does not explicitly pass `--trust=0`; Lean's
default is trust=max. This is distinguished from the author's explicit-trust0
commands. The source transport pins every selected file and the compiler and
checks all 1,471 installed standard-library objects against the official archive.

## Reproduce the complete canonical check

Use a full checkout containing this evidence checkpoint and the frozen source
commit, Python 3, Git, and official Lean 4.19.0. Choose new, nonexistent output
directories. This command recompiles the complete closure and preserves the
original checker and wrapper:

```sh
python3 proofs/contributions/agent-104/prefix620-kernel-20261016/verification/independent620/rebuild.py \
  --repo . \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --dependency-map proofs/contributions/agent-104/prefix620-kernel-20261016/verification/author-base/dependency-map.json \
  --generation-manifest proofs/contributions/agent-104/prefix620-kernel-20261016/generator/GENERATION_MANIFEST.json \
  --source-ref dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4 \
  --stdlib-manifest proofs/contributions/agent-104/prefix620-kernel-20261016/verification/independent620/standard-library-integrity.json \
  --root-module Agent104Prefix620 \
  --endpoint Agent104.Prefix620.palindromeStarts620_iff \
  --endpoint Agent104.Prefix620.ancestry_bound12 \
  --endpoint Agent104.Prefix620.no_196_620_palindrome \
  --build /tmp/new-agent104-620-build \
  --evidence /tmp/new-agent104-620-evidence \
  --jobs 1 --canonical
```

This is a selected 523-module verification, not a repository-wide result.
The checked theorem scope is exactly the canonical leading-digit-620 family.

## Source and evidence design

The 510-file source manifest is `generator/GENERATION_MANIFEST.json`; its
SHA256 is `d2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03`.
The large finite instance is divided into data modules, 256 row leaves, 101
initial slices and 78 short slices. Generic list-membership coverage theorems
and local kernel-checkable equalities connect the slices to the unchanged full
enumerations. No unproved Python completeness claim is assumed by Lean.

Original archived certificate/source provenance, discovery generators, failed
whole-list reductions, out-of-memory/stack/termination logs, the import-repair
failure, successful pilot evidence and later corrections are retained.
Failed attempts are outside the accepted manifest. Reproducible `.olean`
products are not published; their actual hashes are recorded.

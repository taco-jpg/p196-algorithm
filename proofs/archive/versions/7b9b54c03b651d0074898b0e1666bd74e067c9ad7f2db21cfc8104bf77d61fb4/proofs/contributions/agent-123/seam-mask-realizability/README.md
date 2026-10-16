# Agent123: exact seam-mask realizability

Status: WIP candidate source, not yet compiled at publication of this draft.

Task: `agent123-seam-mask-realizability` on `p196/coordination`, claim commit `f423783fd15a4717b9205de0c9bd180efc2eacdb`. Source base: `eec3d5f3646cab50abad6e610ea19626cd249070`. Branch: `research/agent-123/s20261015-1544`. No integration ownership.

This formalizes the full-mask part of Theorem 1 in `proofs/research/main_existence_attempt/continuation_pass/seam_persistence/METHOD_AND_PROOF.md`, rather than claiming a new discovery of the written characterization. Existing IntrinsicSeam activity/maximality and Agent107 response/mass identities are reused, not relabeled as new results.

The exact target is constructive realizability: a binary natural-valued mask on the finite coefficient word is produced by the repository's actual `seamDefect` if and only if its selected positions are actual carry-active nines and selection persists to the next coefficient whenever that coefficient is nine. `cutsOf` explicitly realizes every such mask. Coefficients are bounded by 18; symmetry and canonicality are not required. Finite cuts are the existing nonempty-block partition semantics; the cut bit at zero is immaterial.

The future mass-range extension is not yet implemented. The product formula for the number of masks is also not a completed Lean claim. No temporal regeneration, infinite safe orbit, or P196 conclusion follows.

Rebuild from repository root:

```
python3 proofs/contributions/agent-123/check.py /absolute/path/to/lean-4.19.0/bin/lean
```

The checker uses an empty temporary directory, copies the four pinned source dependencies, compiles every module, and audits each exported theorem's transitive axioms. Only propext, Classical.choice and Quot.sound are permitted. A second run by the same author is not independent review.

Operational evidence: local Git DNS failed, no Lean initially installed. Reused source artifact 11986920772 and runtime artifact 11948836175; subsequent local execution calls returned ClientError, so no local Lean execution is claimed. GitHub Actions is the actual execution route. Bootstrap run 38764593899 failed before Lean because an empty AGENTS.md search caused shell pipefail; commit 5973d5b fixed this. All revisions, including failed proof candidates, are retained in branch history. Runtime downloads, compiled objects and duplicate temporary build trees are reproducible infrastructure excluded from research publication.

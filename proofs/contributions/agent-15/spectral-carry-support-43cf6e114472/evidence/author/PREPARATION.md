# Preparation events, separate from Lean proof attempts

## Initially absent spectral working-tree paths

The first dependency inspection attempted to read `SourceFormula.lean` and `ChargeSymmetry.lean` under:

```text
/dev/shm/p196-agent15-43cf6e114472/support-repo/proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/
```

The preserved visible `ChargeSymmetry.lean` tool result was:

```text
Command: cat '/dev/shm/p196-agent15-43cf6e114472/support-repo/proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/ChargeSymmetry.lean'
Exit code: 1
cat: /dev/shm/p196-agent15-43cf6e114472/support-repo/proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/ChargeSymmetry.lean: No such file or directory
```

The combined tool display was truncated; this note does not reconstruct unretained portions of that display as new execution evidence. The complete tool invocation remains in the session transcript.

A focused file search confirmed that this checkout initially had no spectral Lean source in that contribution path. A read-only search then located the frozen files in the neighboring authorized `repo` checkout. The coordinator subsequently reported that switching the sparse checkout to the new contribution branch had removed these paths from the working-tree view without changing their Git objects. The coordinator materialized all four source files from the protected PR145 pin and verified their frozen hashes.

The author used the resulting files from `support-repo` and independently compared their byte hashes with the pinned Git object identities before copying them only into the owned author build directory. Source metadata and exact read-only pin queries are in `dependency-build-0002/source-records.json`.

No Lean compiler invocation occurred in the failed path lookup. This was a source-location preparation event, not a target proof failure or a missing mathematical dependency. No existing source, Git reference, or access-control instruction was changed by the author to resolve it.

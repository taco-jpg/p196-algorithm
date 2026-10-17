# Preserved initial wiring-checker diagnostic

This is an additive preservation record. The exact adoption wiring PASS and the eight previously sealed independent-review artifacts remain unchanged. This record is not another acceptance gate and contains no new Lean, verifier, generator, graph-enumerator, or failed-checker execution.

## What is original and what is reconstructed

`initial-failure-tool-output.txt` is a verbatim transcription of the actual traceback text returned by the earlier `tools.exec_command` call and forwarded through `text(r.output)` in this conversation. It was not saved as a separate filesystem log at the time. Its content comes from the retained actual tool response, not a simulated error or a rerun. No execution timestamp or numeric process exit code is invented; those fields were not forwarded in that earlier displayed response. `recorded-command.json` preserves the actual earlier command arguments and that provenance limitation.

`initial-checker.RECONSTRUCTED.py` is reconstructed from the unchanged final checker by reversing its one recorded edit, using the actual initial apply-patch input and corrective apply-patch input retained in the conversation. It is not represented as a previously saved original filesystem file. The reconstruction restores the single initial assertion at line 179, which matches the actual traceback. `initial-to-qualified-checker.patch` records the exact difference from that reconstructed initial variant to the sealed qualified checker. Neither variant was executed for this preservation task.

## Cause and scope

The initial assertion counted every byte occurrence of `prefix` in the original WIP, including the retained historical comment, and therefore failed before producing the completed JSON check. That was an error in this independent checker's first assertion, not a defect in the proposed source repair. The corrected assertion counts the four escaped identifiers in the proposed WIP and verifies that unescaping exactly those occurrences recovers all original bytes. The original comment remains unchanged. No proposed source, patch, registry, proof or execution record changed to satisfy the assertion.

The subsequently successful static check and the sealed report already recorded that correction. This directory preserves the original failed diagnostic more explicitly, as requested, without repeating any review or changing its conclusion.

`PRESERVATION_MANIFEST.json` records the newly preserved files and confirms byte identity of all eight previously sealed artifacts before and after this additive write. Hashes of the reconstructed initial script identify this reconstruction; they are not a claim that a historical on-disk hash had been recorded at the time.

# Interrupted production verification checkpoint

The production checker was stopped with Ctrl-C (process exit 130) at the user’s request to finish publication. Exactly 15 modules had recorded successful fresh builds: `LychrelDigitSums`, `ScalarClock`, `ActualScalar`, `ScalarOrbit`, `PrefixExtension`, `ActualPrefixLift`, `FiniteGraph`, `RankRows`, `JobCatalog`, and `JobData0` through `JobData5`. `JobData6` was interrupted and is not accepted. No production `JobChecks` module ran.

The original manifest is retained byte for byte. Its `RUNNING` status describes the last atomic write before interruption; `checkpoint.json` supplies the subsequent stop record. After stopping, every completed module’s recorded source, object, log, and direct dependency hashes was checked again without compilation. This confirms the preserved successful subset, not the full endpoint.

`sources-and-logs.tar.gz` contains all 47 source snapshots and all 16 logs from this isolated build, including the interrupted module’s log. No compiled object or runtime binary is included. Exact archive members and hashes are listed in `checkpoint.json`. Original matching objects remain in the local build directory for guarded resume; the text archive alone cannot justify object reuse.

The 659-vertex and 94/98-period numerical endpoints remain unaccepted. Remaining obligations are the rest of the data modules, all finite row checks, structural/final hierarchy composition, root transport and period endpoints, followed by the full axiom and provenance audit. See the package README for fresh-build and resume commands.

# Round 6 design: reachdisk (external-memory exact reachability)

## Why
reachmt keeps the whole visited set in RAM (~33-40 B per orbit with ROT=1). The four TOO_BIG tasks need more than the
380 GB round-5 budget allows, and round 6 caps RSS at 200 GB (another service holds ~70 GB). The visited set must live on disk.

## Semantics (must match reachmt exactly)
- Same expansion (Expander: same cell rule, same root rule "cell 0 >= 1", same canon() under ROT=1), same targets
  (ALL: every uniform band whose period divides T, every phase; plus the 9-wire streams), same output lines.
- Layer = height. Layer h+1 = successors of layer h that are not visited before. RESULT COMPLETE when layer h+1 is empty.
- Counts are interfaces (ROT=0) or orbits (ROT=1), as in reachmt.

## Layer step (height h)
1. Generate candidates: expand every key of frontier h-1 (height h). Each successor is hashed into one of PB = 1024
   buckets (top PBITS bits of khash) and appended to cand_b.bin. Targets/streams are checked here (checkNew), for every
   candidate, not only for new keys. The first height at which a target or stream appears is the same as in reachmt.
2. Merge per bucket b (buckets in parallel):
   a. read cand_b.bin into RAM, sort, unique (one bucket of candidates is in RAM at a time);
   b. subtract base_b.bin (sorted, unique) and delta_b.bin (sorted, unique) by a streaming two-pointer pass:
      what is left is the new frontier of bucket b;
   c. write the new frontier front_h_b.bin (sorted), append it to delta_b (sorted merge into delta_b.tmp, then rename);
   d. compaction: when delta has more than base/4 keys, merge base and delta into base.tmp, rename, empty delta.
3. Sum the new keys. Zero = COMPLETE. Visited = sum of base + delta. Visited > cap = TOO_BIG.
4. Checkpoint: manifest.txt (layer, visited, targets' heights, streams, parameters) written to a tmp file and renamed.
   The manifest is written after all bucket files of the layer are final. On restart with identical parameters the run
   resumes from front_{layer}_b.bin.

## Cost
Per layer the dedup pass reads all of base_b (about the visited set) once and writes base only at compaction, so the IO
per layer is about V reads plus V/4 writes amortized. The RAM is one bucket of candidates per thread plus 1024 small
write buffers per thread (about 8 MB per thread). RSS is far below the 200 GB limit; the disk is the binding resource.

## Disk policy
- Work directory per task: ~/p196_run/r6/T{T}_{clock}/ on studio (same volume as the rest of the Mac data, 1.3 TB free).
- Guard: stop with TOO_BIG (disk) if free space falls under 15% of the volume (checked each layer).
- Scratch files (cand_*, old front_*, *.tmp, the replaced base/delta) are deleted by the tool as they are consumed. This
  deviates from "move to _to_delete/" because moving does not free space and the visited set is hundreds of GB. Logged in
  DECISIONS.md. Result files and the manifest are kept.

## Validation (before any production run)
Reproduce exactly (orbit/interface counts, heights, targets, streams):
- clock 01, T=8: 61248 orbits, ROT=1; 244784 interfaces with ROT=0 (calib.sh)
- clock 0001, T=12: 45570 orbits (ROT=1), streams 3 at height 53 (ROT=0: 136652 interfaces)
- clock 01, T=16 (ROT=1): 257,093,986 orbits, frontier empty at height 592
- base 13, clock 1010010000, T=10: band {8,16} phase 0 at height 55, phase 1 at 75; 250301 interfaces
- plus calib.sh in full.
Any mismatch is fixed before continuing.

## Phase C order (production)
1. T=24 clock 0001 (ROT=1). Check: the period-12 stream appears at height 53, twice. Rotate each 9-wire stream to clock
   1000 alignment and compare with the two streams listed in the task.
2. T=24 clock 01. 3. T=29, T=30 two tasks. 4. T=31, T=32 heavy (resumable from sweep).

## Optional pruning (not built in this round)
A coarse abstraction that proves "not reachable" could skip work, but it is optional and not needed for the decision.
It is deferred to round 7 unless the exact run is too slow.

## Labels
COMPLETE / EMPTY = COMPUTED. TOO_BIG / TIMEOUT / disk guard = UNDECIDED. A band fit is a candidate only after replay.

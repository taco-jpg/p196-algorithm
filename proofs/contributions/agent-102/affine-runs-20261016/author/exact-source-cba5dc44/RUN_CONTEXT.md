# Preserved source-pinned replay before Git alignment

All seven source modules and the original verifier module-origin audit returned 0.
However, before this run, the ordinary partial-clone mixed reset could not fetch
public blob abda251432ec4fffdff064c0eb796141c7ff2dc4 through the unavailable sandbox
proxy. Local HEAD therefore remained a3329eda74fc419d76c185fa843d9e6e1602a09b.
The attempted directory name anticipated cba5dc44; it is not evidence that HEAD
was that commit. This report is retained as a source-SHA-pinned replay only.
A separate replay after the approved Git alignment will establish the exact
published-commit result. No proof source or verifier rule changed in this repair.

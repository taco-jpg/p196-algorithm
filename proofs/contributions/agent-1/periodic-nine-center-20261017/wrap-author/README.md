# CenterWrap author evidence

Frozen source: `proofs/Agent1PeriodicCenterWrap.lean`.

The single public endpoint `stripPeriodCenter_wrap w K hw` proves that the existing strip operation on `w ++ K ++ w.reverse` equals the exact stripped residual of K with count increased by one. Only w≠[] is required; K may be empty, asymmetric, already wrapped, or arbitrary, and w need not be primitive. No original recursion, empty-period convention, global rewrite attribute, or inherited proof is changed.

The private `centerAux_extraFuel` proves equality of the original loop with extra fuel once fuel≥input length. Its zero-fuel case forces an empty middle and uses nonempty w to rule out another wrapper. Its successful recursive case uses the existing strict middle-length decrease. The public proof unfolds the wrapper once, then compares remaining fuel `K.length+(2*w.length-1)` with `K.length`. It is a prerequisite for an exact nine-center residual map, with no descent/no-return or cycle-discovery claim.

Both actual author attempts are retained and passed. Attempt001 is the first strict source pass; attempt002 recompiles the identical source and performs the full new-module origin audit. The audit checks all6 theorem constants, including private/generated declarations; there are0 safe definitions,0 opaques,0 unsafe runtime implementations or custom axioms. Recursive axiom union is exactly propext and Quot.sound. The sole public type and its axioms are printed literally.

Official Lean4.19.0 commit6caaee842e94, explicit `--trust=0 -j1 -DElab.async=false`, one CPU,4GiB virtual-address limit and600-second timeout per process. Dependency objects are reused only after exact current/snapshot source hashes and object hashes are checked against the frozen NineCycle registry and parent fresh34 evidence. This is incremental author verification, not a new fresh full-closure build. Parent/independent combined verification remains downstream. Exact timing/resource use and every dependency pin are in attempt002 commands.json/dependencies.json.

The accepted source is byte-identical to both passed snapshots. No Git mutation or external message was performed by this author. Local object binaries are excluded from the publication manifest, with source/object hashes retained in the receipt.

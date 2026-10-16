# Actual all-base overflow births

Status: CLAIMED / WIP. No new theorem has yet been accepted.

Agent #7 owns the narrow task `agent7-allbase-overflow-births-20261016`, successfully published at coordination commit `cc9c01d128808d9c0b2b1cf3921a76f7c00e9cf1` and read back exactly. The prior proposal is issue #61 comment 6225127019.

For every integer base b >= 2, the target combines the existing actual computed-carry semantics with the adjacent-column overflow zero/maximal birth classification. It covers the actual output width L+1, shifted reflection index L-i, four complete interior cases for each extreme, the necessary old neutral neighbor for a new extreme, and exact endpoints including the binary exception. Canonical one-step numeral arithmetic will reuse `ReverseAdd.reverse_add_normalization` unchanged.

The scope excludes run population, growth, ancestry, lifetime, new orbit semantics, infinite avoidance, and any conclusion for 196. Exact proposed statements and exclusions are in SCOPE.json. The scope/ directory retains the prior read-only ownership and API scouts; the proposal Lean file is comments only.

The dependencies/ directory preserves eight original source modules byte-for-byte, with original commits, paths, Git blobs, SHA256 hashes and module identities in SOURCE_PINS.json. These are source pins, not new author proofs. All new accepted endpoints will require Lean 4.19.0 compilation, full transitive axiom auditing and independent semantic review.

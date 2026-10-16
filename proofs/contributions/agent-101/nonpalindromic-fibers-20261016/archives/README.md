# Complete generic seven-module verification evidence

`generic-verification.tar.gz` retains 41 original files without changing their
bytes: the canonical published-source seven-module build and 1,000-theorem
audit, the separate full trust-zero review, all 32 public declarations and
48 compiled logical declarations, 19 independent boundary checks, and the
initial rejected implementation-symbol audit classification.

Archive SHA256:
`6aaa2a53fa4d8490c37b974304b3a0bc24a3cbea82eeba682674e0d73d2c3250`.
The companion manifest gives every original repo-relative path, byte length
and SHA256. The validation receipt confirms all 41 archived members match.
No `.olean`, `.ilean` or build cache is included, and original files were
retained locally when packaging.

To recover, first check the SHA256 above and inspect the manifest. Extract the
archive with `tar -xzf generic-verification.tar.gz -C <empty-directory>`.
Members retain their complete `proofs/contributions/agent-101/...` paths.
Use the recovered report and its exact source pins to replay with Lean 4.19.0.
The root contribution README records the distinction between author checking,
independent review, the canonical verifier, and integration.

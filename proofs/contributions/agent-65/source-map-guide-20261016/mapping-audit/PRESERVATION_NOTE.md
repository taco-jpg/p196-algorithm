# Preservation of the complete original preparation failure

This is a preservation-only addition. The original complete structured tool result remained visible in the author's conversation context and was not truncated. Its full `output` string and metadata values have now been retained in [preparation-failure-original.json](preparation-failure-original.json).

## Source and provenance

- Original tool: `tools.exec_command`, returned through `functions.exec`.
- Original tool result chunk ID: `1faac1`.
- Original process exit code: `1`.
- Original reported wall time: `2.0882e-05` seconds.
- Original reported token count: `211`.
- Original operation: a read-only inline Python schema-inspection probe in the authorized isolated checkout, before the audit script was created.
- The failure was a Python parse-time `SyntaxError` on stdin line 6. No source-map read occurred in that failed parse.

The JSON values, including the complete combined `output` text with its diagnostic line, indentation, caret, and final newline, were faithfully transcribed from that original still-visible result. This file is a fresh JSON serialization of the original structured result; its JSON indentation is not represented as an original transport-byte capture. The complete original output string is preserved without truncation. The tool did not expose separate stdout and stderr fields for this result, so no original per-stream separation is invented.

## Content identities

| Content | Bytes | SHA-256 |
|---|---:|---|
| `preparation-failure-original.json` | 976 | `31e4bd1b543c1afb951080d8b514f9d80cd809e721dc43240b9d9b536e88cd17` |
| Decoded original UTF-8 `output` value | 842 | `bbe7aead41e917e167c269fa146453d7e2d159b258188edf49ec232c167796d9` |

The earlier [preparation.json](preparation.json) truthfully said that it retained only an excerpt; it remains unchanged. This addition supplies the complete recoverable original structured result. The audit report, script, results, prior receipt, and `AUDIT_ARTIFACTS.json` remain frozen. The parent may include this addition and this note in its final outer manifest.

No command was rerun to reproduce the failure. No new audit test, source repair, mapped-blob fetch, index/ref change, or modification to a frozen file occurred. Absolute paths in execution records remain raw provenance rather than editorial navigation.

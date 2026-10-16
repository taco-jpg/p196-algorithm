# Repository write rules

Keep only one canonical working branch, `main`; excluded agent branches are retained separately without modification. Only one integration writer is allowed at a time. Other research must use local workspaces and patches containing provenance, actual files, and verification records; do not automatically create permanent remote branches for individual agents.

Current source lives directly in `proofs`; historical research lives in `proofs/archive`; computational products live in `calculation`. Do not delete original research, overwrite conflicting versions, alter historical evidence classifications, or rewrite published Git history. Preserve the original version before updating a current file. Before retiring another branch, verify its exact tip, complete contents and history, preservation tags, recoverable backups, and remote state.

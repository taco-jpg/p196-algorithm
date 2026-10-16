# Agent 108: fixed-window weight formalization

This contribution formalizes the unpadded sliding-window weight argument in FOLDED_WEIGHT_OBSTRUCTION.md section 3 (original Git blob 6979703055d0f61b7997355b5e00a92a66ed3ce7). Agent13 retains the actual binary/buffered family and coefficient-product results. The new task owns window products, endpoint truncation and their weight consequences.

## Current checkpoint

Agent108WindowDefs and Agent108WindowProducts compile under pinned Lean4.19.0 with --trust=0. windows_append_overlap gives exact concatenation across an overlap of width d-1; windows_eq_range_map identifies the literal complete unpadded windows; windows_length gives their exact number. The author axiom reports contain only propext and Quot.sound. author-checkpoint-01.json pins exact source and successful logs; earlier failed source/logs are retained as historical development, outside any accepted build. Independent review is pending.

The full weighted identity, boundary constant and actual incoming-operator conclusion remain WIP. In particular, an unavailable Agent13 buffered arithmetic interface will remain an explicit hypothesis until its checked original source is recovered. No all-time seed or 196 conclusion, global accepted-index update, or main integration is claimed.

## Reproduce the current source

In a fresh output directory, compile Agent108WindowDefs.lean then Agent108WindowProducts.lean with the pinned Lean executable and --trust=0, passing the output directory as LEAN_PATH. Both modules currently need only Std. Build products and official toolchain installations are reproducible infrastructure and are not published. All substantive failed attempts, source, successful compiler logs and axiom output are retained.

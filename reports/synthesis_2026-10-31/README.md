# Synthesis audit publication — 2026-10-31

**Decimal Lychrel existence: UNDECIDED.** Five synthesis reports are consolidated into source-linked proof obligations 和 corrections.

| File | Content |
|---|---|
| [SYNTHESIS.md](SYNTHESIS.md) | Certificate bridges, exact T12 target, recovered connections, scope limits, 和 required Lean gate |
| [Y13_CORRECTION.md](Y13_CORRECTION.md) | Missing repunit factor; broad counterexample 和 restricted-claim limitation |
| [LATTICE_BOUNDARY_CORRECTION.md](LATTICE_BOUNDARY_CORRECTION.md) | Genuine overflow edge omitted by the old graph |
| [reproduce.py](reproduce.py) | Standalone standard-library checks for both counterexamples 和 the port comparisons |
| [evidence.json](evidence.json) | Exact expected outputs, source identities, 和 scope |

Reproduce from the repository root:

```sh
python3 reports/synthesis_2026-10-31/reproduce.py
python3 -O reports/synthesis_2026-10-31/reproduce.py
```

The checks use explicit exceptions; optimization does 不 disable verification. Outputs must report `PASS`. The checker performs only small exact arithmetic 和 string comparisons. It does 不 replay the large graph searches or prove decimal existence.

Primary source snapshot: [95edd48c10119b35ba9d4775d790f815596afde3](https://github.com/taco-jpg/p196-algorithm/tree/95edd48c10119b35ba9d4775d790f815596afde3). Related discussions: [#480](https://github.com/taco-jpg/p196-algorithm/issues/480), [#478](https://github.com/taco-jpg/p196-algorithm/issues/478), 和 [#479](https://github.com/taco-jpg/p196-algorithm/issues/479).

No Lean source changes. Existing formal theorems retain their original verification provenance; the publication makes no fresh kernel-verification claim. Future Lean changes require the strict gate recorded in SYNTHESIS.md.

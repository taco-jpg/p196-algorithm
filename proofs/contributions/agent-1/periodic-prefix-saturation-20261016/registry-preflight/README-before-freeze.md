# Prefix saturation registry preflight

This contribution's scoped registry will be generated from the actual imports
of `Agent1PeriodicInitialUnsaturated`, including the new Prefix and Saturation
modules. The preflight changes no mathematical source, accepted global
registry, Git state, or external service and executes no Lean.

The accepted claim was read using the GitHub contents API at
`8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2`. Its actual intended sources are
the three new modules, `Agent1PeriodicInitialUnsaturated.registry.json`, and
this contribution directory. The original claim and successful read receipt
are retained. `query-history/` preserves incidental task-directory prefix
matches; those records are not claims or dependencies for this contribution.

The constituent published commits were resolved by the read-only API:

- ReturnClock: `ebcaf723d61f9513c8bae30440d02ba4a46343b4`.
- ReturnCore: `946c69edf3d2e6a87f5516db1fd0091eae29e663`.

`baseline-readback.json` preserves both actual commands and responses. The
root subsequently confirmed publication of the combined foundation
`84a65f296625e16851b4a369e27ffca43aaea40c` in its WIP checkpoint; a separate
read-only commit API call confirmed the exact combined identity. This is now
the registry source baseline, with both constituent commits retained.
`baseline-readback-initial.json` preserves the earlier two-commit record.
No future final proof publication commit is assumed.

The inherited registries are ReturnClock, ReturnCore, and the exact
`Agent2SaturatedProfile.registry.json`. Their union has 55 logical modules;
21 duplicate encounters match source SHA-256, Git blob ID, and imports. Every
used path's actual source bytes were checked. This preliminary union count is
not yet a claim about a new root's import closure or a Lean execution result.

One logical module has two physical paths: `LychrelDigitSums` is mapped to
`proofs/LychrelDigitSums__75febdc48f0ca802.lean` by Clock/Core and
`proofs/LychrelDigitSums__0810ace083af80c5.lean` by the saturated-profile
registry. Both source files are byte-identical, with SHA-256
`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`
and Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`. The combined
registry selects the Clock/Core path and records the checked alternate path.
All saturation aliases, including `SaturationCertificate`, come directly from
the original Agent2 registry; no same-named historical alternative is guessed.

Once all three actual sources exist, run from the worktree root:

```
python3 proofs/contributions/agent-1/periodic-prefix-saturation-20261016/registry-preflight/prepare.py run-001
```

Every run requires a new directory, preserves the three source snapshots,
script, generated registry and report, and checks that source bytes remained
stable during the snapshot. The script independently parses the actual
imports, checks inherited pins, extracts actual public theorem names, and
masks comments/strings before scanning executable source for prohibited proof
shortcuts. Lean's own `Std`, `Init`, and `Lean.*` modules are toolchain imports,
not project modules or guessed aliases.

The default output is explicitly provisional. Final registry freeze requires
actual confirmations from all three authors, checked strict compile receipts,
complete new-module axiom audits, and a fresh `--author-checked` preflight run.
That metadata stage still labels the combined fresh build and independent
review as pending. Source inspection and reused author objects are not a
fresh dependency rebuild.

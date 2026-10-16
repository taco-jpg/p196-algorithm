# Normalized certificate carry: scoped source and ownership census

## Decision

No equivalent exported theorem identifying the original native carry before and after maximal phase-suffix removal, or identifying `overflowBit (stateOuter s)` with the original checker `gam s`, was found in the inspected source. There is no unresolved overlapping task within the claim records and branch sources listed below.

The useful next file is an attributed consumer of existing normalization and accounting facts. In particular, `Agent109.norm_band_tail`, `Agent109.norm_append`, and `Agent109.Outer.stripSuffix_spec` already supply the constant-band and decomposition machinery. They should be reused. The new interface does not need a second repeated-block normalization proof.

**This is a read-only census. The candidate statements remain unproved and unclaimed here. Parent alone performs the fresh guarded claim and authorizes proof work.**

## Proposed narrow interface

The structural endpoint can use either of these sufficient hypotheses:

- For arbitrary finite natural coefficient words B, `c ≤ 18` implies `overflow c (stripSuffix c B) = overflow c B`.
- For arbitrary natural phase c, `Bounded B` implies the same equality. When c exceeds 18, bounded B contains no c and the stripping operation changes nothing.

The intended consumer is:

```lean
-- Unproved source-design target; no theorem declared by this census.
∀ s : Agent109.Cert.State, Agent109.Bounded s.B →
  Agent6.ExteriorCoordinates.overflowBit
    (Agent116.CertificateExterior.stateOuter s) =
      Agent109.Cert.gam s
```

The only state-level hypothesis proposed is bounded B. Phase, nonneutrality, evenness, positive head, nonempty B, realization and checker acceptance need not be imposed. The numerical carry bound is still required to turn the nonzero indicator into the carry value.

This would replace the normalized-row indicator sum in the published `checked_row_weighted_balance` by the existing `Agent110.Accounting.totalGam`. The weighted equality keeps its original `check cert = true` premise. The optional gain form merely substitutes the already exported `totalGam_eq_twice_gains`; it is not a new gain theorem or an overflow-existence result.

The claims specialist's companion packet, `claims-agent6/next-gam-scout/REPORT.md`, records exact declaration statements, phase/empty-word controls, and complete 8/16/18-module dependency closures.

## Exact inspected source scope

The main-source census is pinned at `7b9e663b3c40aadfd7038f264729f6b7e3c7ce88`. Its nonrecursive proofs tree is `a03b4ee19ac0072eabe4e02afbd77dbc8f609002`; the contribution subtree is `c073c389b479fe00372156f5f2d45af9454ede59`. Both tree responses were complete.

All 1,831 top-level Lean paths were covered by exact source-blob matches or direct source reads. The 17 new top-level blobs are Agent1 repeated-block, Agent2 overflow-fiber, Agent100 GroupII and Agent101 multiplicity modules. A further 31 distinct public contribution-source blobs were fetched, source-pinned and scanned, including the new Agent3, Agent5, Agent7, Agent8 and Agent9 modules. Unrelated preserved development attempts, probes and audit files in those new contribution trees were explicitly excluded. A source search is not a kernel acceptance audit.

The initial local declaration census read 1,935 paths and deduplicated them into 1,463 source blobs. It checked exact export-name patterns and then inspected files containing native suffix/state projection identifiers alongside carry/overflow identifiers. The relevant existing declarations were read directly. No public native carry/strip or absent-coefficient strip identity was found. General List facts may still discharge the latter without adding a standalone theorem.

### Relevant surviving branch sources

| Branch or source | Exact pin | Finding |
| --- | --- | --- |
| Agent109 exterior bridge | branch 5808b992; OuterBridge blob06ed5a8660e83b2dde192a10c822c9317a79483b | Identical existing normalizer correspondence and suffix decomposition; no exported carry/strip equality. |
| Agent109 OuterCompat | blob7fe45eb71a1d4381c6c750e943d1740229eb1b61 | Only the cap-two ordinary exit consumer. |
| Agent216 correspondence | branch d3766fee; ConcreteEdge blob64f966cc95346316ba9fa229b231dd99f2cd2dc0 | Two concrete edge/zero controls; no universal coercion or normalized-carry theorem. Its general correspondence task remains owned. |
| Agent1 periodic outer stripping | branch bf4ff749; blob9e35c06bf3dd393f33dfd2af965a1ea2d4305bc7 | Complete-block suffix reconstruction, maximality, length and boundedness; separate operator, no native carry equality. |
| Agent115 rho work | PR107 pin 254b4bc6; Targets 9485759ed79424207ca97fab3e8ad7a5c6b47e89; Lemmas ecb978e22270787adacd4dbdd48b50519e14085c | Native Outer rho/carry formula only; no original checker gam or stateOuter interface. Separate PR107 packet preserves exact source and CI failures. |
| Agent5 new absorption source | InitialValidity adfcc154d43683fa8c07a6a9306f1aa734649f3b; FiniteOverflow 308e479acdce02c5c15117f88395bba1f8f392ef | Int-word suffix boundedness and headD preservation, not carry/strip equality. |

This is a scoped negative finding, **not** an exhaustive theorem-equivalence certificate over every branch or every preserved experiment.105 branch heads were enumerated, not all branch bodies reviewed.

## Ownership scope

The current census contains 132 task pins at coordination `32b2f562b54f5d14ce0d45ed2fd5368fa8cd8004`. Nine additional nearby task payloads were read in full and byte-checked in this packet. The claims specialist separately preserves the Agent216/411/412, Agent110/115 and Agent6 task payloads and exact interface inventory.

Agent1 retains repeated-block normalization, periodic stripping and validity. Agent4's normalization-support task explicitly concerns the Int/Nat correspondence already owned by Agent216; its separate legacy decimal transport concerns Int-valued General/Agent5 trajectories. Agent421/422 scopes concern numeric same-carry representatives, complete digit schedules and protected-run normalization. Agent411 retains native charge transport and general-domain closure. Agent412 retains its charge/interface residues and period exclusions. None of these inspected targets claims the proposed original Agent109-to-Agent116-to-Agent6 normalized carry/accounting consumer.

Agent115 retains rho recurrence, positive flow, the rho telescope and compulsory cycle overflow. The proposed carry/accounting bridge excludes those targets.

Parent subsequently reported main `dff1bf97d7c6920fcf60ee9ea1af32338adc1f17`, which adds own PR90 and Agent1 PR94 beyond this fixed main pin, and reviewed PR115 head `dca30e76474569a276c2e58bbd6ee0b96c554ecc`. Parent owns that final main/claim delta check. This packet does not silently relabel its older source snapshot as the newer head.

## Evidence files

- `remote-main-lean-tree.json`, `remote-contribution-lean-tree.json`: exact complete source path/blob inventories.
- `remote-branches.json`, `remote-task-pins.json`: 105 branch heads and 132 task pins.
- `local-declaration-census.json`: deduplicated source and relevant declaration candidates.
- `new-source-pins.json`, `new-source-integrity.json`: 17 new main sources, two branch sources and nine nearby claim payloads.
- `additional-source-pins.json`: 31 further main-source blobs plus Agent1 periodic stripping, with exact identifier matches.
- `all-main-source-coverage.json`, `FINAL_RECEIPT.json`: final source coverage, explicit remaining preserved experiment paths, byte checks and report hash.

All written captures are confined to this scratch evidence directory. No original source, Git ref, remote message, claim or proof was changed by the scout.

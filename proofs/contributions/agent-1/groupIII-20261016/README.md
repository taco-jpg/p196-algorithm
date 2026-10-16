# Group III delayed overlap — Agent #1

Status: **LEAN-CHECKED**, independent full rebuild pending at this source checkpoint. The two final modules compile under Lean4.19.0 with --trust=0. All27 public axiom prints and the author audit of471 new-module theorem declarations contain only propext, Classical.choice, and Quot.sound. Original six dependency modules are unchanged.

For every r>=1, p=1..4, u=10..13, v in {5,6}, u+v<=18, the original coefficient word initial r p u v genuinely leaves independent overlap after its first step, returns after its second step to shiftOne(returnedComponent r p u v), and keeps width2*r+7. For every canonical ordinary integer realizing the initial word, both first and second positive reverse-add outputs are nonpalindromic; the second output has that exact pair word. A positive realization exists for every permitted tuple. The r=1 adjacent-support boundary is included.

Main endpoints: P196.Agent1.GroupIII.numeric_delayed_return and realized_safe_gate; core component_two_step_return, whole_two_step_return, actual_intermediate_overlap_fails. This completes the written seven-core GroupIII branch, not a recurrent or all-time safe family. No GroupII, later-hit timing, infinite orbit or196 claim.

Reproduce with the unchanged scoped verifier:

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --registry proofs/Agent1GroupIII.registry.json --project agent1-groupIII --lean /path/to/lean-4.19.0/bin/lean --output /tmp/groupIII-fresh
```

Sources, failed and repaired attempts and author audit are retained in author/. Exact domain/provenance are in SCOPE.md. Independent finite controls are diagnostics only; the all-parameter claims rest on Lean. Parent Agent1 is sole Git writer; specialist verification_plan authors source; numeric_bridge_review independently reviews arithmetic and rebuilds. Claim2cb89418916f1d0a22813028d5fea623e80900ad, issue61 receipts6224749698/6224930794. No main-write slot.

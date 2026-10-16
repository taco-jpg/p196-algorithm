# Exact period-block stripping — Agent #1

Status: **INDEPENDENTLY-REVIEWED.** Separate fresh14module --trust=0 replay passed1,343 theorem constants and all26 new named theorem exports. All67 named new/prerequisite theorem prints passed; only the standard three logical axioms. Independent semantic review found no unresolved correctness issue. Parent canonical fresh14module replay also passed. All three source modules compile with Lean4.19.0 --trust=0. Literal exports use only propext, Classical.choice, Quot.sound. Source is frozen and pinned in proofs/Agent1PeriodicQuotient.registry.json. Author increments and clean dependency builds are distinguished explicitly; the combined independent and parent rebuilds both passed, with explicit final publication/source receipts.

The executable stripPeriodSuffix and stripPeriodCenter implement the original full-period removal loops, with exact decomposition, maximal stopping conditions, proved sufficiency of input-length fuel, and an explicit harmless empty-period convention. Center test_iff matches the original nonoverlapping length/prefix/reverse-suffix check. Nonprimitive periods and empty remainders are included.

quotient_step_bounded now supplies the unconditional exact algorithm endpoint: for bounded B,H,w, length(w)=4, k>=3, the original stepWord(periodicWord B H w k) equals periodicWord of the computed stripped outer/center/rawPeriod with exponent(k-2)+outerPeriods+centerPeriods. No stripping premise remains. quotient_width_balance proves2*len(B')+len(H')+8*delta=2*len(B)+len(H)+rawGamma over Int; quotient_exponent_accounting gives positive natural output exponent and its agreement with k+delta. quotient_irreducible proves both stopping conditions.

Full ValidPeriodic, safety preservation, interface search, cycles and infinite lift remain outside scope. The historical finite-interface lift owner is not displaced. Original Python/METHOD sources and scope checks are pinned in SOURCE_SCOPE.md and OWNERSHIP_SCOPE.md. PR95 source95a17cee is preserved as exact dependency.

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --registry proofs/Agent1PeriodicQuotient.registry.json --project agent1-periodic-quotient --lean /path/to/lean-4.19.0/bin/lean --output /tmp/periodic-quotient-fresh
```

Claim9f5d2939. ParentAgent1 solely writes Git and authors Quotient; symbolic_scope authors OuterStrip; cap4_existing_theorems authors CenterStrip; research_status separately reviews. No main slot. Finite Python boundary controls are diagnostics only, and all failed Lean attempts are retained outside the accepted root closure.

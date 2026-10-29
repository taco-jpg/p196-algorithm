# AgentN04FoldedRegularInvariant

**PAPER PROOF (format soundness); COMPUTED (finite decimal controls).**
New certificate format: a finite DFA over folded palindromic pairwords, closed under an exact outer-to-inner two-carry finite transducer for reverse-and-add. Any nonempty closed regular language with an odd pair coefficient in every word certifies a Lychrel integer in its base. Unlike a fixed-width centre, it permits asynchronous, moving, unbounded phase interfaces.
PAPER PROOF scope: all bases >=2, canonical numbers with >=2 digits, exact finite transducer and language-closure soundness; no actual decimal closed DFA exhibited.
COMPUTED scope: b9 2880 + b10 3960 exhaustive halfwords (n=2..5), 3000 longer random halfwords per base, zero big-integer discrepancies. Decimal p8/m20: 380 uncorrected relative-phase interfaces through 64 steps, overflow schedule always correct, minimum defect span increases 3/8/17/39 at steps 8/16/32/64. Three independent decimal 64-step, 2000-to-2032-digit big-int controls pass.
Not a decimal Lychrel certificate, not a claim about 196, and not an exclusion of active gliders.
Proof and scope: `reports/AgentN04FoldedRegularInvariant.md`.
Reproduce: `python3 calculation/new_structures/agent-N04/folded_transducer.py`; `python3 calculation/new_structures/agent-N04/phasefront_scan.py`; `python3 calculation/new_structures/agent-N04/independent_replay.py`.
Small data: `calculation/new_structures/agent-N04/{transducer_controls,phasefront_summary,replay_controls}.json`.
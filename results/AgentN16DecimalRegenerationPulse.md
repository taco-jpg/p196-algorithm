# AgentN16DecimalRegenerationPulse
**COMPUTED.** A NEW explicit 28-coefficient centre half-word `C=HEBBBCI8D2545G2HFAHE39AH9IF2` embedded in the decimal p8/m20 seeded pairword `B0 W0^q C reverse(C) reverse(W0)^q reverse(B0)` produces a near-replenishing **one-shot 264-step lattice pulse**.
At q=300, the first 264 steps leave 6,037 matching exterior coefficients (D=2); the empty-centre control has 5,979 (D=60), so this centre preserves **58 additional lattice coefficients** over the CRT-aligned 264-step macrocycle.
Both q=300 and q=301 survive 20,000 true reverse-and-add steps without any palindrome, matching the 8-phase exterior throughout, with independently compared GMP and schoolbook-digit integers at every step.
At q=300: D(528)=61 and D(20,000)=4,487 (the empty-centre control has 4,545). **The pulse is transient, not a periodic certificate**; the centre again consumes ~60 cells per 264 steps.
A separate centre `87FEBC813IFI5D46` emits six exterior cells by t=22 (D=-6) but loses them thereafter; this proves transient outward repair occurs in actual decimal dynamics.
The reproducible 600,000-sample 22/264-step screen followed by 30,000 deterministic mutation refinements discovers the 28-coefficient core; both engines and exact controls included.
Code/data/one-command checks: `calculation/new_structures/agent-N16/regeneration_pulse/`; `sh calculation/new_structures/agent-N16/regeneration_pulse/run.sh`.
Further details: `reports/AgentN16DecimalRegenerationPulse.md`.
**Not claimed:** an infinite Lychrel number, a repeating centre, or sustainable 60-cell-per-cycle regeneration.

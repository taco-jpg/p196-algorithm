# AgentW02P12NestedPulseClock40k
**COMPUTED**, base 10, three explicit 100,000-digit p12/m9 symmetric-packet seeds, all 40,000 reverse-and-add steps; **120,003 ordinary-decimal nonpalindromic states** and 80,002 complete halfword-delta hash agreements with independent carry-engine calculations.
Their rightmost defect fronts translate +33 columns over 76 steps at every t=337..39924 (A) and t=155..39924 (B); final seed length 110,000 digits.
The coefficient immediately behind the rightmost front has a sparse finite defect clock: A has 38 three-step pulses in 19 +76 pairs; B has 70 pulses (64 length3, six length4), with three identical **six-pulse timing patterns** beginning at t=941,18573,39093.
Exceptional-start gaps are 17,632=232*76 and 20,520=270*76, increasing by 2,888=38*76; a three-term finite pattern is NOT an infinite quadratic recurrence.
Full generated trace SHA256 `3942215a5ebadbbc45f1712aa263ef7f24f84411330cd343d8b613ceb25ee3e7`; independent ordinary-digit checker, exact pulse assertions, expected table and corrupted-trace rejection under `calculation/new_structures/agent-W02/`.
Reproduce: `sh calculation/new_structures/agent-W02/run_40k.sh`. Full details: `reports/AgentW02P12NestedPulseClock40k.md`.
This is a NEW finite pulse-clock mechanism with three exceptional episodes, not a bounded soliton, infinite Lychrel certificate, Lean proof, or proof about 196.

# Agent N26 decimal period-8 finite-horizon bulk shield
- **COMPUTED** (not LEAN-VERIFIED, not a base-10 Lychrel certificate).
- Seed family: pairword A ++ reverse(A); A is the rooted 39-column p8/rec0 exterior followed by c copies of its period-20 spatial bulk (phase zero).
- For c=228, the 9,198-digit decimal seed survives 20,000 true reverse-and-add steps with no palindrome, while the first 39 pairword columns match the phase-t mod 8 reference at every time 0..20000.
- For even t the outer pair sum is 17; for odd t the outer decimal digits are 1 and 7. This directly witnesses non-palindromicity throughout the tested horizon.
- First 39-column defect arrival observed at 88c+4 (c=1,2,3,5,10,20,50,100,260), always column 38; positive centre-to-exterior propagation data, not an all-c theorem.
- All source, input data, independent GMP and digit-array checkers, exact commands and controls: calculation/new_structures/agent-N26/.
- Detailed interpretation and scope: reports/AgentN26DecimalP8Shield.md.

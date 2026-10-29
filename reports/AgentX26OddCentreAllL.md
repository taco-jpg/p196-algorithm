# Agent X26: arbitrary-centre odd-band parametric pumping (base 10)

**Status: COMPUTED** for 20,000 exact ordinary-decimal transitions and simultaneous pairword checks; the all-number-of-insertions extension is a **PAPER PROOF** conditional on those checked reference edges. Only the finite horizon t<=20000 is covered.

## Improvement over the fixed-length reference
In AgentX26AdversarialCentreShields the checked base uses an odd 257-digit central word, with exactly L0=22000 nines on each side. This follow-up removes the upper bound on L: for **every integer L>=22000**, and independently for **every C in {0,...,9}^257**, the actual decimal seed
    N0(L,C) = 5 ++ 9^L ++ C ++ 9^L ++ 4
has no palindrome among t=0,...,20000. The initial length is 2L+259 and the t=20000 length is 2L+8533 (the same 8274 overflows). Its pairwords have two coefficient-18 collars of length at least L-t at every t. **Neither L nor C is a function of time in an orbit**; this is not infinite-time survival.

## Sound two-sided pumping lemma (PAPER PROOF)
Let P=pair(D), where pair(D)_i=D_i+D_(n-1-i), and let I9 insert two literal digit 9s at the centre of D. Let I18 similarly insert two literal coefficient 18s at the centre of P. Assume (i) the insertion lies strictly inside a sufficiently long central 9-digit / 18-coefficient band, (ii) carry into the insertion position in the normalization of P is 1, and (iii) the normalized digit word retains a central run of 9s wide enough that moving the insertion index by at most one does not change the word.

Then pair(I9(D))=I18(pair(D)). Carry normalization of I18(P) inserts two 9 output digits with carry unchanged because 18+1=19 at both new sites. In symbols norm(I18(P)) = insert9^2(norm(P),j). The output length is n+gamma; the canonical central index is floor((n+gamma)/2), at most one away from j=floor(n/2). Both insertion points are inside a constant 9-run by condition (iii), hence the two insertions yield identical words. Therefore
    RAA(I9(D)) = I9(RAA(D)).
The same hypotheses persist after adding *any* number m>=0 of central pairs of 9s, since those copies extend the 9/18 band and do not change the carry or the outside digits. This gives exact m-fold commutation, **not merely a check of one extra copy**.

## Finite controls that discharge the hypotheses
The program pump_parametric.cpp performs literal-digit RAA on the two odd-parity reference seeds with L=22000 and L=22001 at all 20,001 time slices. It independently normalizes pairwords and verifies every source and target:
- digits(L+1,t) = I9(digits(L,t));
- pairs(L+1,t) = I18(pairs(L,t));
- step_pair(I18(P_t)) = I18(step_pair(P_t));
- same overflow gamma and actual integer lengths (plus two);
- all coefficients from index floor(n_t/2)-2 through the original high band endpoint 2L0+257 are 18, which guarantees the central 9 and pairword conditions uniformly through t=20000.

The smallest measured distance from the centre to the original right-hand 18-band endpoint was 17,991 sites. This is vastly above the local pumping threshold. Thus the exact algebraic lemma applies at *every* checked base edge, and hence for all integers m=L-22000 by induction on m. At arbitrary L, pairword reference exterior and overflow history are identical, and the 18 band gains 2m central copies.

Finally apply the previously established adversarial-centre carry-box lemma. Its box boundary is ell_t=L+1-t+G_t, with G_20000=8274, and its high collar index is L+257+1+t. The pumped uniform reference has 18 everywhere across the required high and reflected low collars, and retains the same outer nonpalindrome digit witness (maximum index 25). Therefore **all** choices of the central 257 digits are safe through t=20000, with collars of at least L-t. This proves the announced universal finite-horizon family.

## Reproduce
From the repository root:

~~~sh
g++ -std=c++17 -O3 -Wall -Wextra -Werror calculation/new_structures/agent-X26/pump_parametric.cpp -o /tmp/x26_pump
/tmp/x26_pump 22000 20000 257
~~~

The expected six-line output is under calculation/new_structures/agent-X26/pump_checkpoints.tsv; a separate ordinary GNU MP replay of the L22000 Thue-Morse centre and the fixed-L universal carry-box data are in the earlier X26 result. No Lean theorem has been added. A future all-time theorem would still require an autonomous recharge / regenerative centre that prevents the finite band from being exhausted by unbounded t.

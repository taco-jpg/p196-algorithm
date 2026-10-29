# Agent W06: an exact all-length synchronizing buffer lemma

**PAPER PROOF**, for a base-b two-buffer transition under explicit carry guards. This is neither Lean-verified nor a Lychrel certificate.

## General theorem (every integer base b >= 2)

Work with low-digit-first pair coefficients in 0..2b-2. For a block X define F_X(c) as the exit carry (0 or 1) of ordinary base-b normalization with incoming carry c. Let A be nonempty, and let T be a palindromic odd-length coefficient word with even midpoint. Suppose

(1) F_A(0)=1; (2) last(A)>=b and F_reverse(A)(1)=1; (3) first(T)>=b and F_T(1)=1.

For **every L>=1** define two symmetric pairwords

    P_0 = A ++ 0^L ++ T ++ 0^L ++ reverse(A)
    P_q = A ++ (b-1)^L ++ T ++ (b-1)^L ++ reverse(A).

If first(A)>=b, each denotes a valid canonical integer via the standard digit split (min(b-1,p),p-min(b-1,p)), and midpoint coefficient/2. Let N_0,N_q be those integers. **The complete pairwords of their first reverse-add iterates agree, and their second reverse-add iterates are the same integer.** There is no upper bound on L.

## Proof by four impulses

Write a=|A|, m=|T|, n=2a+2L+m. Because F_A(0)=1, each first buffer receives carry 1. A zero buffer emits (1,0,...,0) and exits with 0, while a (b-1) buffer emits only zeros and exits with 1. At first(T)>=b these distinct incoming carries cause a single digit difference of -1 in norm(P_0)-norm(P_q); both become carry 1, so the remainder of T is digitwise identical. By F_T(1)=1 both second buffers receive carry 1, leading to a +1 difference at the first cell of the second buffer. Their outgoing carries 0 and 1 enter reverse(A), whose first coefficient last(A)>=b creates the final -1 digit difference and unifies the outgoing carry at 1. The rest of reverse(A) is identical. By F_reverse(A)(1)=1 each normalized word has length **n+1**.

Thus the **entire** normalized digit difference has exactly four nonzero positions:

    position             a    a+L    a+L+m    a+2L+m
    digit_0 - digit_q   +1    -1       +1       -1

Reflection of the n+1-digit output pairs index i with n-i. In particular, a and a+2L+m pair together; a+L and a+L+m pair together. Both pairs cancel, so the full next pairwords agree at every position. Reverse-add from a number depends only on its current pairword (sum of mirrored digit pairs), hence the next integers are equal. This is a finite carry argument valid for all L, with no finite-horizon extrapolation.

## The exact decimal p8/m20 corollary (including necessity)

Let B and W be the literal rec0 exterior blocks in calculation/new_structures/agent-W06/reset_all_lengths.py, of lengths 39 and 20. For **all** integers k,j>=0 and L>=1, let A=B++W^k, T=W^j++[C]++reverse(W^j), with C in {0,2,4,...,18}. Carry-map checks on those fixed blocks give F_B(0)=1; F_W(0)=F_W(1)=1; F_reverse(B)(0)=F_reverse(B)(1)=1; F_reverse(W)(0)=F_reverse(W)(1)=1; last(B)=last(W)=13; first(W)=17. Therefore the guarded theorem applies exactly when **j>=1 OR C>=10**. In the j>=1 case, the first W in T merges the two entering carry values and the last reverse W exits with carry 1, regardless of C. In j=0,C>=10, T=[C] has the same property.

The condition is **sharp**: when j=0,C<=8, both centre normalizations exit in carry state 0, and the high reverse(A) therefore receives the same carry in both cases. Their first high digits coincide, while the first low buffer digits differ by +1, so the output pairword at index a differs by exactly +1. The full pairwords cannot agree. This decides this entire infinite parameter family, with the same carry-map guards for every k and L.

## Independent computational controls, and what remains open

- Run python3 calculation/new_structures/agent-W06/reset_all_lengths.py: 22,000 distinct exact bounded test cases k=0..10,j=0..3,L=1..50,C even 0..18, another 300 randomized large widths k<=200,j<=50,L<=500, and 30 independent Python BIGINT paired replays. It checks the literal four nonzero difference positions in every successful case and a nonzero mirror-pair witness in every unsuccessful case.
- Run python3 calculation/new_structures/agent-W06/generic_reset_control.py: 7,250 separate randomized guarded cases in bases 2..30, each checking the complete length n+1 output and the four-position identity.
- Separate previous W06 computation: reports/AgentW06HybridHalfGliderReset.md checks 20,000 actual decimal steps and a 44-step/-10 travelling interface. The theorem here certifies a reset/synchronizing **junction**, not a bounded or regenerative centre, and does not prove that any decimal orbit avoids palindromes indefinitely.

The intended next certificate format can quotient two buffer-labelled states by this proven two-step synchronization. A sound infinite-cycle checker still needs a nonshrinking replacement of the inward-moving W wall, the complete normalized template edge, and an all-state nonpalindrome guard. No such cycle is claimed.

# AgentW06AllLengthReset
- **PAPER PROOF:** every base b>=2 has a guarded 0^L vs (b-1)^L two-buffer synchronizer; for **all L>=1**, the full first-step pairwords agree and the full second-step integers coincide.
- Precise guard: F_A(0)=1, last(A)>=b, F_reverse(A)(1)=1, first(T)>=b, F_T(1)=1, T palindromic odd with even midpoint; canonical seeds when first(A)>=b.
- Full proof: only four output digits differ, +1,-1,+1,-1, at two symmetric pairs in the n+1-digit result.
- Decimal p8/m20 corollary: A=B++W^k, T=W^j++[C]++reverse(W^j), all k,j>=0,L>=1, C even 0..18. **PAPER PROOF sharp iff:** reset exactly when j>=1 or C>=10.
- **COMPUTED controls:** 22,000 bounded cases, 300 large random cases, 30 independent BIGINT pairs, 7,250 randomized all-base cases (bases 2..30).
- Reproduce under calculation/new_structures/agent-W06/: reset_all_lengths.py and generic_reset_control.py.
- Complete theorem, proof, and limitations: reports/AgentW06AllLengthReset.md.
- Neither Lean-verified nor a decimal Lychrel/infinite-palindrome-avoidance certificate.

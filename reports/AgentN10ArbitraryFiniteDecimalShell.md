# Constructive arbitrary finite-horizon decimal nonpalindromicity theorem

**Label: PAPER PROOF**, with exact finite coefficient arithmetic cross-checked by two independent COMPUTED programs. The result constructs arbitrarily long *finite* decimal reverse-and-add orbits without palindromes; it is **not** a base-10 Lychrel number.

## Universal eroding-shell rule
Take the already known base-10 period-eight, spatial-period-20 lattice and 39-column exterior `B_t,W_t` (t modulo eight, all words explicit in `calculation/new_structures/agent-N10/phase.json`). All coefficient words are least-significant first and palindromic, with values in 0..18. For any integer r>=1 and any finite palindromic central coefficient word C, define
`P(t,r,C)=B_t ++ W_t^r ++ C ++ reverse(W_t^r) ++ reverse(B_t)`.
Write T for carry-normalization followed by pairing of the resulting digits under reversal, including the possible leading carry as a new digit.

**One-step theorem:** T(P(t,r,C)) has prefix `B_(t+1) ++ W_(t+1)^(r-1)`, the reflected suffix, and the prescribed overflow `g_t=(10101010)[t]`, independently of C. Its unspecified middle is again palindromic. Hence T maps this language into the same language at phase t+1, with the guaranteed band count reduced by at most one.

## Soundness argument
The carry map of every W_t and reverse(W_t) is constant on {0,1} because its coefficient sequence contains a value different from 9. Moreover the input carry from normalizing B_t equals the fixed point of W_t, in every one of the eight concrete phases. Thus normalization of the low exterior is a fixed digit block A_t followed by r copies of a steady 20-digit block U_t. After an arbitrary centre C, its normalized digits D and outgoing carry u are arbitrary. The first high-side reflected W produces a digit block X_(t,u), and all subsequent ones produce a common steady block Y_t. The final reversed B produces Z_t and the phase overflow g_t. The complete normalized word therefore factors exactly as
`A_t ++ U_t^r ++ D ++ X_(t,u) ++ Y_t^(r-1) ++ Z_t ++ [g_t if nonzero]`.
The first 39 paired digits use only the two fixed caps and give B_(t+1). The next r-1 complete 20-column regions pair U_t with the corresponding steady Y_t, yielding exactly W_(t+1). The one exceptional X block and every unknown digit of D occur strictly *inside* that guaranteed exterior. The finite cap/bulk equations hold for all eight phases and both u values; see the symbolic checker. The output pairword is palindromic by construction, so removing the claimed symmetric exterior leaves a palindromic centre. This proves the universal one-step rule for all r and all C, with no search over centre width.

Finite arithmetic audit: `shell_soundness.py` checks 8 phases x 4 sample r x both centre-output carries x 6 lengths of mutually independent symbolic centre-output digits = **384** exact checks, all passing; the general r and C quantifiers follow from the displayed block factorization. Independent `shell_bigint_control.py` tests 8 phases x 4 r x 100 random physically realized decimal integer cores = **3,200** actual `int(s)+int(s[::-1])` computations, all passing.

## Explicit all-horizon nonpalindrome family
Fix arbitrary H>=0 and choose k=H+1, C empty. Start with `P_0=P(0,k,[])`. For each pair coefficient p set the low decimal digit to `floor(p/2)` and its reflected high digit to `p-floor(p/2)`. Because the exterior's first coefficient is 17, the leading digit is 9 and the decimal integer is valid. Its initial digit count is `n_0=78+40k`.

Induct on t=0..H: the actual reverse-and-add iterate has pairword of form `P(t mod 8,k-t,C_t)` for some palindromic C_t. The one-step theorem handles the induction as long as k-t>=1. Every B_t has at least one odd coefficient; the eight odd-coefficient counts are `24,19,16,20,16,9,16,14`. A decimal palindrome has pair coefficients `2d_i`, all even. Therefore no iterate at any t=0..H is a palindrome.

The overflow stream repeats `10101010`, hence `n_t=n_0+ceil(t/2)`. In particular, H=20,000 and k=20,001 yields an explicitly described **800,118-digit** initial decimal integer with a mathematically certified 20,000-step palindrome-free horizon. This is not the economical k=300 numerical example from the preceding result; the latter survives much longer than this conservative universal bound requires.

## Reproduction and Lean plan
```sh
sh calculation/new_structures/agent-N10/run_shell.sh
```
The script regenerates the phase data and runs both independent controls without external packages. A Lean formalization would use `norm_append`, absorbing-band carry fixed points, and a lemma computing the first `39+20(r-1)` pairword coefficients from the above factorization, with eight phase identities discharged by `decide +kernel`. No Lean proof is claimed.

**Critical distinction:** arbitrarily long palindrome-free *finite* orbits do not imply an infinite palindrome-free orbit for any fixed integer. The initial number depends on H, and the guaranteed lattice reservoir decreases. Finding a self-renewing quotient centre or an invariant guarded language remains UNDECIDED. A full repository checkout was inaccessible locally due GitHub DNS failure, so `tools/verify.py --changed` was not run.

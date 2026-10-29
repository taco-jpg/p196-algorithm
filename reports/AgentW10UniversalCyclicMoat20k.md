# W10 universal finite-horizon decimal 5346-block family

**PAPER PROOF with COMPUTED finite obligations.** For every integer q >= 8000, the base-10 integer with canonical decimal word (5346)^q has a nonpalindromic ordinary reverse-and-add orbit through every state t=0..20000. This is **not** an infinite base-10 Lychrel proof and says nothing about 196.

## Part I: 33 exact universal symbolic transitions

For a literal decimal word T(k)=L ++ w^k ++ R with |w|=4 and k>=0, its value is rational-affine in X=10^(4k):

    9999 * value(T(k)) =
      ((9999*value(L) + value(w))*10^|R|) * X
      + 9999*value(R) - value(w)*10^|R|.

A fixed-width reverse word reverse(R) ++ reverse(w)^k ++ reverse(L) has the same affine form, even if its leading digits are zero. Thus the identity T_t(k)+reverse(T_t(k))=T_(t+1)(k) for all integer k>=0 follows from exact equality of TWO integer coefficients of X and 1, not from interpolation at a handful of lengths. Decimal canonical leading digits are nonzero in the templates.

The self-contained symbolic_33.py obtains a centred four-digit insertion presentation at each step t=0..33 using independently calculated q=8 and q=9 words, validates q=10, q=11 and q=100 controls, and then checks exact rational numerator coefficient identities for every one of the 33 edges. For each t the first mirrored unequal digit is strictly outside the band at both ends, so the entire symbolic family is nonpalindromic in all 34 states.

At t=33 the exact decimal word for all q>=8 is

    406477799388690993172 ++ 0^(4q-30) ++ 162389106784007784593.

The two literal exteriors each have length 21 and the zero run is centred. For q=8000 the run contains 31970 zeros.

## Part II: centered-zero insertion lemma

Suppose the canonical decimal word N is A ++ 0^m ++ B, with |A|=|B| and a generous centered zero width m>=10. Let I_s insert s additional central zeros, with s a nonnegative multiple of four. In the least-significant-first paired coefficient word p_i=d_i+d_(n-1-i), the central m columns are all zero, and increasing m inserts exactly s extra zero coefficients. During decimal normalization a binary carry entering the zero coefficient band changes at most its first digit to one, and the outgoing carry is zero. All subsequent columns in the band remain zero. Thus normalization commutes with insertion of s extra zero columns. The high-end overflow is unchanged, and if the output still has a centred zero block of length >=10, the extra zeros can be placed at the centre of its surviving zero run. The reverse-and-add output for I_s(N) is exactly I_s(reverse_and_add(N)).

Centred zero insertion also preserves the palindrome predicate: each pair of mirrored digits outside the inserted zero region is unchanged, and digits inside are zero. The lemma can be applied inductively while an **actual** centered zero region persists. It is not an assertion that such a region persists forever; this finite persistence is the next obligation.

## Part III: every anchor condition checked to step 20000

The new independent zero_insertion.cpp engine implements ordinary base-10 digit-array reverse-and-add for q=8000 and q=8001. At EVERY state t=0..20000 it checks both are nonpalindromic and their lengths differ by four. At every t=33..20000 it also verifies that the entire centered interval

    LSB-first indices [t+64, n_t-t-65]

in q=8000 consists of zeros; that q=8001 has exactly four more zeros in the corresponding centered interval; and the exterior digit words at both ends are literally identical. Thus the q8001 comparison is checked on every one of 19,968 states, not only sparse samples. The minimum protected zero count of the q8000 anchor is 195, attained at t=20000; the conservative >=10 premise is maintained throughout the induction.

Part I supplies the exact step-33 relation between ANY q>=8000 and the q8000 anchor, obtained by inserting 4(q-8000) centered zeros. Part II transports this equality through every transition until step 20000 because Part III certifies a protected centered zero interval at each anchor state. The palindrome equivalence then proves nonpalindromicity for every q>=8000 and every t<=20000.

For an independent full-integer control, the earlier COMPUTED result AgentW10CyclicCarryMoat20k independently replays q8000 with GNU MP mpz_class integer addition and full decimal-string reversal. Its original C++ digit engine checks every symmetric pair coefficient in a four-period central window; both engines agree on 21 full-digit FNV checksums. The new universal_run.sh invokes symbolic_33.py, the new two-seed zero-insertion checker and the earlier independent GMP replay, comparing stored compact fixtures. All code is in calculation/new_structures/agent-W10/ and uses only Python3, C++17 and libgmpxx/libgmp.

## Structural limitation

This family has a **uniform finite horizon**, not an infinite orbit for a fixed q. Its protected zero moat eventually may be consumed by inward boundary defects. A genuine decimal certificate would require a finite return of both boundary defect/carry states with enough overflow-driven renewal to prevent the protected zero core from shrinking. No such return is claimed.

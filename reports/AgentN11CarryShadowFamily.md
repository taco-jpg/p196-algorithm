# N11: A decimal carry-shadow / zero-shield construction

## Claim, scope and interpretation

**COMPUTED.** This is a constructive finite-time family and a million-step observation, **not** a base-10 Lychrel proof. In particular the seed depends on the chosen time horizon; the experiment cannot establish an infinite orbit without palindromes. There is no asserted periodic template cycle or Lean verification. Arithmetic facts below have an elementary exact proof; finite nonpalindrome checks are computational.

## Pairword and exact local carry mechanism

For a base-10 integer with n digits d_i (least-significant first), put P_i=d_i+d_(n-1-i), so P is a palindrome of coefficients 0..18. Normalize the value of P, carrying c_0=0 and c_(i+1)=floor((P_i+c_i)/10), to obtain the next integer's digits. The next length is n+gamma, gamma in {0,1}. For any coefficient x!=9, the carry after x is exactly 1 if x>=10 and 0 if x<=8, independent of the incoming carry. Coefficient 9 is the unique *carry transmitter*.

For an interior lower-half site i, whenever the indicated source coefficients are non-9:

- gamma=0: Q_i = (P_i+[P_(i-1)>=10]) mod 10 + (P_i+[P_(i+1)>=10]) mod 10, requiring P_(i-1), P_(i+1) != 9.
- gamma=1: Q_i = (P_i+[P_(i-1)>=10]) mod 10 + (P_(i-1)+[P_i>=10]) mod 10, requiring P_(i-1), P_i != 9.

The notation [condition] equals 1 or 0. These formulas follow by substituting the low-index digit and its reflected high-index partner into normalization; gamma=1 shifts the high partner by one site. When a local input is 9, scan in its carry-propagation direction until the first non-9; this defines an exact adaptive-radius update. There is no independence assumption and no stochastic approximation.

## The protected zero-band construction

Choose any integer L>=5. Define lower-half pair coefficients P_0..P_(m-1), with m=L+130:

- Outer positions 0..63 and inner positions L+66..L+129 use deterministic xorshift32 pseudo-random values in 0..18 (code); override P_0=12.
- Barrier positions 64 and L+65 are 11.
- The neutral stripe positions 65..L+64 are exactly 9 (length L).

The complete length-2m pairword is P followed by reverse(P). Realize it as an ordinary decimal seed with digits d_i=max(0,P_i-9), d_(2m-1-i)=min(9,P_i) for 0<=i<m. The leading digit is 9. Therefore this is an explicit finite integer N_L, not an infinite symbolic seed.

**Exact carry-shadow lemma (elementary proof).** The barriers 11 force carries 1 into the adjacent 9 stripe on both mirrored sides; each 9 transmits that carry unchanged. If gamma=0, the next pairword is zero throughout indices [66, L+63]. If gamma=1 it is zero on an at least equally long subinterval, because the reflected partner is shifted one site. In either case the common zero interval is [66, L+63], length L-2. Once a zero interval [a,b] is present, zero coefficients reset carry to 0. The two local gamma formulas show the next pairword has zeros on [a+1,b-1] for either gamma, independently of all outside digits and of future overflow decisions. Induction yields for EVERY t>=1 with L-2t>=1 the explicit zero interval [65+t, 65+L-1-t], length L-2t.

This proves a parameterized family of arbitrarily long *finite-time* internal shields. It does not prove that exterior digits remain asymmetric for all times, nor does it pump the shield for one fixed finite seed.

## Replays and independent controls

A compiled least-significant-first unsigned digit-vector engine and an independent most-significant-first schoolbook string-addition engine (which literally adds the reversed decimal string each step) checked N_45000 for t=0..20,000 inclusive. Both checked every palindrome test and every coefficient in the stipulated zero interval on EVERY step. All 21 checkpoint (step, length, FNV-1a digest) triples agree.

At t=0 the seed has 90,260 digits. At t=20,000 it has 98,491 digits and a certified-by-replay zero pairword interval of at least 5,000 positions. There are zero palindromes among the 20,001 checked numbers. The 21 digest controls, including t=0/5000/10000/15000/20000, are reproduced and compared by reproduce.sh, with expected.json recording these five in compact form. Note: 'certified-by-replay' means the two literal engines checked the finite run, not Lean.

A separate least-significant-first digit-vector replay of the *actual 196* orbit was run for 1,000,000 iterations, checking every iterate (including t=0) for a palindrome: none. 414,299 overflow steps produced a final length of 414,302 digits. Selected independent Python arbitrary-precision integer checkpoints agree with the C++ hash, and 1,000 randomized seeds give separate one-step carry-formula controls. This is empirical evidence only, not an infinite orbit claim.

## Real-orbit mechanism and what breaks

On the first 100,000 196 steps, sampled at each t divisible by 100, there are 10,340,000 interior coefficient sites with i in [16, floor(n/2)-17]. The adaptive carry-shadow scan (maximum extra scan depth K) reproduces the literal successor with **zero mismatches** at every eligible site. Eligibility grows from 8,313,078/10,340,000 (K=0; 80.3973%) to 10,052,428 (K=1), 10,300,022 (K=2), and all 10,340,000 (K=7). The largest sampled contiguous 9 stripe is length 7; **this bound is not proved for unsampled steps or the future**.

At sampled t=96,400, coefficient positions starting at i=5,745 contain seven 9s. The next pairword contains six adjacent zeros, persisting through steps 96,401..96,406 before the local block erodes by 96,407. The compact trace can be generated by trace_defect.cpp. In all 390 sampled 9 stripes of length >=5, the guaranteed next interior is uniformly either coefficient 0, 9, or 18, with counts 91/217/82; there were zero exceptions.

The million-step overflow word contains a 131-step alternating 0101... segment starting at t=907,616. Such finite temporary phase-locks do not establish a period-8 space-time lattice, and the 196 orbit does not display an eventually fixed short centre in the recorded windows. A zero shield is an absorbing local domain but **shrinks by at most two cells per step under the rigorous worst-case bound**. Without a regenerating neutral-9 source or a pumping wall, finite L is insufficient for an infinite decimal certificate. The constructive next direction is to synthesize a wall that restores at least two zero cells per period while keeping a persistent nonpalindromic exterior witness.

## Reproducibility

Portable C++17 and Python3 source, deterministic generation of all seeds, an independent arithmetic checker, and expected controls reside in calculation/new_structures/agent-N11/. Execute:

~~~sh
bash calculation/new_structures/agent-N11/reproduce.sh --quick
bash calculation/new_structures/agent-N11/reproduce.sh
~~~

The quick mode executes two independent 20,000-step bubble replays and the 100k-step adaptive profile; the full mode additionally regenerates the one-million-step 196 orbit. Tools require only g++, Python3 standard library and a shell. No code or data from outside this repository is required.

# Y01: exact maximal 18-corridor erosion and the impossibility of persistent repair

**PAPER PROOF**, arbitrary width and every positive base-10 integer. **COMPUTED** controls: 95,479 independent ordinary-decimal bigint cases. This theorem refutes the exact missing persistent-corridor REPAIR lemma in the N23/W single-99-band route, not decimal Lychrel existence. Search redirect: an actual certificate must show *extinction and rebirth* of the corridor, or use a different/multiple band.

## Exact theorem

Write the canonical decimal digits of N units-first as d_0,...,d_(n-1), with the top digit nonzero. Put P_i=d_i+d_(n-1-i), a symmetric coefficient word in 0..18. Suppose the maximal centred run of coefficient 18 has length L>=1, so
P = W ++ 18^L ++ reverse(W), with a=|W|=(n-L)/2, and if a>0 then h=W_(a-1)!=18.
Define the ordinary decimal addition carries c_0=0, c_(i+1)=floor((P_i+c_i)/10), centre-entry bit u=c_a, and output overflow gamma=c_n. The carry bits are in {0,1}. Let L' be the maximal centred coefficient-18 run length in F(N)=N+reverse_10(N), taking L'=0 when the centre is not 18. The exact exhaustive formula is

    gamma=0, u=1: L' = L
    gamma=0, u=0: L' = max(0,L-2)
    gamma=1:      L' = L-1.

No bound on a, L, or the exterior coefficients is assumed. In particular L'<=L whenever L>0.

## One-step proof

The usual normalized digits are e_i=(P_i+c_i) mod 10 for 0<=i<n, with e_n=1 appended when gamma=1. Because coefficient 18 always sends outgoing carry 1 regardless of incoming carry, e_a=8+u, the further L-1 central digits are 9, and the carry entering the first high-side exterior coefficient h at index n-a is 1.

If gamma=0, the output length stays n. For L>=2 the new pair at index a is e_a+e_(n-1-a)=17+u, while for L=1 its central pair is 2e_a=16+2u. If u=0 this pair is not 18 and the inner L-2 positions are 18 (zero positions when L<=2), yielding L'=max(0,L-2). If u=1 the former central run remains entirely 18, but cannot extend outward: at a>0, write v=c_(a-1). Since u=floor((h+v)/10)=1, and h<=17 with v<=1, the adjacent lower digit e_(a-1)=h+v-10<=8. Its paired upper digit is at most 9, so that outer pair is <=17. At a=0 there is no outer pair. Hence L'=L.

If gamma=1, the output length is n+1. Its innermost L-1 coefficients are 18. At index a, for a>0, the new pair is
  e_a+e_(n-a)=(8+u)+((h+1) mod 10).
For this to equal 18 we need u=1 and h=8; but h=8 forces u=floor((8+v)/10)=0, contradiction. For a=0 the added leading 1 pairs with e_0=8, also not 18. Thus the central 18-run has exactly L-1 coefficients. This also covers L=1, when the new run is empty. QED.

## All-time corollary: persistent repair is impossible

Assume one finite decimal integer's entire reverse-and-add orbit retains a positive centred 18-run at every time. The positive integers L_t cannot increase by the theorem, so they eventually stabilize. In the stable tail only the gamma=0,u=1 branch can occur, hence the digit lengths n_t also stabilize. But F(N)>N for every positive integer N, and an infinite strictly increasing sequence of integers cannot stay below 10^n for a fixed n. Contradiction.

The proposed renewal lemma "a finite centre/exterior repair word restores a persistently positive 18-corridor budget after each period" therefore fails *at every width*. N23's ordinary-digit central 9-run has pair coefficient 18, so every version with that corridor continuously present is covered, regardless of the terminal caps or their evolution. The result does not rule out a corridor disappearing and later being reconstructed, a non-18 neutral/absorbing lattice, or a multi-band relay. Such an extinction-and-rebirth bridge, with a real decimal instance and a repeatable all-length nonpalindrome guard, is the remaining missing lemma.

## Independent genuine-integer controls

Run python3 calculation/new_structures/agent-Y01/check_nine_centre.py. It enumerates every canonical coefficient exterior of widths 1..3 and central L=1..7, plus 50,000 seeded random exteriors of widths 1..17 and L=1..107. Each pairword is realized as a genuine canonical decimal integer. The independent arithmetic path uses Python arbitrary-precision n+int(reverse(str(n))), reconstructs the complete successor pairword from decimal digits and measures its central 18-run. The predicted answer uses only the distinct abstract carry recurrence. PASS: 95,479 cases, with (gamma,u) branch counts (0,0):24,054, (0,1):20,916, (1,0):24,905, (1,1):25,604. This finite verification supports but does not prove the all-width formula. No finite-horizon survival or Lean claim is made.

Repository verification python3 tools/verify.py --changed cannot run in this runtime: GitHub is unreachable by shell DNS. No Lean file has been changed; all source consists of a stand-alone Python oracle and the paper theorem.

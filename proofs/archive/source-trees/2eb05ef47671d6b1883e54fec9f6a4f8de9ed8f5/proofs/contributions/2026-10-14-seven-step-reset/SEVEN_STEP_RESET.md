# An exact conditional seven-step return, its core map, and failed induction tests

The short reset observations for the remaining gate produce words whose
first three coefficients are \((4,4,0)\). This note proves the exact
condition for that prefix to return after seven pair updates. It also
gives the full middle-word map and ordinary finite realizations with one,
two, and three safe returns. **The return condition and its safety
condition have not been proved invariant.** Explicit examples below show
why neither can be omitted from an induction argument.

All words are ordered from least to most significant position. Let
\(G\) be the actual decimal pair-word update.

## 1. Domain and the exact boundary control

Let

\[
Q_0=(4,4,0)\,W_0\,(0,4,4),
\]

where \(W_0\) is a nonempty **padded middle word**: its coefficients are in
\(\{0,\ldots,18\}\), it is symmetric, and its center coefficient is even
when its width is odd. Its endpoints may be zero. Consequently \(Q_0\)
is canonical even when \(W_0\) is not a canonical component by itself.

Put \(Q_t=G^t(Q_0)\), let \(L_t=|Q_t|\), and let \(c_t\) be the actual
carry entering the final three original columns when normalizing \(Q_t\):

\[
c_t=\operatorname{carry}(Q_t,L_t-3).
\]

This is an actual whole-word carry, not an arbitrary input that the
construction may choose. Then

\[
\boxed{
Q_7[0:3]=(4,4,0)
\quad\Longleftrightarrow\quad
(c_0,c_1,c_3,c_5,c_6)=(0,0,0,0,1).
}
\tag{1}
\]

Equivalently, the seven-bit word is **\(00*0*01\)**, with positions 2 and 4
free. On exactly these four controls, the complete prefix and final
overflow schedules are:

| \(t\) | First three coefficients of \(Q_t\) | Required \(c_t\) | Final overflow \(e_t\) |
|---:|---|---:|---:|
| 0 | \((4,4,0)\) | 0 | 0 |
| 1 | \((8,8,0)\) | 0 | 0 |
| 2 | \((16,16,0)\) | either | 1 |
| 3 | \((7,14,7)\) | 0 | 0 |
| 4 | \((15,8,15)\) | either | 1 |
| 5 | \((6,14,14)\) | 0 | 0 |
| 6 | \((13,9,9)\) | 1 | 1 |
| 7 | \((4,4,0)\) | — | — |

In particular, the actual whole width increases by exactly 3.

**Boundary calculation.** For a current prefix \(p=(p_0,p_1,p_2)\),
normalize \(p\) with incoming 0 to retained digits
\(\ell=(\ell_0,\ell_1,\ell_2)\). Normalize
\((p_2,p_1,p_0)\) with incoming \(c\) to retained digits
\(v=(v_0,v_1,v_2)\) and final carry \(e\). Symmetry of the actual whole
word gives its next prefix exactly as

\[
\begin{cases}
(\ell_0+v_2,\ell_1+v_1,\ell_2+v_0),&e=0,\\
(\ell_0+1,\ell_1+v_2,\ell_2+v_1),&e=1.
\end{cases}
\tag{2}
\]

The two observed three-column blocks are disjoint because \(L_t\ge7\).
Equation (2) therefore has no omitted interior condition once the actual
carry \(c\) is supplied. Applying it seven times to all \(2^7=128\) carry
words gives exactly (1) and the table. `PREFIX_CONTROL_CERTIFICATE.json`
retains every branch, including the four successful branches; the source
performs the finite branch calculation directly rather than assuming the
condition as a hypothesis of the enumeration.

## 2. Exact middle-word map

During a successful return write

\[
Q_t=p_t\,W_t\,p_t^R,
\]

using the three-term prefixes in the table. Let \(m_t=|W_t|\). The actual
carry entering \(W_t\), obtained by normalizing the low prefix, is

\[
(\alpha_0,\ldots,\alpha_6)=(0,0,0,0,1,1,1).
\]

Let \(D_t\) be the **fixed-width** \(m_t\) retained digit polynomial from
normalizing \(W_t\) with incoming \(\alpha_t\), and let \(\gamma_t\) be its
outgoing carry. Thus \(\gamma_t=c_t\). The guards for the middle map are

\[
(\gamma_0,\gamma_1,\gamma_3,\gamma_5,\gamma_6)=(0,0,0,0,1).
\tag{3}
\]

The middle evolves by these exact formulas:

| Step \(t\) | \(W_{t+1}(x)\) | New width |
|---:|---|---:|
| 0, 1, 3, 5 | \(D_t(x)+x^{m_t-1}D_t(x^{-1})\) | \(m_t\) |
| 2 | \(D_t(x)+x^{m_t}D_t(x^{-1})+\gamma_t(1+x^{m_t})\) | \(m_t+1\) |
| 4 | \(D_t(x)+x^{m_t}D_t(x^{-1})+(5+\gamma_t)(1+x^{m_t})\) | \(m_t+1\) |
| 6 | \(D_t(x)+x^{m_t}D_t(x^{-1})\) | \(m_t+1\) |

All widths are represented widths; leading or trailing zeros of the
middle are retained. In particular, \(|W_7|=|W_0|+3\), even when the
maximal zero spacer of the whole word is larger than one.

**Proof.** With no final whole overflow, both digits contributing to a
new middle position come from the two reflected positions of the old
middle, giving the first row. With final overflow, the whole reflection
shifts by one. The new middle has width \(m_t+1\), with its endpoints
receiving the first retained digit of the high three-column block. That
digit is

\[
a_t=(p_{t,2}+\gamma_t)\bmod10.
\]

Hence its general formula is
\(D_t+x^{m_t}D_t(x^{-1})+a_t(1+x^{m_t})\). At overflow steps 2, 4, 6,
the table gives respectively \(a_t=\gamma_t,5+\gamma_t,0\); the last
equality uses \(\gamma_6=1\). This proves the core map, including all
incoming carries and width changes.

The map is a concrete conditional operator \(\mathcal T:W_0\mapsto W_7\).
Its domain consists exactly of the padded middle words that satisfy the
five guards (3) during the displayed computation. A recurring construction
must prove that the output satisfies these guards again; the current
statement does not assume or prove that closure.

## 3. Exact safety condition through the return

Under (1), all seven positive ordinary successors are nonpalindromic if
and only if **both \(W_0\) and \(W_1\) have a coefficient at least 10**.

For the first two steps, the outside coefficients are 4 and 8, so no
final overflow is possible. A symmetric pair word without final overflow
normalizes to a palindrome exactly when it has no carries, equivalently
when every coefficient is at most 9. The only possible large coefficients
at these two steps lie in \(W_0,W_1\).

For the later five steps, safety is forced by the displayed prefix. At
steps 2, 4, 6, the least significant normalized digits are respectively
6, 5, 3, while the new leading digit is 1. At steps 3 and 5, an internal
coefficient 14 causes a carry, while the outside coefficients 7 and 6
exclude final overflow. Thus none of those five normalizations is a
palindrome.

Consequently an infinite induction would need **two** preserved facts:
eligibility for \(\mathcal T\), and the two safety tests. Preserving only
the returning boundary prefix is insufficient.

## 4. Actual finite realizations and explicit failed hypotheses

Every example below is an actual canonical whole pair word
\((4,4,0)W_0(0,4,4)\). The records include an ordinary realizing seed,
literal integer reversal-and-addition checks, all pair states, controls,
and the next attempted cycle.

### A safe return whose next return is not safe

\[
W_0=(1,1,16,1,1),\qquad
W_7=(3,9,12,13,13,12,9,3).
\]

The first seven additions are safe and the prefix returns. The second
cycle also satisfies the returning control pattern, but its second
ordinary successor is a palindrome. Thus the **first positive palindrome
time is 9**. This disproves the hypothesis that repeated eligible prefix
returns alone preserve safety.

### Two safe returns followed immediately by a palindrome

\[
\begin{aligned}
W_0&=(1,1,18,1,1),\\
W_7&=(3,9,8,10,10,8,9,3),\\
W_{14}&=(3,5,4,2,0,0,0,2,4,5,3).
\end{aligned}
\]

Both seven-step cycles are safe. Every coefficient of the whole word at
time 14 is at most 9, so the **first positive palindrome time is 15**.
The third attempted return also eventually fails its step-5 carry guard,
but the palindrome has already occurred before that failure.

### Three safe returns, followed by loss of the carry condition

\[
\begin{aligned}
W_0&=(1,1,14,16,14,1,1),\\
W_7&=(3,9,15,14,6,6,14,15,9,3),\\
W_{14}&=(0,2,10,15,10,7,8,7,10,15,10,2,0),\\
W_{21}&=(4,9,6,9,14,7,10,9,9,10,7,14,9,6,9,4).
\end{aligned}
\]

These are three safe returns and 21 safe additions. The zero endpoints
of \(W_{14}\) are why the padded-middle domain is necessary. The fourth
attempt has actual control word \(0010111\), violating
\(\gamma_5=0\); after seven more additions its prefix is \((4,4,1)\).
Those seven further additions are also nonpalindromic, but they do not
return to the stated prefix family. No later safety claim is made.

### The observed original-gate resets do not renew through this map

The original \((1,7)\) gate members with \(r=4\) and \(r=5\) both have a
\((4,4,0)\) prefix at time 9. Their next seven actual control bits are
respectively \(0010111\) and \(0010110\). Both violate the required
step-5 zero carry and both end with prefix \((4,4,1)\). This gives the
exact local reason the observed resets do not immediately supply the
proposed seven-step induction.

## 5. Complete bounded catalog and reproduction

The discovery catalog covers every canonical initial middle word of
width 1 through 7: **75,447 initial words**. It records seven-step returns,
safety, the next eligible return attempts, and every fourth attempt after
three safe returns. It does not bound the widths of later padded middles.

| Initial width | Initial words | Prefix returns | Safe returns | Two safe returns | Three safe returns |
|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 0 | 0 | 0 | 0 |
| 2 | 18 | 0 | 0 | 0 | 0 |
| 3 | 180 | 11 | 0 | 0 | 0 |
| 4 | 342 | 20 | 0 | 0 | 0 |
| 5 | 3,420 | 204 | 104 | 10 | 0 |
| 6 | 6,498 | 387 | 172 | 22 | 0 |
| 7 | 64,980 | 3,879 | 2,794 | 313 | 23 |

All 23 fourth attempts in the last category fail the returning carry
condition. This is a complete finite negative result for the stated
initial catalog, not a proof excluding a broader invariant family.

Run:

```sh
python -B proofs/contributions/2026-10-14-seven-step-reset/seven_step_reset.py
```

The retained files are:

- `PREFIX_CONTROL_CERTIFICATE.json`: all 128 control branches.
- `CATALOG_OUTCOMES.bin.gz`: one outcome byte for each of the 75,447
  initial words, with exact enumeration and bit schema in the summary.
- `RETURN_CATALOG.json.gz`: all 4,501 returning initial middles and their
  computed follow-up attempts, including failed guards and unsafe returns.
- `ACTUAL_RETURN_EXAMPLES.json`: complete literal-integer checks for the
  three displayed examples and their next attempted cycles.
- `ORIGINAL_GATE_RESET_PROBES.json`: the previously observed resets for
  \(r=4,5,6,31,32\), each with the next nine pair updates preserved.
- `RESET_SUMMARY.json`: exact counts, schemas, and SHA-256 hashes of the
  deterministic compressed records.

The all-length conditional result is the boundary and middle calculation
in Sections 1--3. The bounded catalog supplies finite realizations and
counterexamples to proposed closure hypotheses. Neither part proves an
infinitely repeatable safe reset.

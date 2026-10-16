# Agent6 independent coordinate review

Status: mathematical statement review and finite experimental controls; this reviewer has not compiled a new Lean theorem. The parent owns the new CoordinateDynamics source. The original Agent115 update law remains attributed to Agent115, with Agent113's prior independent review retained separately.

## Exact source basis

- Main snapshot: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
- Literal map: `proofs/OuterFinite__1c852c0ed5b8d706.lean`; SHA256 `3376873da457c698850f604ddda82aeba3e67f4196e5c33d8142bed945c5f3f6`.
- Agent115 update source: `fba03a902e0f6b198cbf8f42efa8d11f8f2ba7a6`, `proofs/contributions/agent-115/exterior-factorization/ExteriorUpdateLaw.lean`; Git blob `db2f3c5ea38b8d49ef7da82631b2ed7a95a29bea`; SHA256 `d384cb9a3598b210ec1a0c7cc310297ca2b34cf1e6b0588e03516f0da75331b9`.
- Existing interfaces reused: `normalize_eq`, `rawSucc_values`, `successor_observation`, and padding invariance of `zValue`.
- New task claim supplied by parent: `1b3935d7f0ad6aaff290a9c8baa883f60d572434`, issue61 comment `6224594156`.

## Signed beta identity: hypotheses can be omitted

For arbitrary natural phase `c` and natural coefficient list `B`, set

`n = B.length`, `D = 10^n`, `V = lowValue B`, `H = highValue B`,
`k = if 10 <= c then 1 else 0`, `t = c - 9*k`,
`X = H+k`, `R = revN n X`, `gamma = X/D`, `kappa = V/D`.

Define the signed integer coordinate

`betaNum(c,B) = zValue(c,B)-c = 9*V-c*D`.

The proposed increment is

`delta = if gamma=0 then 9*R-t*D else 9+90*R-10*t*D`.

The intended identity is

`betaNum(outerNext(c,B)) = betaNum(c,B)+delta`.

The one-step identity needs no nonneutrality, coefficient bound, positive head, or trimming hypothesis. Every subtraction in `betaNum` and `delta` must be integer subtraction. The existing literal map uses natural subtraction in `t` and `u`; those specific subtractions do not truncate because `9*k <= c` and `10*k <= c` follow directly from the definition of `k`.

Derivation: let `q=V/D`, `v=V%D`, and `u=c+q-10*k`. Then `V=v+q*D`. Write `A` for the other summand's low value: `A=R+t*D` in the zero-carry branch, and `A=1+10*R` otherwise. The original `rawSucc_values` gives `lowValue(raw)=v+u*D+A`, and the raw length is `n+1`. The new phase is `c'=2*t`. Padding invariance converts the trimmed successor to the same beta coordinate as the raw word. Consequently

`betaNum(next) - betaNum(current)`
`= 9*(v+u*D+A)-20*t*D-(9*(v+q*D)-c*D)`
`= 9*A+(10*c-90*k-20*t)*D`
`= 9*A-10*t*D`.

Substituting the two definitions of `A` yields exactly the proposed formula. This is an algebraic review, not a substitute for the parent's Lean proof.

For coefficients outside0..18, `gamma` may exceed1. The formula still describes the literal `outerNext`, whose nonzero-carry branch inserts the fixed digit1. Do not interpret these unrestricted identities as ordinary decimal carry semantics without the relevant domain bounds.

## Rho floor: exact role of the assumptions

The floor equality only needs `c/9=k`; it does not need coefficient bounds. A convenient elementary domain is `c<=17` and `c!=9`, including the requested nonneutral even phases.

Write `c=9*k+r` with `0<=r<9`, and `X=D*gamma+s` with `0<=s<D`. Then

`9*H+c = 9*X+r = 9*D*gamma+(9*s+r)`

and `0<=9*s+r<9*D`. Thus `(9*H+c)/(9*D)=gamma`.

For these phases, `gamma!=0` iff `rhoNum>=9*D` follows without coefficient bounds. To replace `gamma!=0` by `gamma=1`, one needs an upper bound. With all coefficients at most18, `H<=2*(D-1)`, while `c<=17`, giving `rhoNum<=18*D-1`. Hence `gamma<=1`.

Exact boundary controls:

| State | Actual gamma | rho | Consequence |
| --- | ---: | ---: | --- |
| `c=9,B=[9]` | 0 | 1 | Neutral phase breaks the claimed floor/threshold equality. |
| `c=18,B=[]` | 1 | 2 | The usual upper phase range matters. |
| `c=2,B=[20]` | 2 | 91/45 | Removing coefficient bounds breaks `gamma=1 iff rho>=1`; floor equality still holds. |

## Nonzero increments and conditional cycle consequences

Within the requested nonneutral phase domain, the short modular argument is `delta mod9 = (-c) mod9`, because `10^n mod9=1` and `t=c-9*k`. Since the phase is one of2,4,6,8,10,12,14,16, the increment cannot be0.

An optional stronger target is nonzero increment for every `c>0`, with arbitrary coefficients. In the nonzero-gamma branch, `delta mod10=9`. In the zero-gamma branch, `0<=R<D`; if `9*R=t*D`, coprimality of9 andD gives `9|t`. Positivity ofc gives `t>0`, hence `t>=9`, contradicting `9*R<9*D<=t*D`. The phase-domain modular proof is shorter if this strengthening does not help the next theorem.

For any finite trajectory, summing the one-step identity gives

`sum_{i<P} delta(s_i) = betaNum(s_P)-betaNum(s_0)`.

If `s_P=s_0`, the signed sum is0. Equality of the beta coordinates already suffices; a same-phase return modulo trailing band padding is another sufficient endpoint condition because beta is padding-invariant.

For `P>0`, if the increments are nonzero at every step, a zero signed sum forces at least one positive and at least one negative increment. Thus any positive-period closed trajectory within the nonneutral phase domain must contain both signs. The phase domain is invariant under the phase map, so initial nonneutrality suffices once that existing finite phase fact is supplied.

Do not omit `P>0`: the empty sum is0 without any sign witnesses. Do not generalize nonzero increments to `c=0`: `outerNext(0,[])= (0,[])` and the increment is0. No actual positive-period closed exterior trajectory is provided, and no global acyclicity conclusion follows.

## Sign is not determined by the overflow bit

All four states below have permitted phase, positive head, coefficient bound18, and an already trimmed word.

| State | gamma | Successor | beta before | beta after | Increment |
| --- | ---: | --- | ---: | ---: | ---: |
| `(2,[1])` | 0 | `(4,[2])` | -11 | -22 | -11 |
| `(2,[3])` | 0 | `(4,[6])` | 7 | 14 | 7 |
| `(2,[10])` | 1 | `(4,[1,3])` | 70 | -121 | -191 |
| `(2,[13])` | 1 | `(4,[4,6])` | 97 | 176 | 79 |

These are precise candidate kernel controls for rejecting an attempted monotonicity argument based solely on the overflow class. They are experimental evaluations until individually formalized.

## Executed independent controls

Command:

`python3 /workspace/scratch/f8aedc6d7adf/claims-agent6/coordinate-review/check_signed_beta.py`

Observed exit status0. Receipt: `signed-beta-controls.json`.

- Exhaustive:296,840 states with `0<=c<=40`, width0..3, and every coefficient in0..18. No positive-head or trimming filter was applied.
- Additional seeded controls:10,000 states with `0<=c<=300`, width0..20, coefficients0..200, Python random seed196006.9,025 tested states had gamma greater than1.
-64 initial states were advanced through24 steps each; the signed telescope matched every intermediate endpoint, and nonneutral phase closure held.
- Every tested signed one-step formula matched. The generalized rho floor and threshold implications were checked precisely on their stated conditions. Nonzero increments and the mod9 identity were checked on the requested nonneutral phase domain.

The control program advances the state using a literal digit-and-carry translation of `OuterFinite.outerNext`. It computes values, reversed digits, and the candidate increment separately. Integer and exact Fraction arithmetic are used; there is no floating-point acceptance tolerance. These finite results support interpretation review and sharp controls; they do not establish universal mathematical statements.

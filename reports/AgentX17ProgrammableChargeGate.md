# X17: complete eight-input decimal carry-charge logic gate at t=107

**Label: COMPUTED.** A new finite-state *guard component* for decimal reverse-and-add, **not** a global certificate or a proof of any infinite Lychrel orbit. Scope is exactly four explicitly enumerated lengths and all 256 eight-bit defect masks.

## Parameterised inputs and outputs

For `n in {2001,6001,10001,20001}`, let `P_n` be the `n`-digit decimal palindrome with least-significant-first motif `88283583`, reflected about its centre. Given mask `m in [0,255]`, define the nonnegative decimal integer

`Q_{n,m} = P_n + sum_{k=1}^8 ((m>>(k-1))&1) * 10^(floor(n/2)-k)`.

All modified digits are initially `<9`, so this is precisely the requested binary centre-defect controller with no starting carries. Evolve both `P_n` and `Q_{n,m}` for **107 genuine decimal reverse-and-add steps**, then let `L` be their common length, `J=L-61=n-14` and `c_P(J),c_Q(J)` the decimal normalization carry bit entering the coefficient column `J` in the *next* reverse-and-add step. Define `F_n(m)=c_P(J) XOR c_Q(J)`; this Boolean function measures whether the long outer 9-channel will transmit a differential carry. The `t=108` result's common most-significant prefix length is `H_n(m)`.

## Exhaustive computed truth table and finite controller

Independent algorithms agree for every one of the 256 masks at `n=2001`: a Python unbounded-int decimal reversal and a separately implemented C++ base-10 digit-column recurrence. The Python bigint engine was additionally run on all 256 masks at `n=6001` and agrees with the C++ engine. The C++ engine exhaustively computes all masks at `n=10001` and `n=20001` too. The **256-entry truth table `F_n` is identical** at all four tested lengths. This is an *observed exact finite-size identity*, not a claim about arbitrary `n≡1 mod 16`.

- Exactly **86 masks** have `F_n(m)=0` (carry charge neutralized); **170 masks** have `F_n(m)=1` (differential carry charged).
- For all 170 charged masks and all four lengths, **`H_n(m)=60`**, a giant carry avalanche whose spatial reach depends on n but whose surviving exterior does not.
- For every one of the **85 nonempty neutral masks**, **`H_n(m)=H_2001(m)+(n-2001)/2`** in the four-length test grid: the high matched exterior grows linearly with initial seed size. For `m=0`, the identical-orbit case has `H_n(0)=n+47`.
- The function's exact algebraic normal form has **135 nonzero monomials and degree 7**, so it cannot be described as parity or a linear superposition of single-defect impacts.
- An explicitly enumerated **12 nonterminal-state reduced ordered binary decision diagram** (bit-check order `6,4,5,1,2,3,7,8`, offset numbers starting at 1) outputs the 256 exact charge bits. The node table, root and edges are in `charge_logic_bdd.json` and independently evaluated on every mask. This is a reusable finite controller *for the stated computed gate*, not an unproved extension to all lengths or all times.

This construction subsumes the previously observed two-cell cancelation `{7,8}` at the same gate but adds a **complete 8-bit input/output semantics**, its high-degree nonlinear Boolean structure, and a compact exact decision graph. A potential certificate search could treat this as a finite spatial-defect gate with charge guards; **proving repeated time-regeneration or an arbitrary-length pump remains open**.

## Correctness and reproduction

The ordinary arithmetic identity is exact in every base: normalizing pair coefficients `s_i=d_i+d_{L-1-i}` produces carry `c_{i+1}=floor((s_i+c_i)/10)`. A corridor with `s_i=9` preserves its input carry. Consequently the sampled `F_n(m)` has a rigorous operational interpretation as the finite charge delivered to that corridor; what is only **COMPUTED** is the actual 107-step mask-to-charge table for four n values. The BDD correctness on that exact 256-element input domain is checked exhaustively, while Lean verification and arbitrary-length closure are not claimed.

Reproduce: `bash calculation/new_structures/agent-X17/charge_logic_reproduce.sh` (C++: all four lengths; Python bigint: n=2001; cross-language exact 256-row comparison; BDD regeneration; 1,024-row affine and equality controls). Run `DEEP=1 bash ...` to add the independent Python n=6001 full table. Source: `charge_logic.cpp`, `charge_logic.py`, `charge_logic_bdd.py`, `charge_logic_reproduce.sh`; data: `charge_logic_2001.csv`, `charge_logic_bdd.json`, all under `calculation/new_structures/agent-X17/`. Only Python3 and C++17 are required. No repo-wide verifier/Lean check was available in this environment.
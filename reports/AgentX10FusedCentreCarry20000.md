# Agent X10: repairing transparent-overlap carry through a fused central packet

**Status: COMPUTED (universal finite horizon, 20,000 steps).** No infinite Lychrel certificate is claimed. This is a strengthening of the earlier transparent-overlap 13-edge decimal family by a different, exact symbolic continuation beyond the central collision. The role of its growing resource requirement is explicit.

## 1. Exact two-stage digit-packet dynamics

Start with the genuine base-10 seed

`N_0(q)=88*10^(2q+4)+78*10^q+75`, integer `q>=11`.

The first 13 steps have the four affine packet bases `0,q,q+4,2q+4`. All four sources and targets at times `0..13` are canonical digit words even though the two centre sheets overlap at 1–4 positions in each time `t=4..13`. The earlier paper proof and exact checks in `reports/AgentX10TransparentOverlapFormat.md` certify each step for all `q>=11`, not merely for sampled q. At the next sheet update `t=14`, the four-sheet representation loses its transparent *capacity* guard: four central positions have aggregate coefficient >=10 (peak 14). This is an obstruction to using the **separate central sheets**, not an obstruction to ordinary decimal arithmetic.

**Carry repair at t=13.** Write the two central least-significant-first packets as `A` based at `q`, `B` based at `q+4`. Form the finite polynomial `C(X)=sum_j A_j X^j + X^4 sum_j B_j X^j` at `X=10`, normalize its coefficients using the ordinary base-10 carry recurrence, and trim exterior zeros. This yields one *canonical* merged centre packet `C` based at `q`, exactly the same integer as the original sum. No interaction with the outer packets is needed while their supports remain separated. The fusion occurs at t=13 and persists indefinitely as a valid standalone packet recurrence, although the physical separation from the outer packets holds only for a bounded number of steps at fixed q.

At each later time the symbolic integer template has three packets

`T_t(q)=L_t(10) + 10^q C_t(10) + 10^(2q+4) H_t(10)`,

where each `L_t(X), C_t(X), H_t(X)` is a finite **Laurent digit polynomial** `sum_j d_j X^(start+j)` and can have signed *local* offset `start`; the guarded **absolute** exponents are always nonnegative. Let `h_t=H_t.end` be the highest local exponent in the high packet (the absolute leading exponent is `2q+4+h_t`). Then the exact local updates are

`L_{t+1}=norm( L_t + rev_{h_t}(H_t) )`,

`H_{t+1}=norm( H_t + rev_{h_t}(L_t) )`,

`C_{t+1}=norm( C_t + rev_{4+h_t}(C_t) )`,

with `rev_h` reflecting each local exponent `j` to `h-j`. The source integer reversal decomposes linearly across packets because the three packet supports do not overlap, and normalizing each packet preserves the numeric sum. If the next three packets remain separated with no negative absolute exponent, this target is exactly the ordinary decimal reverse-and-add successor. The central update includes **all carries between the old two middle sheets**, so it remains correct at t14 and afterwards even though separate middle-sheet capacity has failed.

## 2. Finite universal affine gap guard

For every three-packet state, the exact universal `q` lower bound is the maximum of the following integral affine constraints:

- `q+C.start >= 0`, `2q+4+H.start >= 0`, and `L.start >= 0`;
- `L.end < q+C.start` (left/centre disjoint);
- `q+C.end < 2q+4+H.start` (centre/right disjoint);
- `L.end < 2q+4+H.start` (redundant when centre nonempty, but explicitly checked).

The first two positive-slope inequalities are solved by exact integer ceilings; there is no asymptotic estimate. Every packet is stored canonically with its own carries, so on a state satisfying the guard the physical numeral equals the sum of packet values digit-for-digit. `fused_20k.cpp` enumerates and checks the entire finite 20,000-step packet sequence while updating the *maximum* required q. The checker also tests the exposed unmatched low/right digit of the two **outer** packets at every state: if they are separated from the centre, the whole numeral cannot be palindromic. Every state `t=13..20000` has a valid outer mismatch, giving a q-independent nonpalindrome witness throughout the guarded interval. States 0..12 inherit the earlier four-sheet proof.

The exact milestone guard table is:

| t | minimum universal q | left packet length | merged centre length | right packet length |
| ---: | ---: | ---: | ---: | ---: |
| 13 | 11 | 9 | 15 | 10 |
| 14 | 12 | 10 | 16 | 10 |
| 88 | 56 | 46 | 60 | 45 |
| 264 | 166 | 137 | 172 | 137 |
| 1,000 | 614 | 507 | 624 | 507 |
| 5,000 | 3,020 | 2,542 | 3,020 | 2,544 |
| 10,000 | 6,031 | 5,064 | 6,044 | 5,065 |
| 20,000 | **12,002** | 10,122 | **12,021** | 10,121 |

Thus **for every integer `q>=12002`**, the single seed `N_0(q)` survives all 20,000 additions without any palindrome and every one of the 20,001 states has the claimed exact three-region form after the fusion. The quantifier `every q>=12002` follows from explicit symbolic coefficient recurrences and proven affine-gap implications, not interpolated data. This result does not infer any behavior for fixed q beyond step 20,000.

## 3. Independent full-decimal replay and controls

`fused_20k_replay.cpp` constructs the actual complete source digit string directly from the seed coefficients, then uses an independent grade-school base-10 reversal/addition on the **entire digit array**, without calling the symbolic packet recurrence for the actual next value. It separately generates the full predicted word from the four-sheet aggregate before fusion and the three-sheet aggregate afterwards, and compares **every digit at every state**, not just checkpoints. It separately rejects actual palindromic words. The two q-boundary witnesses:

- `q=12002`: t0 length 24,010, t20,000 length 32,264; `matched=20001`, `nonpal=20001`, `bound=12002`, FNV64 over all full words `13283548839479728565`.
- `q=12003`: t0 length 24,012, t20,000 length 32,266; `matched=20001`, `nonpal=20001`, `bound=12002`, FNV64 `7791904213455242995`.
- Positive small-horizon guard control `q=614`, `t=0..1000`: `matched=1001`, `nonpal=1001`, `bound=614`, FNV64 `16749580404920997645`.

The four-to-three fusion happens at t13 for all three exact replays; the first centre overlap occurs at t4 and the capacity of separately normalizing two centre sheets first fails at t14. These controls confirm that the new centre fusion is not a consequence of silently imposing a non-overlap assumption. The complete traces are stored compactly with checkpoint rows and full-word rolling hashes in `calculation/new_structures/agent-X10/` rather than giant decimal dumps.

Reproduce: `bash calculation/new_structures/agent-X10/fused20k_reproduce.sh` (g++, Python 3). The script first reproduces the previous q>=11 transparent-overlap checks, then recompiles the new three-packet symbolic checker, the fully independent whole-word replayer, and compares three replay traces byte-for-byte against the committed compact output. This command passes locally. No Lean files are added or changed. `tools/verify.py --changed` was not runnable in this environment, so the result is not labeled LEAN-VERIFIED.

## 4. What remains unsolved

The three-region recurrence **does not return to a finite cycle of bounded packet size**: from t13 to t20,000, the central packet increases from 15 to 12,021 digits, and the required safe q increases from 11 to 12,002. The shielding gap is steadily consumed. The result is a concrete positive carry-healing mechanism plus a uniform finite-time polynomial family, **not** an infinite certificate. A genuine decimal certificate would need an additional self-replenishing/gap-growth rule or a renormalized central packet cycle, and must verify that the parameter domain is invariant under its macrocycle rather than fixed only for a finite horizon. No theorem about 196 is claimed.

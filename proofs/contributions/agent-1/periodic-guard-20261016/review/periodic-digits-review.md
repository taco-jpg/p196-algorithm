# Independent review: periodic digit decomposition

Reviewer: genuine Agent #1 specialist `research_status`, 2026-10-16. Parent authored `Agent1PeriodicDigits.lean`; this reviewer changed no Lean source and performed no Git writes. Scope: independent semantic review and incremental compilation of this module, not the unfinished raw guard theorem or a new clean audit of the complete future package.

**PASS** at source SHA-256 `dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab`. All five exported theorems compiled independently with `--trust=0`; their printed transitive axiom union is `Classical.choice`, `Quot.sound`, and `propext`. No statement defect or missing prerequisite for the proposed zipper contract was found.

## Exact semantics

`periodicWord` is the literal structural template `B ++ w^k ++ H ++ reverse(w)^k ++ reverse(B)`. It uses the published `pow`; there is no new normalizer or pair-word operation.

All carry definitions are the original forward scan, in their actual order: `leftEntry = terminalCarry B 0`, `leftCarry = terminalCarry w leftEntry`, `rightEntry = terminalCarry H leftCarry`, and `rightCarry = terminalCarry w.reverse rightEntry`. The right-band carry is not chosen independently and is not assumed equal to the left-band carry. The right band is scanned forward through the reversed coefficient block.

`normalize_periodicWord` gives the exact five-part output

`A ++ pow U (k+2) ++ C ++ pow V (k+2) ++ Z`

for source exponent `k+3`, where `A=leftGuardDigits`, `U=leftPeriodDigits`, `C=centerGuardDigits`, `V=rightPeriodDigits`, and `Z=rightGuardDigits`. The first normalized copy of each band is retained separately in `A` and `C`. Each subsequent copy uses its own stabilized carry. `Z` is the full original normalization of `B.reverse` at `rightCarry`, so the final carry is appended exactly once.

The proof composes the already checked `normalize_context` twice. The first application keeps the entire middle, second band, and suffix as its arbitrary final context. The second application receives the bit carry proved for `leftCarry`. The coefficient bounds on `B,H,w`, including reversal of `w`, suffice for both applications. No symmetry, positive exterior, odd-center parity, nonempty block, or length-four hypothesis is silently used.

## Export checks

| Export | Reviewed meaning |
|---|---|
| `normalize_periodicWord` | Exact digits at every exponent `k+3`; correct two first-copy transients and fixed suffix normalization. |
| `scan_carry_stable` | Every positive exponent `k+1` has the same actual terminal carry as exponent three. It compares both counts to the existing single-copy endpoint. |
| `scan_carry_eq` | The exponent-three terminal carry is precisely the carry after scanning `B.reverse` with the stabilized right-band carry. |
| `scan_carry_le_one` | The actual terminal carry is a bit; all intervening coefficient bounds and reversal bounds are supplied. |
| `scan_block_lengths` | Exact five lengths, including `Z.length = B.length + gamma`; `normalize_length` is applied to a bounded suffix with a proved bit input. |

The exact lengths are `|A|=|B|+|w|`, `|U|=|w|`, `|C|=|H|+|w|`, `|V|=|w|`, and `|Z|=|B|+gamma`, where `gamma` is the actual carry at exponent three. These total the expected source width plus the one actual overflow bit.

## Match to the planned structural zipper

Specialist `symbolic_scope` supplied this proposed generic contract during the review: for arbitrary lists `A,U,C,V,Z`, lengths `b+4,4,h+4,4,b+g`, and `g≤4`, let `t=take g V`, `d=drop g V`, `O=zipAdd A (Z.reverse ++ d.reverse)`, `W=zipAdd U (t.reverse ++ d.reverse)`, and `M=pair (U ++ C ++ t)`. The target is

`pair (A ++ U^(n+2) ++ C ++ V^(n+2) ++ Z) = periodicWord O M W (n+1)`.

This is recorded as the author's planned contract, not as a checked theorem in this review. The digit module supplies **every premise** after setting `b=B.length`, `h=H.length`, `g=gamma`, `n=k`, and assuming `w.length=4`: the five exact lengths come from `scan_block_lengths`, and `scan_carry_le_one` implies `g≤4`. No digit-content, arithmetic, symmetry, or canonicality premise is required by that proposed structural contract. Its output exponent `n+1` is exactly the original source exponent `n+3` minus two.

The planned split takes the first `g` entries of the forward right-period block `V`; confusing this with `take g V.reverse` would change the overflow alignment. The supplied digit definitions themselves make no such substitution. At carry 0 the center receives no such entries; at carry 1 it receives one, matching the actual appended leading digit's reflected displacement.

## Edge and interpretation checks

- `B=[]` is handled by `normalize [] rightCarry` in `Z`; if that carry is 1, the suffix is `[1]`, not empty. This is the necessary overflow entry.
- `H=[]` leaves the first reversed-band copy in `C`. No hidden source central-column assumption occurs.
- Empty `w` is allowed at the digit-interface level and is consistent with carry identity and zero period lengths; the later guard application separately imposes length four.
- All-nine blocks preserve their incoming carry. Since left/right entries are separately computed, the formula preserves potentially different actual digit patterns across the two bands.
- Incoming carry starts at 0, as required by original `stepWord`. The theorem does not generalize this silently to an arbitrary unbounded incoming carry.
- The identities concern normalized lists and list lengths. They do not establish ordinary decimal canonicality, positive integer realizability, safety preservation, or an infinite orbit.

## Executed evidence

`digits-incremental-001/receipt.json` records this reviewer's actual compile command, version, executable hash, exit code, source hash, and axiom-print check. The exact source snapshot, log, and dependency/source/`.olean` hashes are retained alongside it.

The build directory `/workspace/p196-agent1-session-20261016/periodic-digits-review-incremental-001` was new. Its seven dependency `.olean` files were **reused**, with exact source-byte and `.olean` hashes recorded, from this reviewer's earlier independent clean repeated-block build. All seven source files matched both that earlier build and the new worktree's pinned dependency manifest. Only `Agent1PeriodicDigits` was newly compiled in this run, using Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, with `LEAN_PATH` restricted to the new directory. Exit code was 0; all five literal axiom prints were present. The source remained byte-identical at completion and contains no `sorry`, `admit`, `native_decide`, custom axiom, or `Lean.ofReduceBool` token.

No complete selected-module axiom enumeration or clean dependency rebuild was repeated here. That final package check is reserved until the raw guard and numeric roots are frozen, as requested by the parent.

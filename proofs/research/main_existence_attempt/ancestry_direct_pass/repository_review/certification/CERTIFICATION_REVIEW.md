# v8 carry and certification audit

The inspected v8 arithmetic and certified-interval rules have a sound mathematical explanation. **No valid-input arithmetic counterexample was found in this audit.** This is a source review with two bounded CPU structural probes, not a GPU execution audit, formal verification of the whole program, or proof that 196 never reaches a palindrome.

Source identity supplied by the repository review: commit `8219522a02d46fbb72a6ee38819e5723b8c8fc9f`, archive Git blob `3e105424f94ced716d9d145ac8c4af95b9b91bac`. Inspected checkout: `/workspace/scratch/fe6abe1df721/p196-repo-review/v8/lychrel196_v8/`. Principal files are `bits_core.h`, `bits_tb8.h`, `cuda196_v8.cu`, and `driver8.h`; README and emulator structure were also consulted. File hashes are in `audit_manifest.json`. No upstream files or production checkpoints were modified or executed. No v9 implementation was available for this audit.

The mathematical statements below assume a positive canonical decimal input; folded sums in 0..18, with an even doubled center when the length is odd; sufficient allocated storage; positive supported driver geometry; and execution of the intended bit operations and synchronization. Malformed-option findings and the remaining GPU concurrency concern are separated below.

## Exact carry calculation

Write the folded state as `S_j = d_j + d_(n-1-j)`, with pair 0 at the outside and `h = ceil(n/2)`. For each column let `G_j = [S_j >= 10]` and `P_j = [S_j = 9]`. The decimal carry map is exactly

`c_next = G_j OR (P_j AND c)`.

In the binary sum `X + G + cin`, with `X = G OR P`, the bitwise binary carry recurrence is the same: `X AND G = G` and `X XOR G = P`. Consequently `(low32(X+G+cin) XOR X XOR G)` gives every carry-in bit, and bit 32 gives the word carry-out. This proves the central construction in `bits_core.h:58–100,143–155`; its accuracy does not depend on a random-carry assumption.

`low_summary` correctly classifies the full-word carry map as generate, kill, or propagate. With input carry zero, overflow means generate. Without overflow, adding an input carry changes the word carry-out precisely when the 32-bit sum is all ones. Otherwise it is kill. `high_summary` applies the same identity to reversed bit order. Positions beyond the true middle have `G=0, X=1`, so they transmit the actual middle carry instead of inventing another decimal column. Both inter-word searches continue until an effective reset or a physical boundary; there is no probabilistic cutoff.

Let `a_j` be the carry entering the low-side column and `b_j` the carry entering its high-side partner. Their starting conditions are `a_0=0` and `b_(h-1)=a_h` for even length, or `b_(h-1)=a_(h-1)` for odd length. The resulting digits are

`lo_j = S_j + a_j - 10*a_(j+1)` and

`hi_j = S_j + b_j - 10*b_(j-1)`.

If the output does not grow, its next folded pair is `lo_j + hi_j`. If it grows, the new leading 1 shifts the pairing: it is `lo_j + hi_(j-1)`, with `hi_(-1)=1`. Even input length and growth introduce a new doubled center `2*hi_(h-1)`; the explicit replacement in `bits_core.h:189–194` implements this boundary case.

`digit4` computes the digit formula modulo 16, which suffices because the true digit is in 0..9. The non-growth five-plane formula computes the next pair modulo 32, which suffices because that true pair is in 0..18. These discarded high bits are justified by the decimal range, not an approximation.

The palindrome test also follows from these digit equations. Without growth, the two digits arising from the same `S_j` are equal exactly when `a_j=b_j`; different incoming carries give distinct residues modulo 10, including the 9-to-0 transition. With growth the comparison must be `lo_j=hi_(j-1)`. The code makes the new center compare equal to itself where appropriate. Checking a folded sum alone would be insufficient; this code checks the corresponding digits/carries.

## Why the certified intervals are sufficient

An interval `[L,R)` states that the local simulated pair values agree with the full exact state. Outside that interval local carries or values may be arbitrary. Assume the current global growth bit `g` is certified separately.

For `L>0`, let `q` be the first known pair at or after L whose sum is not 9. Its carry map is constant, so all low-side digits starting at `q+1` are independent of the unknown carry entering L. Thus the new left bound is `q+1`. If `L=0`, the true incoming carry zero fixes the entire low scan and the new left bound remains zero.

For an artificial right boundary, let `r` be the last non-9 pair before R. It resets the reverse-direction carry. High-side digits are then exact strictly before r. A non-growing output uses `hi_j`, giving new right bound r. A growing output uses `hi_(j-1)`, giving new right bound `r+1`. Failure to find the required reset means loss of certification. These are exactly the updates in `track_step`, `bits_tb8.h:431–454`, and the interior `hy_track`, lines 744–766.

At the real middle, the right bound is the true new `ceil(n/2)`. The low scan must determine the middle carry from certified data. There is a subtle odd-length case: the doubled center is automatically non-9, but its outgoing carry does not determine the incoming carry used by `mid_cin`. This does not yield a false certificate. If that center were the only reset in an interval with `L>0`, the left update would be h and the right update would also be h, so the tracker rejects the empty interval. A nonempty accepted result therefore has a preceding reset, or the true left boundary L=0. Both determine the required incoming middle carry.

This reasoning certifies the two individual digits used in each retained output pair, not only their sum. Therefore it also certifies the mismatch votes for retained pairs.

The hybrid code has a six-word local window: four owned words and one word of context on each side. It imports only contiguous certified portions of adjacent published spans (`bits_tb8.h:790–800`). Although the reset search examines local words beyond the current certified interval, it accepts the first reset only if `q<R` and the last reset only if `r>=L`. An unknown reset outside the interval therefore cannot establish a certificate.

For an interior interval the left bound only increases and the right bound never increases. If the final interval after a hybrid micro-window still covers every owned pair, those pairs were certified after every earlier step in that micro-window. This justifies retaining the per-step palindrome mismatch bits and checking coverage at the end. Failure is sticky over later micro-windows. For a normal tile with the real middle, its right bound follows the true physical extent; the same coverage argument applies to all physical owned pairs at each earlier step. This resolves the apparent concern that a final-state certificate alone might silently validate an earlier speculative palindrome vote.

The outer-prefix growth rule is exact: the first non-9 pair encountered from the outside determines final overflow by whether its sum is at least 10. If every pair is 9, a canonical word has even length and carry zero throughout. The bounded 128-pair search does not assume a later reset absent: when it cannot establish the bit from certified data, it fails and requires replay. `ph_init` checks the initial growth bit. At each subsequent step `ph_track` checks the preceding search result against the current prefix certificate before certifying that step. The computed bit after the final step is unused; only bits 0 through K-1 enter the control tape. A hybrid tile rejects an uncertified tape (`cuda196_v8.cu:64–67,131–165`).

## What is trusted and what is replayed

The time-blocked path deliberately writes speculative state, including outside certified regions. In the CUDA backend `dFail` is combined with `atomicOr` and is not reset between launches in one host verification window. `tbSync` reads it before clearing it (`cuda196_v8.cu:286–303`). Thus a later successful launch cannot erase an earlier reported certification failure.

`Engine::advance` saves the beginning of the host window. Either a failure or a palindrome flag restores that backup and replays the whole window with the per-step core (`driver8.h:198–239`). The restore also clears the alternate buffer and data above the saved extent (`cuda196_v8.cu:311–325`). This avoids retaining stale speculative tails. The per-step path selects the first zero-mismatch step, restores, and advances only to its predecessor before materializing the candidate integer. `reportPalindrome` performs a scalar decimal palindrome check on that materialization.

A certified time-blocked palindrome flag contradicted by exact replay causes an exception. A flag from a failed speculative window may harmlessly disappear during replay. A missed flag from genuinely incorrect arithmetic would not automatically force replay, so the fallback is not a replacement for correctness of the core or the interval certificate.

Normal checkpoint creation deliberately retains the predecessor folded state and materializes the following decimal integer. The supplied checkpoint value and its claimed starting iteration are trusted input. The SHA-256 metadata authenticates bytes against a supplied digest, not the assertion that the checkpoint lies on the 196 orbit. Consequently a continuation is a finite verification conditional on its starting checkpoint, unless that ancestry is independently established.

## Concrete driver robustness defects

`driver_progress_probe.cpp` includes the unmodified `driver8.h` but substitutes a tiny mock backend. It uses input `196`, a short horizon, and deliberate exceptions to stop non-progress after two calls. It launches no CUDA, runs no production executable, and reads or writes no checkpoints. Results are in `driver_progress_probe.jsonl`.

| Accepted option | Observed source/probe behavior | Scope |
| --- | --- | --- |
| `--window=-1` | After one outer pass `Engine.it=-1`; the next pass starts again. `min(window, remaining)` supplies negative work and `done` moves backwards. | Malformed CLI progress defect, not a valid-configuration arithmetic failure. |
| `--batch=0` through run-mode setup | Two successive calls request zero steps; iteration remains 0. | Run mode lacks the positive-batch check present in bench mode. Actual GPU/backend handling may error instead; the bounded mock establishes driver non-progress if the backend returns. |
| `--halo=-4` | `setup` accepts `conf.HW=-4`. It checks divisibility by four but not positivity. | Missing geometry validation demonstrated. No resulting memory fault or wrong numerical result was claimed or tested. |

References: `driver8.h:121–139,167–195,198–218,297,327–339`. These malformed options do not refute the valid-input interval argument.

## GPU concurrency item: multiple clears of `S.hyok`

`State::hyok` is a plain shared `int`, initialized to 1 by thread 0 before barriers. Each failing owned group performs `S.hyok=0` (`bits_tb8.h:887`). The CUDA loop assigns groups to distinct threads, then executes a block barrier before thread 0 reads the flag (`cuda196_v8.cu:73–86`). There is no atomic operation, volatile qualifier, or reduction at that store.

This is not merely a hypothetical unreachable branch. `hyok_writer_probe.cpp` constructs a canonical 10,000-digit even-length state, with no center constraint, using pair values 2 in the first 256 positions, 9 in positions 1920 through 4415, and 0 elsewhere. The positive outer sum realizes a canonical decimal integer. With K=1, tile 64 words, halo 4 words, and block 1, the prefix growth tape is certified and the hybrid branch is selected. The 16 owned groups, assigned to CUDA thread IDs 1 through 16, each reach the same-address zero store. The CPU probe invokes the header functions sequentially only to establish those branch conditions. Its exact output is `hyok_writer_probe.json`.

All possible concurrent worker writes have the same value zero; no worker restores one. The subsequent barrier supplies a phase boundary but does not serialize the preceding simultaneous stores. This deserves explicit CUDA memory-model/racecheck assessment, or an atomic clear/block reduction as hardening. **This audit did not execute a GPU kernel, observe a stale read, demonstrate a lost failure flag, or establish an arithmetic error caused by these stores.** It should not be reported as a GPU-runtime-confirmed bug. The mathematical certificate above assumes a failure flag is preserved as intended.

## Use in the Lychrel proof search

This implementation is useful as an efficient exact transition oracle and as a model of bounded dependence certificates. It exposes the decisive carry resets at non-9 columns and shows how speculative local computation can be checked and discarded. These ideas can accelerate counterexample discovery and finite orbit replay.

It does not supply the missing positive all-length language invariant. An interval certificate says that particular columns in a particular finite block of steps are exact; it does not assert an infinite supply of resets, recover discarded unknown columns from a finite observation class, or prove forward closure of a safe regular language. The finite computations and the mathematical transition identities therefore provide no all-time conclusion for 196 or any other alleged decimal Lychrel seed.

Using a shared header in CPU and GPU implementations checks agreement with that header, not independent correctness of its mathematics. Our finite-language certificate verifier should continue to use ordinary integer reversal/addition or a separately proved scalar transducer, including independent palindrome checks and all-edge closure obligations.

## Reproduction

From this review directory, obtain the pinned upstream archive (access to
this private repository is required). These commands create temporary source
files and do not modify the upstream checkout:

```sh
review_source_tmp=$(mktemp -d)
git clone --no-checkout https://github.com/taco-jpg/p196-algorithm.git "$review_source_tmp/repo"
git -C "$review_source_tmp/repo" show 8219522a02d46fbb72a6ee38819e5723b8c8fc9f:lychrel196_v8.zip > "$review_source_tmp/v8.zip"
python3 -m zipfile -e "$review_source_tmp/v8.zip" "$review_source_tmp/extracted"
v8_source="$review_source_tmp/extracted/lychrel196_v8"
```

Then compile and run:

```sh
g++ -std=c++17 -O2 -pthread -I"$v8_source" driver_progress_probe.cpp -o driver_progress_probe
./driver_progress_probe > driver_progress_probe.jsonl
g++ -std=c++17 -O2 -I"$v8_source" hyok_writer_probe.cpp -o hyok_writer_probe
./hyok_writer_probe > hyok_writer_probe.json
```

Both probes completed with exit status 0. All subprocesses started for this audit have finished. The retained files are the report, source probes, exact small outputs, and manifest; no upstream source archive is duplicated here.

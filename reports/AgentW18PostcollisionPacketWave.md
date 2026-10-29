# W18: delayed central packet nucleation after the neutral-9 shield collapses
**Label: COMPUTED** (actual decimal digit arithmetic; not an infinite Lychrel certificate, not Lean verified).

## Concrete post-collision mechanism
Use the earlier independently checked W18 family `N0(Q)=5(99)^Q4`. Instead of stopping when its central all-nine band vanishes, perform true ordinary base-10 reverse-and-add on the full digits for each of Q=4138,4139,4140 through **25,000** transitions, checking that *none of the 75,003 states is a palindrome*. The first Q has an all-nine band of length 2 at t20000, length1 at t20002 and length0 at t20004, but its real orbit continues, not becoming a palindrome through t25000.

At each time compare the **entire least-significant-first digit strings** of neighbouring Q values. Define the canonical mismatch kernel by removing the longest equal prefix and the longest equal suffix without overlap. Initially the change Q -> Q+1 is a single central insertion of `99`. The first distinct physical event is at **t=20006** for Q4138->4139: old kernel `1`, new kernel `892`, with 8,277 exactly equal digits on *each* side. Q4139->4140 still has the pure `99` insertion at t20006, and suffers the same `1 -> 892` event at **t=20010**. For Q4140->4141 its first event is t20014. Thus there is a delayed *defect-packet nucleation*, not a simultaneous infinite wall collision. This mechanism is constructive and appears at reproducible locations in actual integers.

At t=25000 the Q4138 and Q4139 digit strings have lengths 18,644 and 18,646. Their mismatch kernels have lengths 3,853 and 3,855; both outer regions remain identical, with low common prefix 7,395 digits and high common suffix 7,396 digits. The untouched portions occupy 14,791/18,644, approximately 79.33% of the shorter numeral. For Q4139 vs Q4140 the analogous numbers are common prefix 7,390, common suffix 7,390, kernels 3,866 and 3,868. This **measured finite cone** is not a universal finite-speed theorem; carries could propagate farther at a later step.

| time | length Q4138 | Q4138 vs Q4139: equal low | mismatch lengths | equal high |
|--:|--:|--:|--:|--:|
| 20000 | 16552 | 8277 | 0 -> 2 | 8275 |
| 20006 | 16555 | 8277 | 1 -> 3 | 8277 |
| 20100 | 16594 | 8259 | 75 -> 77 | 8260 |
| 20500 | 16751 | 8190 | 371 -> 373 | 8190 |
| 21000 | 16969 | 8106 | 756 -> 758 | 8107 |
| 22000 | 17390 | 7927 | 1533 -> 1535 | 7930 |
| 23000 | 17812 | 7751 | 2310 -> 2312 | 7751 |
| 24000 | 18237 | 7579 | 3077 -> 3079 | 7581 |
| 25000 | 18644 | 7395 | 3853 -> 3855 | 7396 |

## Insertion-break clock and independent arithmetic
The separate `seam_clock.cpp` mines 40 adjacent differences Q4138..4178. It constructs the exact pre-collision family at t19990 using the **already established** two-wall all-nine carry lemma (where band length 6), and from that point executes direct full decimal-digit reverse-and-add. The first failure of the pure `99` insertion occurs at times `20006,20010,20014,20019,20024,20029,20034,20038,...,20192` for Q4138..4177. The 39 inter-level delays range from **3 to 8**; the series is not four-periodic. Complete 40-row ledger: `calculation/new_structures/agent-W18/seam_clock.tsv`. This is a new clock of *when the collision starts*; there is no claim that its 40 levels prove the pattern for arbitrary Q.

A separate `postcollision_bigint.cpp` represents the whole positive integer in radix 10^9 limbs, converts it to an ordinary decimal string, reverses that string and adds limbs. It independently checks no palindrome in Q4138's 25,001 states, including beyond t20004, and agrees with direct-decimal `seam_wave.cpp` at t25000: 18,644 digits and full decimal checksum **704483961** modulo 1000000007. Since the whole-number algorithms are different, this provides an independent check of the postcollision arithmetic, not only the earlier protected-band model.

## What breaks, and the next constructive target
The old `U++9^L++V` representation is invalid once the band length drops below 2. A nontrivial replacement packet forms at the seam and widens, while large outer regions remain identical. To obtain infinite closure, seek a parameterized **packet substitution/transducer** that recognizes the growing mismatch kernel, and a regenerative event restoring the exterior guard, not an assumed recurrent short fixed-width centre. The exact data give fresh seeds for a finite-state, charge-aware **moving-seam** or two-counter macro-certificate. No all-time safety or stationary glider is asserted.

Run `bash calculation/new_structures/agent-W18/reproduce_seam.sh`; this compiles and checks direct 25k all-three orbits, the independent bigint check, and the 40-level insertion clock. Full repo `verify.py --changed` is unavailable in this container without GitHub HTTPS checkout; no Lean code is added.

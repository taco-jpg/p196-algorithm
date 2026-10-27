# Agent 4 / T2: base-10 period-22 full-B census, one unresolved stream

**STATUS: COMPUTED PARTIAL CLASSIFICATION / ONE KNOWN POSITIVE B RETURN / ONE CAPPED-UNDECIDED.** No Lean theorem and no decimal Lychrel certificate. Coordination issue #289, depends on corrected 128-bit B automaton and necessary head filter in core Draft PR #323.

## Exhaustive input coverage

There are exactly **190,746** rotation-inequivalent binary overflow streams of length 22. The necessary 18-state first-coefficient automaton (PAPER proof in parent report) leaves **1,000** streams. A stream rejected by that filter cannot be emitted by an accepted B cycle, whatever its B width.

| Number of overflows | Necessary survivors | Exact B-position outcomes |
|---:|---:|---|
| 6 | 4 | 4 EXHAUSTED |
| 7 | 107 | 107 EXHAUSTED (Agent 2 independently owns #322) |
| 8 | 445 | 444 EXHAUSTED, 1 ACCEPT |
| 9 | 392 | 392 EXHAUSTED |
| 10 | 51 | 50 EXHAUSTED, 1 CAPPED/UNDECIDED |
| 11 | 1 | 1 EXHAUSTED |
| All other weights | 0 | excluded by necessary filter |

**Overall:** 998 EXHAUSTED B negatives; 1 B ACCEPT that is precisely a known nonprimitive 11-cycle repeated twice; 1 B stream remains UNDECIDED. Therefore an unqualified no-p22-B-cycle claim would be false, and a complete period-22 certificate exclusion cannot yet be concluded from this census.

## The sole accepted B (pre-existing, NOT new)

The positional B solver accepted

    g = 1110001000011100010000 = (11100010000)^2
    e = 1010011001110100110011 = (10100110011)^2

at depth 29, visiting 5,758,823 positional states. The exact B word recovered in witness mode (least-significant coefficient first) is

    B0 = [18,14,0,2,10,10,6,0,7,8,18,9,1,5,9,6,4,3,12,10,10,12,13,10,13]

Independent coefficient-level decimal normalization and suffix-nine trimming verify **B11=B22=B0**, and exact repeated e/g streams. Thus the p22 acceptance is merely the existing p11 B-cycle repeated twice; no primitive p22 B structure has been established by it. The original neutral-band README already records a COMPUTED all-center-length absence for the p11 driver with k=2; this pre-existing center obstruction covers this *particular old driver only*, not the unresolved alternative stream.

The other five-second timed-out p22 weight8 word g=1010100101000110001000 was isolated and **EXHAUSTED** at depth40/states3,280,645 in 17.79s, peak RSS 263,568 KB.

## Last unresolved stream, exact resource evidence

g=1001011100010010111000 has ten overflows; its 11-bit *overflow* motif repeats twice. This does NOT by itself force B or the carry e stream to have period 11, and existing p11 B enumeration does not include that motif.

- 5s initial timeout: UNDECIDED.
- 10M-state isolated attempt: **CAPPED**, depth20 / 10,363,705 states, wall48.70s, peak RSS 816,612KB.
- 40M-state isolated attempt: **CAPPED**, depth43 / 40,148,945 states, wall234.13s, peak RSS 2,980,228KB, exit code3. Strict process budgets: 240s timeout, 6.5GB virtual-memory guard, one process.

No accepting state was observed before the cap, but that observation is NOT a negative proof or even an exact B no-return decision.

## Reproduction

Compile the exact source from PR #323; then run the standalone all-overflow harness on this branch:

    c++ -std=c++17 -O2 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
    c++ -std=c++17 -O2 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
    python3 calculation/agent-4/test_low_digit.py
    python3 calculation/agent-4/run_p22_all.py

The harness insists on the known nonprimitive ACCEPT, independently checks B11=B22 and its e/g words, and will not report any capped stream as negative. It uses 2M visited states/5s for ordinary streams; 10M/90s for known positive; and 40M/250s for the last hard case. All resource caps and nonzero exits are reported. Isolated hard case:

    calculation/agent-4/fixed_g_B_probe 1001011100010010111000 40000000 140

**STUDIO REQUEST** in #289 asks a single source-audited 80M-state, 20-min/8GB attempt, with terminal status, RSS, and duration. It has not been reported as executed.

## Explicit limitations

No complete base10 p22 negative, no primitive new B-cycle, no matching center C, no base-10 cycleOK certificate, no ordinary orbit-of-196 theorem, no universal one-neutral-band impossibility. The p11/k2 all-length C exclusion is cited as previous COMPUTED work, not a new Lean theorem. No Lean module or `python3 tools/verify.py --changed` PASS. Independent second-agent review is required for new finite negatives.

**DRAFT / UNVERIFIED / DO NOT MERGE.** Does not edit README, RESULTS or other agents' paths.

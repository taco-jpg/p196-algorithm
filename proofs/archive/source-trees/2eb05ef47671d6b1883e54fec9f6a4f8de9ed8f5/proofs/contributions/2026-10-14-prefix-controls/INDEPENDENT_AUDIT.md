# Independent fixed-clock prefix audit

**Result: PASS.** The reported classifications for widths one through
three agree with an independent ordinary-integer transition oracle and
an independent functional-graph algorithm. No larger width was searched.

The audit checked 13,716 distinct (prefix, incoming-bit) transitions and
classified 27,432 phase-augmented states across the nine existing tests.
Exact source hashes and every surviving cycle edge are retained in
`independent_audit.json`.

## Independently reproduced counts

| Width | Repeated schedule | Total phase states | Eventually unsafe | Safe-cycle basin states | Longest finite escape |
|---:|:---:|---:|---:|---:|---:|
| 1 | 0 | 18 | 18 | 0 | 1 |
| 1 | 1 | 18 | 18 | 0 | 1 |
| 1 | 01 | 36 | 36 | 0 | 1 |
| 2 | 0 | 342 | 339 | 3 | 13 |
| 2 | 1 | 342 | 339 | 3 | 12 |
| 2 | 01 | 684 | 678 | 6 | 13 |
| 3 | 0 | 6,498 | 6,498 | 0 | 21 |
| 3 | 1 | 6,498 | 6,498 | 0 | 21 |
| 3 | 01 | 12,996 | 12,996 | 0 | 24 |

Unsafe here means that the prefix no longer excludes both exact
palindrome-predecessor branches. It does not mean that the actual next
integer must be a palindrome.

## Integer transition oracle

For a prefix p=(p_0,...,p_{k-1}) with p_0>0 and a requested incoming bit
gamma, construct least-significant-first digits

\[
(\max(p_i-9,0))_{i=0}^{k-1},\quad 9\gamma,\quad
(\min(p_i,9))_{i=k-1}^{0}.
\]

This is a canonical positive integer. Its symmetric pair coefficients are
p, 18 gamma, reverse(p). The central column forces its outgoing carry to
gamma, regardless of the carry entering that column. Ordinary integer
addition with the reversed decimal string therefore realizes precisely
the requested one-step prefix transition.

Every prefix transition produced by `fixed_clock_controls.next_prefix`
matches this integer oracle. For gamma=0 it also matches
`fixed_zero_prefix.successor`.

## All reported cycle edges have actual one-step realizations

| Clock | Prefix / phase | Input bit | Ordinary seed | Actual next integer | Next prefix / phase |
|:---|:---|---:|---:|---:|:---|
| 0 | (8,12) / 0 | 0 | 89030 | 92128 | (17,4) / 0 |
| 0 | (17,4) / 0 | 0 | 94008 | 174057 | (8,12) / 0 |
| 1 | (8,11) / 0 | 1 | 89920 | 92918 | (17,3) / 0 |
| 1 | (17,3) / 0 | 1 | 93908 | 174847 | (8,11) / 0 |
| 01 | (8,11) / 1 | 1 | 89920 | 92918 | (17,3) / 0 |
| 01 | (17,3) / 0 | 0 | 93008 | 173047 | (8,11) / 1 |
| 01 | (8,12) / 0 | 0 | 89030 | 92128 | (17,4) / 1 |
| 01 | (17,4) / 1 | 1 | 94908 | 175857 | (8,12) / 0 |

These are separate finite realizations of the edges. For example, the
first seed advances to 92128, not to the 94008 seed used to realize the
next edge. The table does not concatenate into one infinite integer orbit.

## Independent graph method

The reviewed scripts label forward paths. This audit instead:

1. Constructs all transitions using the integer oracle.
2. Runs reverse breadth-first search from every unsafe state to obtain
   the exact finite escape distances.
3. Removes zero-indegree vertices from the remaining safe subgraph to
   separate cycle vertices from their incoming basins.
4. Extracts the surviving cycles and compares them up to rotation,
   retaining the clock phase.

No discrepancy was found in the reported state counts, cycle basins,
escape horizons, phases, or complete cycle lists.

The absence of cycles at width three concerns only the imposed clocks
0, 1, and 01. Actual interior carries can follow other histories, so these
finite tests do not prove universal prefix escape or decimal Lychrel
existence. A safe cycle disproves escape for its particular abstract clock.

Reproduce with:

```sh
python independent_audit.py
```

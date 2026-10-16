# Direct NFA ancestry pass

**No positive Lychrel invariant was found.** This pass avoided determinizing
the saved 6,680-state safe-two-ancestry NFA. It completely excluded one
precise acceptance family by a finite arithmetic certificate: no nonempty
union of its terminal-component languages is safe and forward closed.

There are 8,396 original terminal flags `(state, center)`. Exact NFA × current
palindrome-predecessor reachability initially excluded 3,466. The positive
search retained every other flag until a concrete terminating word was found
in its component. All 8,396 flags were eventually excluded, in 11.07 seconds.
The search used at most 150 representative-tree trials and 200 ordinary
reverse-add operations per tested word; it finished after trial 135.
These bounds limit discovery only. Every final exclusion has an explicit
finite witness, and every original flag is covered.

`check_terminal_certificate.py` independently checked all 8,396 NFA paths
and ordinary integer orbits. It imports neither the discovery program nor
the carry transducer. The largest first palindrome time in the certificate
is 72, the largest starting integer has 29 digits, and the largest resulting
palindrome has 56 digits. The complete proof is
`terminal_acceptance_result.json`; its hash and audit are in
`terminal_certificate_audit.json`.

This is not a termination claim about 196 or all inputs. Each excluded
component contains at least one terminating word, which is enough to forbid
accepting that entire component. A different word in the same component may
remain unresolved. The certificate does not exclude conjunctive conditions
on several NFA paths, Boolean tests on full reachable configurations, other
transition structures, or arbitrary regular invariants.

The direct search settled this acceptance family before an antichain
inclusion check was needed. No incomplete inclusion search is described as
an exclusion, and no full subset automaton was constructed.

## Structural ancestry facts

Write `C` for all canonical pair words, `B` for palindrome predecessors,
`G` for the exact pair-word reverse-add map, and

`S0=C`, `S_(r+1)=G(S_r minus B)`.

1. The sets descend: `S_(r+1) subset S_r`. This follows from `S1 subset C`
   and monotonicity of image and set subtraction by fixed `B`.
2. Exactly `G(S_r minus B)=S_(r+1) subset S_r`. This is closure into `S_r`,
   not closure into its safe part. Root's literal 89 control gives a word
   in `S_r minus B`, for every `r<=22`, whose image is in `B`.
3. Their intersection contains no finite word. The checked width theorem
   `t+4*L0 <= 4*Lt+4` gives `r<=4L` for any positive r-step ancestor of a
   word of width L, since `L0>=1`. Hence that word is outside `S_(4L+1)`.
   This applies even without the safety restriction.
4. Empty ancestry intersection does **not** refute forward nontermination.
   If `L` is a nonempty safe forward-invariant language, then `G^r(L)` is
   nonempty, safe, forward invariant, and contained in `S_r` for each finite
   r. The witnesses may move to larger words with r. An intersection or
   compactness argument cannot produce a fixed finite seed from ancestry.

The 89 control uses

`w = ((17,9,10,11,9,9), no center)` and
`G(w) = ((8,8,1,3,2,0), center 0)`.

It corresponds to ordinary integers
`955594506548 -> 1801200002107 -> 8813200023188`, with the final integer a
palindrome. Direct evaluation of the saved NFA accepts both pair words;
this independently exercises its exact safe-two-ancestry membership.

## Why the certificate is an all-length exclusion

For a terminal flag f let `C_f` contain every canonical word with an NFA
path ending at that flag. Choosing an arbitrary flag set F accepts
`L_F = union_(f in F) C_f`. For every f the certificate gives a word
`w_f in C_f` and a positive integer h such that `G^(h-1)(w_f) in B`.

If `L_F` were safe and forward closed and f belonged to F, it would contain
`w_f`, then all its successive pair words, including the displayed word of
`B`. This is impossible. Thus F is empty. The proof covers all accepted
word lengths because acceptance of an entire component forces acceptance
of its one recorded witness; no maximum orbit length is imposed on a
hypothetical invariant.

The exact technical limitation is visible at 1675. Its pair word has only
one accepting NFA terminal flag, `(6679, no center)`, the shared terminal
used after the extra pair emitted by odd overflow. This component also
contains a certified terminating word. Ordinary terminal-flag selection
cannot use the nonaccepting residual NFA states or impose correlation
between alternative complete histories. Such additional information is
outside this completed exclusion and would need a new positive certificate.

## Reproduce

From the project root:

```sh
python3 main_existence_attempt/ancestry_direct_pass/language/nfa_terminal_synthesis.py --seconds 300 --trials 150 --orbit-limit 200
python3 main_existence_attempt/ancestry_direct_pass/language/check_terminal_certificate.py
python3 main_existence_attempt/ancestry_direct_pass/language/check_ancestry_controls.py
```

The NFA is read from the previous pass and has SHA-256
`6a1e9b8f87f308c8f5c6099c853674c30c66dd1878daa97b2bb646252f0d1039`.
All new files are in this directory. Previous return-pass artifacts were
left unchanged. All subprocesses stopped. No proof of decimal Lychrel
existence, Lean formalization, novelty, or external peer review is claimed.

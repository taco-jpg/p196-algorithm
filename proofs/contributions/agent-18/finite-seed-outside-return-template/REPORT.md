# Agent #18 — finite-seed exploration outside the fixed two-gap return-template ansatz

Status: WIP. This is an exact finite computation, not an infinite-time result and not a Lean-accepted theorem.

## Candidate

Seed: `10828`.

Using the ordinary decimal map `T(n)=n+reverseDecimal(n)`, the first palindrome occurs exactly at time 39. States at times 0..38 are nonpalindromic.

A structural test was also applied to every state 0..39. Its mirrored pair-word was tested against the Agent #8/109 fixed two-gap template shape, with phase c in {1,...,17}\{9} and positive outer/interior band lengths. No state in this trajectory matched that template shape.

This gives a concrete finite safe prefix that does not rely on the currently studied fixed two-gap return-template ansatz. It is not an infinite-safe construction and says nothing about 196.

## Exact trajectory

| t | n | width | palindrome |
|---:|---:|---:|:---:|
| 0 | 10828 | 5 | no |
| 1 | 93629 | 5 | no |
| 2 | 186268 | 6 | no |
| 3 | 1048949 | 7 | no |
| 4 | 10547350 | 8 | no |
| 5 | 15921851 | 8 | no |
| 6 | 31734802 | 8 | no |
| 7 | 52578515 | 8 | no |
| 8 | 104166040 | 9 | no |
| 9 | 144827441 | 9 | no |
| 10 | 289555882 | 9 | no |
| 11 | 578111864 | 9 | no |
| 12 | 1046223739 | 10 | no |
| 13 | 10419450140 | 11 | no |
| 14 | 14524941541 | 11 | no |
| 15 | 29039884082 | 11 | no |
| 16 | 57088777174 | 11 | no |
| 17 | 104266565249 | 12 | no |
| 18 | 1046832227650 | 13 | no |
| 19 | 1614054614051 | 13 | no |
| 20 | 3118219118212 | 13 | no |
| 21 | 5246338246325 | 13 | no |
| 22 | 10482766582750 | 14 | no |
| 23 | 16211333311151 | 14 | no |
| 24 | 31322666622412 | 14 | no |
| 25 | 52745333244725 | 14 | no |
| 26 | 105489566599450 | 15 | no |
| 27 | 160485232583951 | 15 | no |
| 28 | 319870465168012 | 15 | no |
| 29 | 530732029246925 | 15 | no |
| 30 | 1060374949483960 | 16 | no |
| 31 | 1754224444214561 | 16 | no |
| 32 | 3408348888439132 | 16 | no |
| 33 | 5727697776877175 | 16 | no |
| 34 | 11445484554844450 | 17 | no |
| 35 | 16890330103298861 | 17 | no |
| 36 | 33779560206608722 | 17 | no |
| 37 | 56560220413206455 | 17 | no |
| 38 | 112020451815413020 | 18 | no |
| 39 | 132334969969433231 | 18 | yes |

## Reproduction

`verify.py` recomputes every transition with Python integers, checks palindrome status at every time, and independently checks the pair-word template predicate.

Expected result: `first_palindrome_time=39`, `nonpalindromic_prefix_through=38`, and `template_matches=0` for times 0..39.

## Scope

- Exact decimal arithmetic only.
- Finite horizon only.
- The template test is a structural membership test for the currently published fixed two-gap shape; it is not a proof that no other symbolic encoding can represent the same trajectory.
- No claim about the orbit of 196.
- No infinite-safe-seed claim.
- No Lean acceptance yet.

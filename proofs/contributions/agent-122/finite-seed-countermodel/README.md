# Agent 122: finite-seed countermodel, checkpoint 1

LEAN-CHECKED supporting numeral lemmas; the total countermap remains WIP. No independent review or default-branch integration is claimed.

SparseNumbers.lean proves the original report's c(a,j)=10^(a+j)+10*a+9 (a>=3) labels have canonical width a+j+1, are injective in their two labels, are not palindromes, and are not actual one-step palindrome predecessors. It also proves that b(a,k)=10^(a+k+1)+2 is nonpalindromic but its true reverse-and-add successor is a palindrome. The definitions are ordinary natural numbers and the imported Lychrel196 arithmetic, not symbolic surrogates.

The larger task is the written-only countermodel in research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md section 2. No total-map, all-seed termination, unbounded-delay, density, full pair-word quotient, or actual 196 conclusion is established by this first checkpoint.

Pinned source: main eec3d5f3646cab50abad6e610ea19626cd249070. Lean 4.19.0 (6caaee842e94), core and Std. Imports reuse Agent108 LeadingWitness and Agent13 Family rather than reproving their bounds and singleton-value formulas. One import-only adapter copies AutonomyDefs into a disposable build replacing import Lychrel196Research by import LychrelDigitSums. The complete original base, minus import Std, is verified as a byte-identical substring of the continuation, so this avoids duplicate global declarations without changing mathematics. No collaborator file is edited.

Local incremental builds and the audit of all 14 exported supporting theorems succeeded. Reported axiom union: propext, Classical.choice, Quot.sound. No sorryAx or compiler-trusted reduction appears in these audited chains. A complete fresh rebuild and reproducibility/evidence publication are in progress within this active session; source-only inspection is not called independent execution. All.lean is the candidate entry point; Audit.lean audits every export.

# Agent X02: exponentially branching two-step decimal carry-erasure funnel
Label: PAPER PROOF (all-length two-step identity); COMPUTED (independent 20,000-step replay).
For decimal a=5..8 and h>=1, the 2^(h-1) pairword halves [a+9] ++ {a,a+9}^(h-1) represent distinct positive nonpalindromic N0 seeds.
Every such seed has identical second reverse-and-add iterate N2=(a+1)(2a-9)^(2h-2)(2a-10)a, interpreted as decimal concatenation.
The intermediate N1 pairword is [a] ++ [2a]^(2h-1) ++ [a] regardless of the independent binary choices; N0,N1,N2 are nonpalindromic.
Exhaustive Python bigint check: 8,188 seeds for a=5..8,h<=11, all pass.
For a=8,h=20200, independent ordinary-digit and GNU GMP arithmetic replay 20,000 steps from N2=9(7)^40398 68, 0 palindromes.
Each step retains an exact interior six-phase pairword band, 489,875,762 pair positions checked in EACH replay; final 48,684 digits and matching FNV64 e55e4d3ead4fa4c0.
This is a finite-horizon positive mechanism, NOT a base-10 Lychrel certificate and NOT an infinite palindrome-avoidance theorem.
Code and compact data: calculation/new_structures/agent-X02/; proof and commands: reports/AgentX02BinaryFunnel.md.

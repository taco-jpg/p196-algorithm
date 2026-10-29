# Agent X08: short-seed paired-parity trajectory families
**COMPUTED**, base 10; not an infinite Lychrel certificate.
- Family A: decimal four-digit word a b c d with 1<=a<=8, 4<=b<=9, c=13-b, d=8-a: 48 seeds, all first successor 9438. Representative 1497.
- Family B: decimal five-digit word a b 9 d e with 1<=a<=9, 6<=b<=9, d=15-b, e=10-a: 36 seeds, all first successor 116960. Representative 16999.
- Each seed family is therefore a common real-integer trajectory from step 1 onward.
- Every iterate t=0..100000 has an odd mirrored digit-pair sum at index <=22 (A) or <=24 (B); hence all are non-palindromes. C++ exact decimal digit-vector arithmetic; 100000-step representative lengths 41387 and 41255.
- Independent Python ordinary-bigint and C++ positional arithmetic agree on the **entire numerical trajectory**, SHA-256 of all 20001 decimal states/newlines: A 8ab0894c7daf435e5e5af2c4b1bbf2b5e62f4aea3558ff9fefba38753a49d325; B 2cd0f8b0357fe7bab6d27c2186ed565530fb194a77dfd2b35a756d3b7c89e289.
- Reproduce: sh calculation/new_structures/agent-X08/run.sh; code replay.cpp, independent.py; details reports/AgentX08ShortSeedParityFamilies.md.
- **Not claimed:** palindrome avoidance past step 100000, invariant/inductive parity language, an infinite Lychrel certificate, a periodic centre, Lean verification, or anything about 196.

# A positive 361-seed basin for the decimal 44-step travelling head

**COMPUTED, exact finite scope.** This is an extension of \`AgentN17DecimalWake44\`, but is a new positive basin result: it shows that the moving head is not a one-seed numerical accident. No exclusion or no-go is claimed.

## Family and finite claims

Use the rooted decimal pairword A0 from \`reports/AgentN17DecimalWake44.md\`, with prefix length 39 and bulk spatial period 20. For half-width h=500, form a palindromic pairword P of length 1000: its lower half agrees with A0 except that its **final two coefficients** P[498],P[499] are replaced by arbitrary (a,b) in the full range 0..18, and the upper half mirrors it. Convert each pair coefficient p into decimal digits (max(0,p-9), p-max(0,p-9)) from the low and high ends, respectively. This defines exactly 19^2=361 distinct initial numbers, each with 1000 digits.

For each of all 361 cases, ordinary decimal reverse-and-add was replayed from t=0 through 1500 inclusive, with no palindrome. Every step has the exact alternating overflow 1010... and the rooted eight-phase exterior. The minimum measured first disagreement with that exterior is coefficient index **157**, leaving the odd nonpalindrome witness in the first 39 coefficients intact.

Define front f_t as in the previous report. For **every** pair (a,b) and **every** t=716..1500, both engines verify \`f_t=f_(t-44)-10\` and equality of all 60 pair coefficients at relative offsets [-20,40) in the comoving frame. This is 361*(1500-715)=**283,385** individual 44-step comparisons. There is at least one failure at t=715, and no later failure in the tested interval. The 60-cell head has **27 distinct phase-aligned words at t=800**, distributed among the 361 seeds (class sizes in lexicographic head order: 7,10,3,6,6,4,4,34,7,16,8,3,1,1,15,11,31,18,31,17,16,70,17,3,15,3,4). This is a family of glider states rather than one universal state.

## Independent evidence

\`universe.cpp\` uses a little-endian digit-vector engine and direct palindrome comparison. \`universe_gmp.cpp\` independently constructs decimal seeds, performs \`mpz_add\` against a number parsed from reversed decimal text, and extracts pair coefficients from the resulting big integer. Both enumerate exactly the double loop a=0..18, b=0..18 and replay all 1500 steps. Both recompute front positions and rolling 44-step comoving head equality from every literal state; their shared exact summary is: cases 361; minfront 157; last failure 715; late comparisons 283385; head states 27; palindromes 0; odd-witness failures 0; overflow failures 0. \`universe.cpp\` also prints the complete 27 distinct 60-character head states and their multiplicities, which add to 361. No probabilistic sampling is used.

Reproduce from repository root:

\`\`\`bash
bash calculation/new_structures/agent-N17/run_universe.sh
\`\`\`

On systems without GMP headers/library, the digit-list engine alone runs via \`g++ -O3 -std=c++17 calculation/new_structures/agent-N17/universe.cpp -o /tmp/n17-universe && /tmp/n17-universe\`, but that alone does not reproduce the independent validation.

## What this redirects

The outgoing wave head is robust to these two arbitrary terminal packet digits and can have multiple wake-head states, a promising starting point for a finite-state travelling-head generator. Yet its measured displacement is **outward**, toward the fixed root, so even the proven finite family does not supply an infinite decimal Lychrel certificate. The needed next structural change is a wave moving inward, or a regenerative wake/boundary that prevents the head from reaching the root. Neither exists in this result.

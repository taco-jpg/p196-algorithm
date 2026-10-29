# AgentX23SixSiteCrystal96
- **COMPUTED**: a second positive decimal distributed-kink bulk clock, spatial period 6 and genuine temporal period 96 under g=1010..., with independently replayed 20,000 genuine decimal steps.
- All 19^3-1=6,858 nonneutral initially reflection-symmetric six-site rows (a,b,c,c,b,a) were enumerated; 6,854 reach a unique periodic carry orbit within 2,000 updates, and 4 enter the ambiguous all-9 neutral ring.
- Eventual minimal periods among 6,854 unique-carry rows: 2:18, 6:1636, 12:222, 18:3000, 24:10, 36:1572, 96:396; data in `period6_counts.csv`.
- Witness R=(18,12,6,6,12,18) has immediate temporal period 96, aligned with outer p8 clock; spatial 6 divides 48 overflows per 96 steps.
- Explicit seed pairword B ++ W^400 ++ R^2500 ++ reverse(R^2500) ++ reverse(W^400) ++ reverse(B), with B,W constants in source: 46,078-digit positive decimal integer.
- All t=0..20,000: full pairword agrees with independent GMP integer reverse-add, no palindrome, and alternating overflow schedule; final length 56,078 digits.
- The W20 exterior prefix retains >=3,465 cells and R6 centre suffix >=7,498 at every checked state; the interface nonetheless grows to 17,037 cells, so **no infinite certificate** is claimed.
- Reproduce: `cd calculation/new_structures/agent-X23 && g++ -O3 -std=c++17 crystal96.cpp -lgmpxx -lgmp -o crystal96 && ./crystal96 400 2500 20000 && g++ -O3 -std=c++17 ring6.cpp -o ring6 && ./ring6`.
- Code/data: `calculation/new_structures/agent-X23/`; discussion: `reports/AgentX23SixSiteCrystal96.md`.

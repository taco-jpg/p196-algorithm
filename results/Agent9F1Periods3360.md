# Agent9F1Periods3360
**COMPUTED.** Exact base-10 position-0 F1 legal overflow-necklace counts for each p=33..60.
Complete totals and primitive counts: `calculation/decimal_frontier/exterior_census/data/f1_b10_p33_60.csv`.
Weight-G and primitive-by-weight counts from semigroup/Burnside code; no state or time caps.
The binary relation semigroup has 434 reachable states, maximum shortest depth 17.
Run: `python3 calculation/decimal_frontier/exterior_census/py/f1_semigroup_count.py 10 60 /tmp/f1_out.json`.
Independent direct FKM check agrees at every (p,G), primitive split for all p<=44:
`c++ -O3 -std=c++17 calculation/decimal_frontier/exterior_census/py/f1_necklace_check.cpp -o /tmp/f1_check && /tmp/f1_check 44`.
Published controls p36=351150 and p40=1943815 reproduced.
**PAPER PROOF.** Existing mod-9 charge closure admits binary carry words e in number
2^p (odd p), (2^p+2)/3 (p=2,4 mod 6), (2^p+8)/9 (p=0 mod 6).
Run: `python3 calculation/decimal_frontier/exterior_census/py/f1_charge_mod9_count.py 60`.
**Not claimed:** F1 words are full exterior B-cycles; charge filters g alone; any decimal Lychrel certificate.

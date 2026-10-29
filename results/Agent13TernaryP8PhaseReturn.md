# Agent13TernaryP8PhaseReturn

**PAPER PROOF.** For the primitive ternary substitution `0→01,1→02,2→00`, no injectively coded interior length-32 factor can return after decimal overflow schedule `10101010` to an injectively coded aligned length-28 factor of the same substitution, with arbitrary shifts and **unrestricted seven intermediate pairwords**.
Exact necessary two-sided carry transducer; all four entering-carry pairs allowed every step, with prefix-cropping proof.
Complete shorter census: 5,814 coefficient tables × 72 exact length-28 factors = 418,608 cases, zero state-cap hits (cap 50,000, maximum 2,400), just 16 survivors at four tables `(0,8,17),(0,17,8),(18,1,10),(18,10,1)`.
Independent Python check of the four exceptional tables on all 80 length-32 factors: 320 cases, zero length-28 endpoint matches. Every longer match would imply a shorter match, so all tables are excluded at length 32.
Independent validation: 3,000 ordinary integer steps, 5,000 carry/prefix-cropping controls, exact factor-language comparison; mandatory b9/b13 control replay.
Full proof: `reports/Agent13TernaryP8PhaseReturn.md`.
Source, independent checker, resumable runner, commands and controls: `calculation/decimal_frontier/ternary_p8/`.
Reproduce: `sh calculation/decimal_frontier/ternary_p8/run.sh /tmp/agent13-ternary-p8`.
Scope: this substitution, overflow `10101010`, injective starting/eighth endpoint encodings and interior length≥32 only; no conclusion for rotation `01010101`, short centres, other languages, or general decimal Lychrel existence.
Not LEAN-VERIFIED; no result about 196.

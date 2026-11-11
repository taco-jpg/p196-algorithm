# Chain 8, T = 72: final state of the round-11 run (UNDECIDED)

The round-11 job `g381_T72_bfilt` (chain 8 clock 110001001000, T = 72, BB_10-filtered forward search toward the PR381
centre stream; code and command in `../../round11/chain6_chain8/FINAL.md`, binary `reachdisk128`) was still running when
round 11 was committed; `../../round11/chain6_chain8/logs/g381_T72_bfilt.log` stops at height 15.
`g381_T72_bfilt.log` here is the complete log (its first 2,520 bytes are that file). The run was stopped by hand on
2026-11-05 at height 34, with 3,836,399,833 orbits visited and the frontier not empty (176,992,715 new at height 34); the next layer
would have passed the 4e9 cap. No wire target was reached. Result: **UNDECIDED** (nothing claimed for T = 72).

Command (Studio, cwd round-11 work dir): `WINCHECK=10 WINDIR=wsets8 BFILT=1 EARLY=1 BPREFIX=bwinE ROT=1 WRAP=1 THREADS=6
nice -n 10 ./reachdisk128 10 72 110001001000 WIRE wd/g72b 4000000000 0.20`.

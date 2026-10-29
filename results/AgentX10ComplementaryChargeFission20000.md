# AgentX10ComplementaryChargeFission20000
**COMPUTED**, with a **PAPER PROOF** of the stated complementary-band carry identity and finite-gap pumping criterion; NOT an infinite decimal certificate.
For every R>=1 and digit a=0..9, let `N=u a^R (9-a)^R v`, u=10A+B, v=10C+D (two-digit u,v), s=A+D, t=B+C+1, s>=10,t>=10.
Then one ordinary base-10 reverse-add yields `H 0^(2R) L` exactly, `H=100+10(s-9)+(t-10)`, `L=10(t-10)+(s-10)` (L padded to two digits).
The 90 `(s,t)` channels were computed to 20,000 further steps by a two-end exact carry recurrence; 13 have a nonpalindromic separated-packet trajectory throughout this horizon.
Best channel: `88 4^R 5^R 49 -> 183 0^(2R) 37`; for EVERY R>=5976, the charged seed and all 20,001 successors are nonpalindromic (20,001 reverse-add operations, 20,002 states).
At R=5976 the charged seed has 11,956 digits, and after 20,001 operations the number has 20,264 digits. Full independent grade-school replay matches 20,001/20,001 predicted successor words.
Further 20,001-step full-word controls: R=5977 (same channel), and `88 4^5993 5^5993 75 -> 146 0^11986 63`; total 60,003 full-word and 60,006 nonpalindrome checks across those three runs.
Independent Python big integers validate 2,706 one-step identities over all 90 channels and six interior complementary choices; R=305 short controls include a=0 and a=4.
Exact symbolic threshold at step 20,000: `M=2R+2>=11953` for `(H,L)=(183,37)`, and `M>=11988` for `(146,63)`; no extrapolation past this horizon.
Code/data: `calculation/new_structures/agent-X10/{charged_edge_classification.cpp,charged_fission_replay.cpp,charged_identity_control.py,complement_front_probe.cpp,charged_fission_reproduce.sh}` and CSV/traces.
Reproduce: `bash calculation/new_structures/agent-X10/charged_fission_reproduce.sh`; full proof scope: `reports/AgentX10ComplementaryChargeFission20000.md`.
No recharged complementary band, no cyclic certificate, no infinite base-10 Lychrel or 196 proof, no Lean verification.

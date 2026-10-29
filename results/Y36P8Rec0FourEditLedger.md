# Y36P8Rec0FourEditLedger

**COMPUTED.** For the rooted decimal p8/m20 rec0 template with q,k>=20, fixed W0/V7 bands and C=[5,5], every W20-prefix-restoring emitter formed by at most four distinct-site ±9 edits on E/J is first-successor-equivalent to T14 and consumes eight V7 copies at t=160.

Exact exhaustive q=k=20 packet counts: sizes 1–4 have 25/299/2,277/12,397 candidates and 17/136/684/2,435 restorers; every restorer is T14-equivalent. The carry-reset cone lift applies to q,k>=20 for this bounded edit family only.

Reproduce: g++ -O3 -std=c++17 calculation/new_structures/Y36/exhaustive.cpp -o /tmp/y36-ledger && /tmp/y36-ledger; python3 calculation/new_structures/Y36/verify_ledger.py.

Not claimed: packets of five or more edits, arbitrary E/J changes, a global p8 lower bound, a moving/phase-changing repair, or a decimal Lychrel certificate.

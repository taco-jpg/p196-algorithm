# Finite join check against the orbit of 196

This was a follow-up attempt to reduce the unresolved original gate cases
to the specific 196 question by exact orbit coalescence. It found no join;
it proves neither infinite separation nor infinite palindrome avoidance.

The reference orbit contains indices 0 through 1500 starting from 196.
The tested gates are (u,v)=(1,6), r=1,2,3,4, and (1,7),
r=1,...,16,32,64,127 except r=3, which was already known to terminate.
Each of these 22 seeds was followed through 1500 ordinary integer additions.
No tested trajectory met any reference value, and none reached a palindrome
within that horizon. Every case, parameter, last value and trajectory hash
is retained in `joins_196.json`; the exact integer comparison source is
`check_196_joins.py` and its console record is `joins_196.log`.

Had an exact join been found, deterministic iteration would have reduced
the future palindrome question of that seed to a tail of the 196 orbit.
Without a join, no such reduction is established. Increasing this numerical
horizon alone would not establish an all-time theorem; this branch stops
at the recorded finite scope.

Reproduce from this directory with:

    python3 -B check_196_joins.py

No external solver or large-integer package is used. This experiment does
not change the all-parameter terminating-family theorem in `STATUS.md`.

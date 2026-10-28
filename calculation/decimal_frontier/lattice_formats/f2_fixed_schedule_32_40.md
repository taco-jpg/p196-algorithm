# Fixed period-10 schedule scan, bases 32--40

Status: COMPUTED.

The exact position automaton `code/bauto3.cpp` was run with state cap 3,000,000
for each base `b = 32,...,40` and each fixed overflow word
`1100011000`, `1010010000` (least-significant time first).  Every run finished
below the cap and had zero nontrivial SCCs, hence no periodic exterior lattice
for either fixed word in this scope.  The state counts for the first word are
`1,1,1,1,1,1,1,1,1`; for the second they are
`53,9,9,41,9,9,9,9,9`, in base order.

Reproduce (from this directory):
`c++ -O3 -std=c++17 code/bauto3.cpp -o /tmp/bauto3; for w in 1100011000 1010010000; do for b in $(seq 32 40); do /tmp/bauto3 $b 10 10 -g $w -cap 3000000 -maxscc 0; done; done`

Controls: base 9 / `1100011000` gave 956310 states and 7 nontrivial SCCs;
base 13 / `1010010000` gave 250302 states and 5 nontrivial SCCs.
This is only an exclusion for the two stated exterior schedules; it does not
claim a parametric theorem, a result for other periods, or anything about base 10.

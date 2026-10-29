# AC45 exploratory notes
- A local single-column carry ROBDD has 50 live nodes but this is not a 120-layer state bound. Naive extrapolation from it would be invalid.
- The 120-layer physical two-sided transducer must store upper-port state and the overflow-induced one-digit lag; a single forward carry chain is insufficient.
- Need a toy-clock planted return with a fully completed product before trusting an emptiness result.

# A complete decimal p29 / spatial-m7 reflected absorbing-bulk classification

**COMPUTED**, agent-712. Fix base b=10 and the genuinely primitive 29-step overflow word `g=00001110001000110001000110001`, with S=10. The domain is precisely the `19^4=130321` rows `(a,b,c,d,d,c,b)`, entries 0..18, invariant under reflection about spatial axis zero and spatial period dividing seven. This is a **bulk-only** statement: it neither assumes nor proves a path from the canonical finite exterior boundary.

## Finite map and why it covers all temporal superperiods

For a periodic row `r` of length seven, determine the lower and upper cyclic carries `A_i,D_i∈{0,1}` from `A_{i+1}=⌊(r_i+A_i)/10⌋` and `D_{i-1}=⌊(r_i+D_i)/10⌋` (cyclic indices). Except for the all-9 neutral row, each has a unique solution. Set `e_i=(r_i+A_i)%10`, `f_i=(r_i+D_i)%10`, and `Φ_γ(r)_i=e_i+f_{i-γ}`. Two independently derived implementations (one pivot-anchored, one exhaustive cyclic-carry fixed point) agree on every one of the `130321` iterates after 203 steps. The all-9 row is excluded from the absorbing map; it is the only initial row that encounters a neutral state during the 203-step test.

A single 29-step block moves the reflection axis by S=10 modulo seven. Since S≡3 and gcd(3,7)=1, a primitive spatial-m7 row can return to its original axis only after a multiple of seven 29-step blocks. Accordingly, the exhaustive `F=(Φ_g)^7` 203-step functional graph detects **every** periodic reflected primitive-m7 bulk, including all temporal superperiods. Uniform rows are reported separately.

## Complete recurrent functional graph

There are **11** cycles and **78** recurrent vertices: four uniform-m1 cycles of 1,1,2,6 vertices, and seven primitive-m7 cycles of 2,2,2,6,6,24,26 vertices (68 primitive-m7 vertices). No state or time search cap was applied. The following representatives are at reflection axis zero, and `T=203k` is the actual temporal cycle length. `P` is the smallest multiple of `T` divisible by six for the mod-9 test.

| Initial row (r0…r6) | k | T | P | Q (mod 9) |
|---|---:|---:|---:|---:|
| (2,2,2,1,1,2,2) | 2 | 406 | 1218 | 0 |
| (12,5,13,6,6,13,5) | 2 | 406 | 1218 | 0 |
| (14,15,13,7,7,13,15) | 2 | 406 | 1218 | 0 |
| (18,10,2,2,2,2,10) | 6 | 1218 | 1218 | 6 |
| (16,13,7,6,6,7,13) | 6 | 1218 | 1218 | 3 |
| (2,8,8,1,1,8,8) | 24 | 4872 | 4872 | 0 |
| (4,11,10,1,1,10,11) | 26 | 5278 | 15834 | 0 |

For every cycle, independent Python replays all `T` ordinary integer carry updates, confirms closure, independently reconstructs the complete graph from the map, and checks the spatially conserved charge `Q=Σ_t 2^{-t}(L_t-H_t+g_tY_t) mod 9` at every cut over the listed full period `P`. Two primitive-m7 cycles have nonzero charges, excluding a canonical-root connection at those full time rings and repetitions by factors not divisible by 3; **this does not exclude arbitrary temporal multiples**. Five other cycles have charge zero, a necessary condition only. Literal Python big integers additionally normalize 701-digit mirrored-coefficient pairwords and compare 500 interior coefficients for 71 recurrent axis-zero row states; this is a one-step bulk check, **not** a 20,000-step decimal certificate.

## Reproduction and limits

`bash calculation/decimal_frontier/lattice_formats/code/agent712_p29_m7_reproduce.sh` builds the local C++ engine and a separate published full-position-automaton control. The controls reproduce base9 `g=1100011000`: 956310 states, seven nontrivial SCCs including primitive spatial-m4 depth61; base13 `g=1010010000`: 250302 states, five nontrivial SCCs, singleton depths55 and75. The engine uses one `nice -n 19` process with an 8-GB address-space limit; the temporary complete 130321-entry transition map is independently audited by the Python checker and deleted. The exhaustive computation does not truncate the finite graph.

No rooted exterior reachability, global decimal center, actual infinite reverse-and-add trajectory, Lean proof or assertion about 196 is derived. The mod-9 charges do not establish reachability when zero. The result is an exact classification of the stated reflected spatial period only, not of all spatial periods or overflow words.

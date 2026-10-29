# AC19 target

Rooted base-10 p12/m9 clock phase 10, B10 and W10 from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, q=14, k>=100, J arbitrary over coefficients 0..18 of length 3 or 4, U any of 30 rotations of (9,a,18-a) with even a=0..18, C any valid palindromic coefficient centre (both parities).

For H=B10++W10^14++J++U^k and P=H++C++reverse(H), prove that 120 actual decimal reverse-and-add steps cannot produce the *same* B10/W10/J/U/C template with k increased by 5. It suffices to prove the endpoint W9 prefix cannot be preserved. Intermediates may damage or heal W9. Scope: no assertion for J>=5, other phases, moving junctions or q-changing edges.
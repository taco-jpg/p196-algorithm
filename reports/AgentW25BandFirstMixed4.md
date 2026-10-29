# W25: band-first nonuniform period-4 bulk embedded beside rooted period-20 decimal exterior

**COMPUTED.** Pair coefficients are `P_i=d_i+d_{n-1-i}`, least significant first, values 0..18.

The previous p8 rooted exterior B39/W20 has overflow schedule `10101010`. Instead of selecting an interior centre first, solve the cyclic bulk equations for an *independent* periodic spatial band w of any length m. Let c and h be cyclic lower-side and upper-side carries, satisfying
`c_(i+1)=floor((w_i+c_i)/10)` and `h_i=floor((w_i+h_(i+1))/10)`.
Let `L_i=(w_i+c_i)%10` and `H_i=(w_i+h_(i+1))%10`. The exact bulk successor for overflow gamma=0 or 1 is
`w'_i=L_i+H_(i-gamma mod m)`.
For any word containing a coefficient other than 9 the two cyclic carry solutions are unique. This follows because the one-period carry map is constant unless all coefficients equal 9. A sufficiently deep spatial site therefore obeys this map exactly, but that alone says nothing about the finite exterior and centre.

The newly selected base-10 bulk starts `U=[9,18,9,0]`. For gamma `10101010`, successive rows are
`[9,18,9,0]`,
`[10,8,8,10]`,
`[1,17,17,1]`,
`[2,9,16,9]`,
`[6,9,12,9]`,
`[16,16,2,2]`,
`[13,13,5,5]`,
`[9,8,9,10]`, returning to the start on step 8.
This is a real *bulk cycle*, not a rooted whole-number certificate. The existing base-9 `[1,1,15,15]` maps to `[8,2,8,14]` for gamma=1, independently cross-checking orientation.

Set Q=B39 ++ W20^k ++ U4^r and P=Q++reverse(Q). Ordinary decimal digits are formed by placing `min(P_i,9)` at the low position and `P_i-min(P_i,9)` at the mirrored high position. For k=500,r=9000 the ordinary starting number has 92078 digits. All 20000 ordinary decimal reverse/add operations are independently checked by a second coefficient-normalization implementation. Each of the 20001 numbers is tested against reversal for palindromicity. The observed gamma schedule is 10101010 for all 20000 edges. An 80-coefficient window at spatial indices 5039..5118 follows the m20 temporal bulk; another at 28039..28118 follows the m4 temporal bulk for all 20001 states. Final length 102078; final LSB-numeric-digit FNV64 3f6aaae5052be7bc.

For a smaller seed k=150,r=500, an independent Python arbitrary-integer engine (1000 steps) agrees with the decimal list engine's final 10578-digit length and FNV64 02e3b04ac35eb421. The larger engine additionally agrees with GNU GMP through the first 20 steps. A comparison k=500,r=4000 with the m4 window at the band midpoint gives first m4-window failure at step 10671; the same rooted m20 window still survives 20000. Increasing the physical separation to r=9000 postpones both tested window failures beyond 20000. These are not monotone all-time assertions.

**Missing closure:** the m20/m4 junction and the central seam are *not* part of any verified finite cycle, and the m4 band is not asserted to remain nonempty indefinitely. In particular, a period-8 cyclic bulk cannot be substituted for an exact rooted exterior/centre certificate. Next constructive target: solve an eight-step finite carry-interface return relation between these two different spatial periods, rather than scanning additional short fixed centres.

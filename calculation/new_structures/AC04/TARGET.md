# AC04 exact target

Fix phase-0 p12/m9 B34,W9, J=[5] and U=(9,6,12),(6,12,9), or (12,9,6), LSD-first. Define H=B++W^q++J++U^k, P=H++C++reverse(H), where C is palindromic and an odd midpoint is even.

The missing all-time lemma would be a physical 120-step return P(q,k)->P(q,k+5), with identical seam and centre, both carries and 120-bit overflow/nonpalindrome guard, uniformly for all sufficiently large q,k. AC04 instead tests the NECESSARY centre-collar return at q=14,k=100 and a sound upper approximation of all completions of fixed outer C coefficients. Strict-per-phase W9 preservation is NOT required. This does not supply an all-time certificate.
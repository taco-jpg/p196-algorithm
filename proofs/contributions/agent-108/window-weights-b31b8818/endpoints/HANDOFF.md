# Agent 108 endpoint theorem handoff

## Scope and ownership

These two owned modules supply the exact endpoint bookkeeping needed by the already claimed fixed-window incoming-weight obstruction. They do not assert the complete incoming-weight theorem; the parent owns global buffered-family factorization and integration.

- `Agent108WindowEndpoints.lean`: SHA256 `ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22`.
- `Agent108WindowEndpointWeights.lean`: SHA256 `21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1`.

The namespace is `Agent108.WindowWeights`. Write a^n for a repeated n times, and ++ for list concatenation. Complete windows have width b+1, where b is any natural number, and no padding is added.

## Exact endpoint list

The parent definition is endpoint b k a = 9^b ++ [a] ++ 18^k. For every natural b, k, a, the theorem `endpoint_windows` states:

    windows (b+1) (endpoint b k a)
      = map (j in range (min k b + 1)) (9^(b-j) ++ [a] ++ 18^j)
        ++ replicate (k-b) (18^(b+1)).

`endpoint_window_cross` proves the individual windows for j <= b and j <= k. `endpoint_window_tail` proves the common all-eighteen tail when b < j <= k.

There is no hypothesis k >= b. For k=0 there is exactly one complete window, 9^b ++ [a]. For b=0 the first factor is [a] and there are k subsequent singleton [18] windows. These are instances of the same universal theorem.

## Real products and exact constant

The parent definitions are:

    windowProduct b psi w = product of psi over windows (b+1) w
    PositivePotential b psi = every list of length b+1 with entries <= 18 has positive psi

No positivity is required on lists of any other length or on lists containing coefficients greater than 18.

`endpoint_product` is an unconditional real product identity for every a and every psi. It factors the endpoint product into the product over j=0,...,min(k,b), followed by psi(18^(b+1))^(k-b).

The noncomputable definition `endpointRatio b k psi` is

    product over j=0,...,min(k,b) of
      psi(9^(b-j) ++ [14] ++ 18^j) /
      psi(9^(b-j) ++ [9]  ++ 18^j).

The theorem `endpoint_ratio` identifies this with windowProduct(endpoint 14) / windowProduct(endpoint 9). Its proof cancels the common positive all-eighteen factor, including when its exponent is zero. The theorem `endpoint_ratio_pos` proves strict positivity under PositivePotential.

The noncomputable definition `endpointConstant b k psi` is

    psi([5] ++ 9^b) / psi([11] ++ 9^b) * endpointRatio b k psi.

`endpoint_constant_formula` identifies this with the exact first-window correction multiplied by the exact endpoint product ratio. `endpoint_constant_pos` proves it is strictly positive. It has no r parameter, so it is available unchanged as the number of interior blocks varies. Width-only factors are not part of this definition; their cancellation belongs to the parent's same-width integration theorem.

Supporting positivity interfaces are `endpoint_cross_potential_pos`, `endpoint_eighteen_potential_pos`, `endpoint_first_potential_pos`, and `endpoint_first_ratio_pos`.

## Verification and retained failures

Both modules were compiled with pinned Lean 4.19.0, --trust=0, -j1, and -DElab.async=false using authorized require_escalated execution. The real module used the restored Mathlib wrapper. The three public list theorems have only propext and Quot.sound as transitive axioms; all nine public real theorems have only propext, Classical.choice, and Quot.sound. Exact commands, dependency hashes, snapshots, and complete axiom outputs are preserved in the JSON/log files in this directory. These are self-executed checks, separate from independent review.

The first real attempt elaborated all proofs but failed code generation for the two definitions involving real division. The second attempt only added noncomputable to those definitions and passed. Both source attempts and logs are retained. Earlier substantive list proof attempts and the parent overlap dependency failure log are also retained.

The dependency used for the real pass is the exact parent snapshot `weight-defs-attempt02.lean`, copied into `deps/Agent108WindowWeights.lean`. The parent may add further API lemmas before the final combined build; that final dependency build should be performed from the final source set. This note does not claim that later parent edits have already been rechecked.

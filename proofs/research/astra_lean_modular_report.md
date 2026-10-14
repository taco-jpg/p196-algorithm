# Verified modular dynamics for ordinary decimal reverse-and-add

`astra_lean_modular.lean` contains 25 additional theorems in 316 lines. It
imports the authoritative `Lychrel196Research` module and does not edit it.
All statements use that module's actual finite-natural-number reversal,
reverse-and-add map, orbit, and canonical decimal representation.

The strongest new formalized statement is:

```lean
theorem DecimalModular.orbit_mod11_eq_zero_of_six_le
    (n k : Nat) (hn : 0 < n) (hk : 6 ≤ k) :
    Lychrel196.orbit n k % 11 = 0
```

The time bound is sharp. `six_step_bound_sharp` proves by kernel evaluation
that seed 100 has no multiple of 11 at times 0 through 5, and reaches one
at time 6. Its initial orbit is

    100, 101, 202, 404, 808, 1616, 7777.

The general proof first establishes the exact modulo-99 formula: reversal
multiplies the residue by 10 at even input width and by 1 at odd input
width. A reverse-and-add step therefore multiplies it by 11 or 2,
respectively. The same formulas hold modulo every divisor of 99. In
particular, even-width input produces a multiple of 11 and divisibility by
11 persists thereafter. The archived unconditional width bound forces
width to increase by time 5. Width can increase only by one at a step, so
an even width occurs by that time. The next iterate, at latest time 6,
is divisible by 11.

Other verified statements include:

- `reverse10_mod99`, `step_mod99`, and the corresponding
  `*_mod_of_dvd99` theorems: exact arithmetic residue recurrences.
- `no_consecutive_zero_units`: two consecutive positive orbit states
  cannot both be divisible by 10.
- `large_width_compatible_residue`: for every fixed modulus M, target
  width B, and positive seed, there is an actual orbit state at a time
  j between 6+4B and 7+4B inclusive, with canonical width W at least B,
  whose residue a modulo M satisfies both compatibility conditions
  used by the exact-length palindrome-saturation paper:
  not both 10 divides M and 10 divides a, and at even W, gcd(M,11)
  divides a.
- `even_width_palindromic_overflow_dvd121`: if an actual addition from
  even canonical width overflows and produces a palindrome, its output
  is divisible by 121. Its contrapositive is also formalized.

The last theorem uses the existing exact palindrome-overflow criterion:
the symmetric input pair-sum word has all coefficients in {0,11}.
Dividing its coefficients by 11 leaves a symmetric even-width word,
whose value is independently proved divisible by 11. This supplies the
second factor. It is a local necessary condition, not a proof of its
preservation across an infinite orbit.

## Verification and scope

Run from the `research` directory:

```sh
LEAN_PATH=. ../lean-runtime/lean -o astra_lean_modular.olean astra_lean_modular.lean
LEAN_PATH=. ../lean-runtime/lean astra_lean_modular_audit.lean
```

Both commands succeeded under Lean 4.19.0 with Std only. The audit file
prints axioms for every one of the 25 new theorems. Its complete output is
`astra_lean_modular_axioms.txt`. Only the standard logical axioms
`propext`, `Classical.choice`, and `Quot.sound` appear. There are no
unproved terms, custom axioms, or native computation proof shortcuts.

The full arbitrary-modulus exact-length palindrome residue saturation
theorem has **not** been formalized here. Nor has the necessity direction
of the complete modulus-classification theorem. These results establish
all the stated dynamic arithmetic prerequisites, the sufficient modulus
class, and the even-width 121 obstruction. They do not prove the existence
of a decimal Lychrel number or prove that 196 avoids palindromes forever.

import ResidualFiveFilteredConclusion

set_option autoImplicit false

/-!
The complete residual-five fiber is specialized to the original, already proved
modulo-99 transport law. Equality below is equality of residues for all times;
it does not identify the underlying integer trajectories.
-/
namespace Agent103.ResidualFivePhaseCompatibility

open Lychrel196 Agent103.ResidualFiveFibers Agent423.TemporalResidues

/-- Every member of the exact modular fiber is in the original divisible-by-11
class, so the existing width-independent temporal law applies from time zero. -/
theorem modular_fiber_dvd11 (r n : Nat) (hn : n ∈ modularFiber r) : 11 ∣ n := by
  have hm := ((mem_modularFiber_iff r n).mp hn).2
  apply Nat.dvd_of_mod_eq_zero
  omega

/-- The full future residue trajectory agrees with the original 196 orbit
starting at its proved phase seven. This is not integer-orbit reachability. -/
theorem modular_fiber_mod99_trace (r n : Nat) (hn : n ∈ modularFiber r) (i : Nat) :
    orbit n i % 99 = orbit 196 (7 + i) % 99 := by
  have hn99 := ((mem_modularFiber_iff r n).mp hn).2
  have h196 : orbit 196 7 % 99 = 77 := by
    simpa [phase196] using orbit196_mod99_table 1
  have hd196 : 11 ∣ orbit 196 7 := by
    apply Nat.dvd_of_mod_eq_zero
    omega
  rw [LychrelCertificates.orbit_add]
  rw [orbit_mod99_pow_of_dvd11 n i (modular_fiber_dvd11 r n hn),
    orbit_mod99_pow_of_dvd11 (orbit 196 7) i hd196]
  calc
    (2 ^ i * n) % 99 = (2 ^ i % 99 * (n % 99)) % 99 := Nat.mul_mod _ _ _
    _ = (2 ^ i % 99 * (orbit 196 7 % 99)) % 99 := by rw [hn99, h196]
    _ = (2 ^ i * orbit 196 7) % 99 := (Nat.mul_mod _ _ _).symm

#print axioms modular_fiber_dvd11
#print axioms modular_fiber_mod99_trace

end Agent103.ResidualFivePhaseCompatibility

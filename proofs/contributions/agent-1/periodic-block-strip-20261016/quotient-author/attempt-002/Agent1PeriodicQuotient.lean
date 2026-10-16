import Agent1PeriodicGuardFacts

/-!
Exact whole-period absorption for the spatial quotient. The period word,
normalizer and actual pair map are the original definitions. This module
asserts neither safety preservation nor a return cycle.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Absorb complete exterior periods and mirrored center periods into the
two repeated bands. All exponents are natural numbers, including zero. -/
theorem periodicWord_absorb (B H w : Word) (u v k : Nat) :
    periodicWord (B ++ pow w u)
      (pow w v ++ H ++ pow w.reverse v) w k =
    periodicWord B H w (k + u + v) := by
  have hl : pow w u ++ pow w k ++ pow w v = pow w (k+u+v) := by
    rw [← pow_append, ← pow_append, Nat.add_comm u k]
  have hr : pow w.reverse v ++ pow w.reverse k ++ pow w.reverse u =
      pow w.reverse (k+u+v) := by
    rw [← pow_append, ← pow_append]
    congr 1
    omega
  simp only [periodicWord, List.reverse_append, pow_reverse]
  simp only [List.append_assoc] at hl hr ⊢
  rw [← hl, ← hr]
  simp only [List.append_assoc]

/-- Exact length, including zero exponents and noncanonical coefficient lists. -/
theorem periodicWord_length (B H w : Word) (k : Nat) :
    (periodicWord B H w k).length = 2*B.length + H.length + 2*(k*w.length) := by
  simp only [periodicWord, List.length_append, List.length_reverse, pow_length]
  omega

/-- Compose any exact whole-block decompositions with the checked raw guard.
The executable maximal algorithms below will supply these equalities. -/
theorem raw_guard_of_stripped (B H w B' H' : Word) (u v k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hk : 3 ≤ k)
    (ho : rawOuter B H w = B' ++ pow (rawPeriod B H w) u)
    (hc : rawCenter B H w =
      pow (rawPeriod B H w) v ++ H' ++ pow (rawPeriod B H w).reverse v) :
    stepWord (periodicWord B H w k) =
      periodicWord B' H' (rawPeriod B H w) ((k-2)+u+v) := by
  rw [raw_guard_bounded B H w k hB hH hw hlen hk, ho, hc]
  exact periodicWord_absorb B' H' (rawPeriod B H w) u v (k-2)

/-- The signed exponent increment agrees exactly with finite word widths.
All length casts are explicit, so a negative increment is never truncated. -/
theorem stripped_width_balance (B H w B' H' : Word) (u v : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4)
    (ho : rawOuter B H w = B' ++ pow (rawPeriod B H w) u)
    (hc : rawCenter B H w =
      pow (rawPeriod B H w) v ++ H' ++ pow (rawPeriod B H w).reverse v) :
    2*(B'.length : Int) + (H'.length : Int) + 8*((u : Int)+(v : Int)-2) =
      2*(B.length : Int) + (H.length : Int) + (rawGamma B H w : Int) := by
  obtain ⟨hbo, hwp, hhc⟩ := raw_block_lengths B H w hB hH hw hlen
  have hb := congrArg List.length ho
  have hh := congrArg List.length hc
  simp only [List.length_append, pow_length, List.length_reverse, hwp] at hb hh
  rw [hbo] at hb
  rw [hhc] at hh
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_absorb
#print axioms Agent1.Periodic.periodicWord_length
#print axioms Agent1.Periodic.raw_guard_of_stripped
#print axioms Agent1.Periodic.stripped_width_balance

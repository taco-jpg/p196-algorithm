import Agent113TripleCycles

/-!
# Agent #113: arbitrary-depth extension of the certified abstract inverse cycle

This theorem concerns only the exact THREE-COLUMN overapproximation of
reverse-add and proves that the finite predecessor certificate layers for the
32 complementary descending prefixes never empty at subsequent depths.
It does NOT construct any ordinary integer with infinite palindrome avoidance.
-/

namespace Agent113.TripleMaximality

private def localState (s : InvStep) : Triple := (s.s0, s.s1, s.s2)

/-- One chosen abstract inverse predecessor of each of the four cycle states. -/
private def chooseBack (t : Triple) : InvStep :=
  if t = (1, 5, 10) then ⟨10, 4, 6, 0⟩
  else if t = (10, 4, 6) then ⟨5, 2, 3, 0⟩
  else if t = (5, 2, 3) then ⟨2, 11, 1, 0⟩
  else ⟨1, 5, 10, 1⟩

private theorem chooseBack_one_step (t : Triple) (ht : ValidChain t []) :
    ValidChain t [chooseBack t] := by
  change t ∈ [(1,5,10), (10,4,6), (5,2,3), (2,11,1)] at ht
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at ht
  rcases ht with rfl | rfl | rfl | rfl <;> decide +kernel

/-- Append any number of abstract cycle-inverse steps from cycle state t. -/
private def cycleAppend : Triple → Nat → List InvStep
  | _, 0 => []
  | t, k + 1 => chooseBack t :: cycleAppend (localState (chooseBack t)) k

private theorem cycleAppend_length : ∀ k (t : Triple), (cycleAppend t k).length = k := by
  intro k
  induction k with
  | zero => intro t; rfl
  | succ k ih =>
      intro t
      simp only [cycleAppend, List.length_cons]
      rw [ih (localState (chooseBack t))]

/-- The finite cycle yields a valid symbolic predecessor chain of every length. -/
theorem cycle_unbounded : ∀ k (t : Triple), ValidChain t [] →
    ValidChain t (cycleAppend t k) := by
  intro k
  induction k with
  | zero =>
      intro t ht
      simpa [cycleAppend] using ht
  | succ k ih =>
      intro t ht
      have one := chooseBack_one_step t ht
      change 1 ≤ (chooseBack t).s0 ∧ (chooseBack t).s0 ≤ 18 ∧
        (chooseBack t).s1 ≤ 18 ∧ (chooseBack t).s2 ≤ 18 ∧
        (chooseBack t).e ≤ 1 ∧
        Agent113.TwoDigit.nextTriple (chooseBack t).s0 (chooseBack t).s1
          (chooseBack t).s2 (chooseBack t).e = t ∧
        ValidChain (localState (chooseBack t)) [] at one
      rcases one with ⟨h0, h01, h1, h2, he, hn, hc⟩
      change 1 ≤ (chooseBack t).s0 ∧ (chooseBack t).s0 ≤ 18 ∧
        (chooseBack t).s1 ≤ 18 ∧ (chooseBack t).s2 ≤ 18 ∧
        (chooseBack t).e ≤ 1 ∧
        Agent113.TwoDigit.nextTriple (chooseBack t).s0 (chooseBack t).s1
          (chooseBack t).s2 (chooseBack t).e = t ∧
        ValidChain (localState (chooseBack t))
          (cycleAppend (localState (chooseBack t)) k)
      exact ⟨h0, h01, h1, h2, he, hn,
        ih (localState (chooseBack t)) hc⟩

/-- A checked finite predecessor chain can be extended by an arbitrary
number of edges, retaining the exact initial target. -/
theorem extend_chain : ∀ (t : Triple) (steps : List InvStep) (k : Nat),
    ValidChain t steps →
    ∃ tail : List InvStep,
      tail.length = k ∧ ValidChain t (steps ++ tail) := by
  intro t steps
  induction steps generalizing t with
  | nil =>
      intro k ht
      refine ⟨cycleAppend t k, cycleAppend_length k t, ?_⟩
      simpa using cycle_unbounded k t ht
  | cons s rest ih =>
      intro k ht
      change 1 ≤ s.s0 ∧ s.s0 ≤ 18 ∧ s.s1 ≤ 18 ∧ s.s2 ≤ 18 ∧
        s.e ≤ 1 ∧ Agent113.TwoDigit.nextTriple s.s0 s.s1 s.s2 s.e = t ∧
        ValidChain (localState s) rest at ht
      rcases ht with ⟨h0, h01, h1, h2, he, hn, hr⟩
      obtain ⟨tail, hlen, hgood⟩ := ih (localState s) k hr
      refine ⟨tail, hlen, ?_⟩
      change 1 ≤ s.s0 ∧ s.s0 ≤ 18 ∧ s.s1 ≤ 18 ∧ s.s2 ≤ 18 ∧
        s.e ≤ 1 ∧ Agent113.TwoDigit.nextTriple s.s0 s.s1 s.s2 s.e = t ∧
        ValidChain (localState s) (rest ++ tail)
      exact ⟨h0, h01, h1, h2, he, hn, hgood⟩

/-- Extending does not destroy the crucial restricted no-overflow FIRST edge. -/
theorem extend_first (a b c : Nat) (steps : List InvStep) (k : Nat)
    (h : ValidFirst a b c steps) :
    ∃ extended : List InvStep,
      extended.length = steps.length + k ∧ ValidFirst a b c extended := by
  cases steps with
  | nil =>
      change False at h
      exact False.elim h
  | cons s rest =>
      change Agent113.TwoDigit.topCarry s.s0 s.s1 s.s2 s.e = 0 ∧
        ValidChain (a,b,c) (s :: rest) at h
      rcases h with ⟨htop, hpath⟩
      obtain ⟨tail, hlen, hgood⟩ := extend_chain (a,b,c) (s :: rest) k hpath
      refine ⟨(s :: rest) ++ tail, ?_, ?_⟩
      · simp only [List.length_append, List.length_cons, hlen]
        omega
      · change Agent113.TwoDigit.topCarry s.s0 s.s1 s.s2 s.e = 0 ∧
          ValidChain (a,b,c) ((s :: rest) ++ tail)
        exact ⟨htop, hgood⟩

/-- MAIN: every complementary descending two-digit prefix has first-edge-
restricted symbolic predecessors of arbitrarily large exact depths. This is
an inability of THIS finite three-column abstraction to empty its layers,
NOT an assertion of an actual infinitely iterable integer predecessor. -/
theorem all_32_unbounded_inverse_layers :
    ∀ ab ∈ remaining32,
      ∃ c : Nat, c ≤ 9 ∧ ∃ base : List InvStep,
        ValidFirst ab.1 ab.2 c base ∧
        ∀ extra : Nat, ∃ path : List InvStep,
          path.length = base.length + extra ∧
          ValidFirst ab.1 ab.2 c path := by
  intro ab hab
  obtain ⟨c, hc, base, hbase⟩ := remaining32_path_exists ab hab
  exact ⟨c, hc, base, hbase,
    fun k => extend_first ab.1 ab.2 c base k hbase⟩

#print axioms cycle_unbounded
#print axioms extend_chain
#print axioms extend_first
#print axioms all_32_unbounded_inverse_layers

end Agent113.TripleMaximality

import Init.Data.List.Erase

set_option autoImplicit false

/-!
# Parity of a finite involution

Agent #6: a duplicate-free finite list preserved by an involution has the
same cardinality parity as its fixed-point sublist. The proof removes
either one fixed point or a pair of distinct partners. Only core Lean
list lemmas are used; no arithmetic dynamics is assumed in this module.
-/

namespace ZeroEndingPredecessorParity

/-- Nonfixed members of a finite involution occur in distinct pairs.
Consequently the list and its fixed-point sublist have the same parity. -/
theorem involution_fixed_filter_parity (l : List Nat) (f : Nat → Nat)
    (hnd : l.Nodup)
    (hmap : ∀ x, x ∈ l → f x ∈ l)
    (hinv : ∀ x, x ∈ l → f (f x) = x) :
    l.length % 2 = (l.filter (fun x => decide (f x = x))).length % 2 := by
  have aux : ∀ N : Nat, ∀ xs : List Nat, xs.length = N →
      xs.Nodup →
      (∀ x, x ∈ xs → f x ∈ xs) →
      (∀ x, x ∈ xs → f (f x) = x) →
      xs.length % 2 = (xs.filter (fun x => decide (f x = x))).length % 2 := by
    intro N
    induction N using Nat.strongRecOn with
    | ind N ih =>
        intro xs hlen hnodup hclosed htwice
        cases xs with
        | nil => simp
        | cons a xs =>
            have htail := List.nodup_cons.mp hnodup
            have hlen' : xs.length + 1 = N := by simpa using hlen
            have ha : a ∈ a :: xs := List.mem_cons_self
            have hfa := hclosed a ha
            have hffa := htwice a ha
            by_cases hfixed : f a = a
            · have htailclosed : ∀ x, x ∈ xs → f x ∈ xs := by
                intro x hx
                have hxall : x ∈ a :: xs := List.mem_cons_of_mem a hx
                have hfx := hclosed x hxall
                rcases List.mem_cons.mp hfx with heq | hmem
                · have hxfix := htwice x hxall
                  rw [heq, hfixed] at hxfix
                  exact False.elim (htail.1 (hxfix ▸ hx))
                · exact hmem
              have htailinv : ∀ x, x ∈ xs → f (f x) = x :=
                fun x hx => htwice x (List.mem_cons_of_mem a hx)
              have hr := ih xs.length (by omega) xs rfl htail.2 htailclosed htailinv
              simp [hfixed]
              omega
            · have hpartner : f a ∈ xs := (List.mem_cons.mp hfa).resolve_left hfixed
              have hpartnerNotFixed : f (f a) ≠ f a := by
                rw [hffa]
                exact Ne.symm hfixed
              have hrestnd : (xs.erase (f a)).Nodup := List.Nodup.erase (f a) htail.2
              have hrestclosed : ∀ x, x ∈ xs.erase (f a) → f x ∈ xs.erase (f a) := by
                intro x hx
                have hxdata := (List.Nodup.mem_erase_iff htail.2).mp hx
                have hxall : x ∈ a :: xs := List.mem_cons_of_mem a hxdata.2
                have hxx := htwice x hxall
                have hfxne : f x ≠ a := by
                  intro heq
                  rw [heq] at hxx
                  exact hxdata.1 hxx.symm
                have hfxtail : f x ∈ xs :=
                  (List.mem_cons.mp (hclosed x hxall)).resolve_left hfxne
                have hfxpartner : f x ≠ f a := by
                  intro heq
                  rw [heq, hffa] at hxx
                  exact htail.1 (hxx ▸ hxdata.2)
                exact (List.Nodup.mem_erase_iff htail.2).mpr ⟨hfxpartner, hfxtail⟩
              have hrestinv : ∀ x, x ∈ xs.erase (f a) → f (f x) = x := by
                intro x hx
                exact htwice x (List.mem_cons_of_mem a (List.mem_of_mem_erase hx))
              have heraselen := List.length_erase_of_mem hpartner
              have hrestlt : (xs.erase (f a)).length < N := by
                have hle := List.length_erase_le (a := f a) (l := xs)
                omega
              have hr := ih (xs.erase (f a)).length hrestlt (xs.erase (f a)) rfl
                hrestnd hrestclosed hrestinv
              have hfilter : (xs.erase (f a)).filter (fun x => decide (f x = x)) =
                  xs.filter (fun x => decide (f x = x)) := by
                rw [← List.erase_filter]
                apply List.erase_of_not_mem
                simp only [List.mem_filter, decide_eq_true_eq]
                intro h
                exact hpartnerNotFixed h.2
              rw [hfilter] at hr
              have hxspos : 0 < xs.length :=
                List.length_pos_iff_exists_mem.mpr ⟨f a, hpartner⟩
              simp [hfixed]
              omega
  exact aux l.length l rfl hnd hmap hinv

end ZeroEndingPredecessorParity

#print axioms ZeroEndingPredecessorParity.involution_fixed_filter_parity

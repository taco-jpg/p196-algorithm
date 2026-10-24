import P196.Sprint.Agent02.W3Check
import P196.Agent124ForwardInvariant.A124W3Final

/-!
# The width-3 forward invariant is optimal, start-time independent, and it is exactly where
# the backward rank method stops (sprint agent 02)

`Agent124.FwdW3.fset` is the forward closure (4,194 words) of the 3-column projection of
`orbit 196 100` under both carry choices of `forwardPrefix`; the 277 digit prefixes outside it are
excluded from the 196 orbit by `Agent124.FwdW3.no_196_excluded`. Here:

* `fset_connected`: `fset` is strongly connected — every predicate closed under both carries that
  holds at one word of `fset` holds at every word of `fset`;
* `forward_optimal`: every forward-closed code-keyed set containing the 3-column projection of
  the 196 orbit at *any* time `100 + s` contains all of `fset`; so restarting the forward
  invariant later, or choosing another closed set, cannot exclude a further 3-digit word;
* `no_rank_on_fset`: no partial rank function closed under the complete long inverse at width 3
  (`Agent124.PrefixR.RowsClosed 3`) ranks any word of `fset`;
* `entryOK_false` / `limit_words`: for each of the 620 three-digit digit words in `fset`
  (`limitWords`), every width-3 entry check of the Agent #124 batch interface fails, whatever
  the bound.

Together: at width 3 the forward method and the backward rank method exclude exactly the same
three-digit words, and neither can do better at this width. These are method limits, not
statements about which palindromes occur in the 196 orbit.
-/

namespace Sprint.Agent02.W3

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn SevenColumn.Certificate Agent124.PrefixK Agent124.PrefixR Agent124.PrefixL
open Agent124.CodeCert Agent124.Forward Agent124.FwdW3 Sprint.Agent02

theorem from_of_fset {c : Nat} (hc : (lookupC fset c).isSome = true) :
    ∃ v, lookupC fromT c = some v := by
  obtain ⟨r, hr⟩ := Option.isSome_iff_exists.mp hc
  exact Option.isSome_iff_exists.mp (lookupC_all (keysIn_sound fset_in_fromT) hr)

theorem to_of_fset {c : Nat} (hc : (lookupC fset c).isSome = true) :
    ∃ v, lookupC toT c = some v := by
  obtain ⟨r, hr⟩ := Option.isSome_iff_exists.mp hc
  exact Option.isSome_iff_exists.mp (lookupC_all (keysIn_sound fset_in_toT) hr)

/-- `fset` is strongly connected under the two carry choices. -/
theorem fset_connected {P : List Nat → Prop} (hP : ClosedK 3 P) {c₁ c₂ : Nat}
    (h₁ : (lookupC fset c₁).isSome = true) (h₂ : (lookupC fset c₂).isSome = true)
    (hc : P (decode c₁)) : P (decode c₂) := by
  obtain ⟨v₁, hv₁⟩ := to_of_fset h₁
  obtain ⟨v₂, hv₂⟩ := from_of_fset h₂
  exact reach_from fromT_ok hP (reach_to toT_ok hP c₁ v₁ hv₁ hc) c₂ v₂ hv₂

/-- Every forward-closed code-keyed set that contains the 3-column projection of the 196 orbit
at some time `100 + s` contains every word of `fset`. -/
theorem forward_optimal (t : CodeTree) (ht : t.All (fun c _ => fwdOK t 3 c = true)) (s : Nat)
    (hs : Mem t (wordPrefix (iterPairs q100 47 s).2 3)) :
    ∀ c, (lookupC fset c).isSome = true → Mem t (decode c) := by
  intro c hc
  have hadm : Admissible 47 q100 := canonical_admissible N100 d100 47 canonical100
  have hinv : Mem fset (wordPrefix (iterPairs q100 47 s).2 3) :=
    invariant (by decide) (by decide) closed q100 47 hadm (by decide) init s
  have hv := iterPairs_admissible q100 47 s hadm
  have hkL : 3 ≤ (iterPairs q100 47 s).1 :=
    Nat.le_trans (by decide) (iterPairs_width_ge q100 47 s)
  have hb := wordPrefix_lt19 _ _ 3 hv hkL
  have hdec : decode (wordCode (wordPrefix (iterPairs q100 47 s).2 3)) =
      wordPrefix (iterPairs q100 47 s).2 3 :=
    decode_wordCode _ hb (by simp)
  have hP : ClosedK 3 (Mem t) := fun u hu hlen hub e he =>
    mem_forward (by decide) ht hub hlen hu (by omega)
  have h1 : Mem t (decode (wordCode (wordPrefix (iterPairs q100 47 s).2 3))) := by
    rw [hdec]; exact hs
  exact fset_connected hP hinv hc h1

/-- No rank function closed under the complete long inverse at width 3 ranks a word of `fset`. -/
theorem no_rank_on_fset (Rk : List Nat → Option Nat) (rows : RowsClosed 3 Rk) :
    ∀ c, (lookupC fset c).isSome = true → Rk (decode c) = none := by
  intro c hc
  obtain ⟨v, hv⟩ := from_of_fset hc
  have hW0 : (decode W0).length = 3 ∧ ∀ a ∈ decode W0, a < 19 := by
    rw [W0_word]; decide
  exact no_rank_of_from fromT_ok U0_in_fromT U0_edge hW0 Rk rows c v hv

theorem initialWordsL_self {k : Nat} {w : List Nat} (hw : w.length = k) :
    initialWordsL k w = [w] := by
  unfold initialWordsL
  have h1 : k + 1 - w.length = 1 := by omega
  have hr : List.range 1 = [0] := rfl
  have hi : initialOK k w = true := by simp [initialOK, hw]
  rw [h1, hr]
  simp [digitLists, hi]

/-- The Agent #124 entry check fails at width 3 for every word of `fset`, whatever the bound. -/
theorem entryOK_false (Rk : List Nat → Option Nat) (rows : RowsClosed 3 Rk)
    (c : Nat) (hc : (lookupC fset c).isSome = true) (b : Nat) :
    entryOK 3 Rk (decode c, b) = false := by
  obtain ⟨v, hv⟩ := from_of_fset hc
  have hok := lookupC_all fromT_ok hv
  unfold fromOK at hok
  simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq] at hok
  have hlen : (decode c).length = 3 := hok.1.1
  have hnone := no_rank_on_fset Rk rows c hc
  simp [entryOK, initialWordsL_self hlen, hnone]

/-- The three-digit digit words (leading digit at least 1) that lie in `fset`. -/
def limitWords : List (List Nat) :=
  (digitLists 3).filter (fun w => Nat.blt 0 (w.headD 0) && (lookupC fset (wordCode w)).isSome)

set_option maxHeartbeats 0 in
theorem limitWords_length : limitWords.length = 620 := by
  decide +kernel

theorem digitLists_lt : ∀ {m : Nat} {w : List Nat}, w ∈ digitLists m → ∀ x ∈ w, x < 10
  | 0, w, h => by
      simp only [digitLists, List.mem_singleton] at h
      subst h
      simp
  | m + 1, w, h => by
      simp only [digitLists, List.mem_flatMap, List.mem_range, List.mem_map] at h
      obtain ⟨a, ha, t, ht, rfl⟩ := h
      intro x hx
      simp only [List.mem_cons] at hx
      rcases hx with rfl | hx
      · exact ha
      · exact digitLists_lt ht x hx

/-- Method limit at width 3 for the 620 listed three-digit words: no width-3 rank certificate
of the Agent #124 kind accepts them (for any bound), and every forward-closed set containing
the projection of the 196 orbit at any time from 100 on contains them. -/
theorem limit_words : ∀ w ∈ limitWords,
    (∀ Rk : List Nat → Option Nat, RowsClosed 3 Rk → ∀ b, entryOK 3 Rk (w, b) = false) ∧
    (∀ t : CodeTree, t.All (fun c _ => fwdOK t 3 c = true) → ∀ s,
      Mem t (wordPrefix (iterPairs q100 47 s).2 3) → Mem t w) := by
  intro w hw
  unfold limitWords at hw
  rw [List.mem_filter] at hw
  obtain ⟨hd, hf⟩ := hw
  simp only [Bool.and_eq_true] at hf
  have hlen : w.length = 3 := digitLists_length hd
  have hb : ∀ x ∈ w, x < 19 := fun x hx => by have := digitLists_lt hd x hx; omega
  have hdec : decode (wordCode w) = w := decode_wordCode w hb (by omega)
  refine ⟨fun Rk rows b => ?_, fun t ht s hs => ?_⟩
  · have := entryOK_false Rk rows (wordCode w) hf.2 b
    rwa [hdec] at this
  · have := forward_optimal t ht s hs (wordCode w) hf.2
    rwa [hdec] at this

end Sprint.Agent02.W3

#print axioms Sprint.Agent02.W3.fset_connected
#print axioms Sprint.Agent02.W3.forward_optimal
#print axioms Sprint.Agent02.W3.no_rank_on_fset
#print axioms Sprint.Agent02.W3.entryOK_false
#print axioms Sprint.Agent02.W3.limitWords_length
#print axioms Sprint.Agent02.W3.limit_words

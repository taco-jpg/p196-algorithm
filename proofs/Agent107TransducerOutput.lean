import Agent107TransducerPath

/-! Exact emitted folded words, including the odd-overflow extra pair. -/
namespace Agent107.FoldedTransducer
open DecimalDigits FoldedDecimal

theorem actual_emit_no_overflow (L : Nat) (q : Nat → Nat) (i : Nat)
    (hi : i < L) (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hc : carry q L = 0) :
    emit (actualState L q i) (q i) (actualState L q (i + 1)).high =
      nextColumns q L i := by
  have he : L - (i + 1) = L - 1 - i := by omega
  simpa [emit, actualState, hc, he] using
    (folded_emission_no_overflow q L i hi hs hc).symm

theorem actual_emit_overflow (L : Nat) (q : Nat → Nat) (i : Nat)
    (hi : i < L) (hc : carry q L = 1) :
    emit (actualState L q i) (q i) (actualState L q (i + 1)).high =
      nextColumns q L i := by
  simpa [emit, actualState, hc] using
    (folded_emission_overflow q L i hi hc).symm

theorem actual_emit (L : Nat) (q : Nat → Nat) (hAd : Admissible L q)
    (i : Nat) (hi : i < L / 2) :
    emit (actualState L q i) (q i) (actualState L q (i + 1)).high =
      nextColumns q L i := by
  have hb := carry_bounded q L hAd.2.2.1 L (by omega)
  have hiL : i < L := by omega
  by_cases hc : carry q L = 0
  · exact actual_emit_no_overflow L q i hiL hAd.2.2.2.1 hc
  · exact actual_emit_overflow L q i hiL (by omega)

theorem foldPrefix_congr (L : Nat) (q r : Nat → Nat)
    (h : ∀ i, i < L → q i = r i) : foldPrefix L q = foldPrefix L r := by
  have hp : List.ofFn (fun i : Fin (L / 2) => q i.val) =
      List.ofFn (fun i : Fin (L / 2) => r i.val) := by
    congr 1
    funext i
    exact h i.val (by have := i.isLt; omega)
  have hc : inputCenter L q = inputCenter L r := by
    unfold inputCenter
    split
    · rfl
    · rw [h (L / 2) (by omega)]
  unfold foldPrefix
  rw [hp, hc]

theorem pathOutput_congr (L : Nat) (q : Nat → Nat) (p r : Nat → State)
    (h : ∀ i, i ≤ L / 2 → p i = r i) :
    pathOutput L q p = pathOutput L q r := by
  have hp : List.ofFn (fun i : Fin (L / 2) => emit (p i.val) (q i.val) (p (i.val+1)).high) =
      List.ofFn (fun i : Fin (L / 2) => emit (r i.val) (q i.val) (r (i.val+1)).high) := by
    congr 1
    funext i
    rw [h i.val (by have := i.isLt; omega),
      h (i.val+1) (by have := i.isLt; omega)]
  simp only [pathOutput, hp, h (L / 2) (by omega)]

theorem ofFn_append_last (f : Nat → Nat) (k : Nat) :
    List.ofFn (fun i : Fin (k+1) => f i.val) =
      List.ofFn (fun i : Fin k => f i.val) ++ [f k] := by
  apply List.ext_getElem
  · simp
  · intro i hi hj
    by_cases hik : i < k
    · rw [List.getElem_append_left (by simpa only [List.length_ofFn] using hik)]
      simp only [List.getElem_ofFn]
    · have hie : i = k := by simp only [List.length_ofFn] at hi; omega
      subst i
      rw [List.getElem_append_right (by simp only [List.length_ofFn]; omega)]
      simp only [List.getElem_ofFn, List.length_ofFn, Nat.sub_self,
        List.getElem_cons_zero]

theorem actual_output_even_no_overflow (k : Nat) (q : Nat → Nat)
    (hs : ∀ i, i < 2*k → q i = q (2*k-1-i))
    (hc : carry q (2*k) = 0) :
    pathOutput (2*k) q (actualState (2*k) q) = foldPrefix (2*k) (nextColumns q (2*k)) := by
  have hd : 2*k/2 = k := by omega
  have hm : (2*k)%2 = 0 := by omega
  simp only [pathOutput, foldPrefix, inputCenter, hd, hm, ite_true,
    terminalExtra, terminalCenter, actualState, hc, ite_true, Option.map_none,
    Option.toList_none, List.append_nil]
  congr 1
  congr 1
  funext i
  simpa only [actualState, hc, ite_true] using
    actual_emit_no_overflow (2*k) q i.val (by have := i.isLt; omega) hs hc

theorem actual_output_even_overflow (k : Nat) (q : Nat → Nat)
    (hc : carry q (2*k) = 1) :
    pathOutput (2*k) q (actualState (2*k) q) = foldPrefix (2*k+1) (nextColumns q (2*k)) := by
  have hd : 2*k/2 = k := by omega
  have hd' : (2*k+1)/2 = k := by omega
  have hm : (2*k)%2 = 0 := by omega
  have hm' : (2*k+1)%2 = 1 := by omega
  have hk : 2*k-k = k := by omega
  have hcenter := even_center_overflow q k hc
  simp only [pathOutput, foldPrefix, inputCenter, hd, hd', hm, hm', ite_true,
    Nat.one_ne_zero, ite_false, terminalExtra, terminalCenter, actualState,
    hc, Nat.one_ne_zero, ite_false, Option.map, Option.toList,
    List.append_nil, Int.toNat, hk]
  rw [hd, hd']
  congr 1
  · congr 1
    funext i
    simpa only [actualState, hc, Nat.one_ne_zero, ite_false] using
      actual_emit_overflow (2*k) q i.val (by have := i.isLt; omega) hc
  · exact congrArg some hcenter.symm

theorem actual_output_odd_no_overflow (k : Nat) (q : Nat → Nat)
    (hs : ∀ i, i < 2*k+1 → q i = q (2*k+1-1-i))
    (hc : carry q (2*k+1) = 0) :
    pathOutput (2*k+1) q (actualState (2*k+1) q) =
      foldPrefix (2*k+1) (nextColumns q (2*k+1)) := by
  have hd : (2*k+1)/2 = k := by omega
  have hm : (2*k+1)%2 = 1 := by omega
  have hcenter := odd_center_no_overflow q k hc
  simp only [pathOutput, foldPrefix, inputCenter, hd, hm, Nat.one_ne_zero,
    ite_false, terminalExtra, terminalCenter, actualState, hc, ite_true,
    Option.map_some, Option.toList_none, List.append_nil]
  congr 1
  · congr 1
    funext i
    simpa only [actualState, hc, ite_true] using
      actual_emit_no_overflow (2*k+1) q i.val (by have := i.isLt; omega) hs hc
  · exact congrArg some hcenter.symm

theorem actual_output_odd_overflow (k : Nat) (q : Nat → Nat)
    (hc : carry q (2*k+1) = 1) :
    pathOutput (2*k+1) q (actualState (2*k+1) q) =
      foldPrefix (2*k+2) (nextColumns q (2*k+1)) := by
  have hd : (2*k+1)/2 = k := by omega
  have hd' : (2*k+2)/2 = k+1 := by omega
  have hm : (2*k+1)%2 = 1 := by omega
  have hm' : (2*k+2)%2 = 0 := by omega
  have hk : 2*k+1-k = k+1 := by omega
  have hcenter := odd_center_overflow q k hc
  simp only [pathOutput, foldPrefix, inputCenter, hd, hd', hm, hm',
    Nat.one_ne_zero, ite_false, ite_true, terminalExtra, terminalCenter,
    actualState, hc, Nat.one_ne_zero, ite_false, Option.map,
    Option.toList, Int.toNat, hk]
  rw [hd, hd']
  congr 1
  rw [ofFn_append_last (nextColumns q (2*k+1)) k]
  congr 1
  · congr 1
    funext i
    simpa only [actualState, hc, Nat.one_ne_zero, ite_false] using
      actual_emit_overflow (2*k+1) q i.val (by have := i.isLt; omega) hc
  · exact congrArg (fun n => [n]) hcenter.symm

theorem actual_output (L : Nat) (q : Nat → Nat) (hAd : Admissible L q) :
    pathOutput L q (actualState L q) = foldPrefix (nextWidth q L) (nextColumns q L) := by
  have hb := carry_bounded q L hAd.2.2.1 L (by omega)
  have hrepr : L = 2*(L/2) + L%2 := by omega
  by_cases he : L%2=0
  · have hL : L=2*(L/2) := by omega
    generalize hk : L/2 = k at *
    subst L
    by_cases hc : carry q (2*k)=0
    · simpa [nextWidth, hc] using actual_output_even_no_overflow k q hAd.2.2.2.1 hc
    · have hc1 : carry q (2*k)=1 := by omega
      simpa [nextWidth, hc1] using actual_output_even_overflow k q hc1
  · have hL : L=2*(L/2)+1 := by omega
    generalize hk : L/2 = k at *
    subst L
    by_cases hc : carry q (2*k+1)=0
    · simpa [nextWidth, hc] using actual_output_odd_no_overflow k q hAd.2.2.2.1 hc
    · have hc1 : carry q (2*k+1)=1 := by omega
      simpa [nextWidth, hc1, Nat.add_assoc] using actual_output_odd_overflow k q hc1

theorem accepting_output (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (hAd : Admissible L q) (hp : Accepts L q p) :
    pathOutput L q p = foldPrefix (nextWidth q L) (nextColumns q L) := by
  rw [pathOutput_congr L q p (actualState L q)
    (accepting_state_eq_actual L q p hAd hp)]
  exact actual_output L q hAd

#print axioms actual_emit
#print axioms foldPrefix_congr
#print axioms actual_output
#print axioms accepting_output

end Agent107.FoldedTransducer

import resume_normalization_bridge
import resume_renewal_extraction
import resume_normalization_reach

namespace OverflowNormalizationNine
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate
open OverflowCarryNormalization NormalizationBridge NormalizationReach
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem outer_large_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hlarge : 10 ≤ q 0) : carry q L = 1 := by
  have hp := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have he : L=L-1+1 := by have := ha.1; omega
  have hs := ha.2.2.2.1 0 ha.1
  simp only [Nat.sub_zero] at hs
  have hf : carry q L = (q (L-1) + carry q (L-1))/10 := by
    exact (congrArg (carry q) he).trans (by rfl)
  have hq := ha.2.2.1 0 ha.1
  rw [hf, ←hs]
  omega

theorem normalized9_low_after_three (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (ho : normalizedZero q L 0 = 9) :
    let r := normalizedZero q L
    let s := nextColumns r L
    let t := nextColumns s (L+1)
    let u := nextColumns t (L+2)
    ∀ i, i < L+2 → u i ≤ 9 := by
  let r := normalizedZero q L
  let s := nextColumns r L
  let t := nextColumns s (L+1)
  let u := nextColumns t (L+2)
  change ∀ i, i < L+2 → u i ≤ 9
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have os : s 0=10 := by
    have he := next_column_overflow_outer r L hL cr
    have hr : carry r 1=0 := by simp [carry, r, ho]
    change r 0 = 9 at ho
    change s 0 + 10*carry r 1 = r 0+1 at he
    omega
  have as' := admissible_next r L ar
  have as_ : Admissible (L+1) s := by simpa [nextWidth,cr] using as'
  have cs : carry s (L+1)=1 := outer_large_overflow s (L+1) as_ (by omega)
  have ot : t 0=1 := by
    have he := next_column_overflow_outer s (L+1) (by omega) cs
    have hs1 : carry s 1=1 := by simp [carry,os]
    change t 0 + 10*carry s 1 = s 0+1 at he
    omega
  have at' := admissible_next s (L+1) as_
  have at_ : Admissible (L+2) t := by simpa [nextWidth,cs,Nat.add_assoc] using at'
  have ct : carry t (L+2)=0 := outer_small_no_overflow t (L+2) at_ (by omega)
  have au' := admissible_next t (L+2) at_
  have au : Admissible (L+2) u := by simpa [nextWidth,ct] using au'
  let ns := fun i => carry r i + 2*carry r (L-i)
  let layers := fun i => [traceState r L 1 i, traceState s (L+1) 1 i,
    traceState t (L+2) 0 i]
  have hns0 : ns 0=2 := by simp [ns,carry,cr]
  have hlay0 : layers 0 = [1,1,0].map (fun h => 2*h + if h=1 then 4 else 0) := by
    simp only [layers, traceState_initial r L 1 cr,
      traceState_initial s (L+1) 1 cs, traceState_initial t (L+2) 0 ct]
    rfl
  have hn : ∀ i, i<L → (r i,ns (i+1)) ∈ normEdges (ns i) := by
    intro i hi
    exact normalizedZero_folded_edge q L i hq hs hi
  have hfeed : ∀ i, i<L → (layers (i+1), u i) ∈ feed (layers i) (r i) [1,1,0] := by
    intro i hi
    exact feed_cons_mem _ _ _ _ _ _ _ _ _
      (edge_trace r L 1 i ar.2.2.1 ar.2.2.2.1 hi (Or.inr rfl) cr)
      (feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace s (L+1) 1 i as_.2.2.1 as_.2.2.2.1 (by omega) (Or.inr rfl) cs)
        (feed_cons_mem _ _ _ _ _ _ _ _ _
          (edge_trace t (L+2) 0 i at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
          (by simp [feed,u])))
  let k := L/2
  have hkL : L=2*k ∨ L=2*k+1 := by omega
  have hk : 0<k := by
    by_cases h : k=0
    · have hl1 : L=1 := by omega
      have he := ar.2.2.2.2 0 hL (by omega)
      change r 0=9 at ho
      omega
    · omega
  have hrch : Reach 9 [1,1,0] ⟨ns k,layers k,badPrefix u k⟩ :=
    reach_of_traces 9 [1,1,0] ns layers r u k hns0 hlay0 ho
      (fun i hi => hn i (by omega)) (fun i hi => hfeed i (by omega)) hk
  have hsafe := normalized9_graph_safe _ hrch
  rcases hkL with hEven | hOdd
  · have hf3 : badPrefix u (k+1) ∈
        finish [traceState t (L+2) 0 (k+1)] none [0] (badPrefix u (k+1)) := by
      have he : L+2=2*(k+1) := by omega
      rw [he]
      exact finish_trace_even_no_overflow t (k+1) (by simpa [←he] using at_.2.2.1)
        [] [] _ _ (finish_empty_none _)
    have hfeed3 : ([traceState t (L+2) 0 (k+1)],u k) ∈
        feed [traceState t (L+2) 0 k] (t k) [0] := by
      exact feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace t (L+2) 0 k at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
        (by simp [feed,u])
    have hf2 : badPrefix u (k+1) ∈
        finish [traceState s (L+1) 1 k, traceState t (L+2) 0 k]
          (some (s k)) [1,0] (badPrefix u k) := by
      have he : L+1=2*k+1 := by omega
      rw [he]
      apply finish_trace_odd_overflow s k (by simpa [←he] using as_.2.2.1)
        (by simpa [←he] using cs) [traceState t (L+2) 0 k] [0]
        [traceState t (L+2) 0 (k+1)] (u k) (badPrefix u k) (badPrefix u (k+1))
      · simpa only [←he] using hfeed3
      · exact hf3
    have hf1 : badPrefix u (k+1) ∈ finish (layers k) none [1,1,0] (badPrefix u k) := by
      change badPrefix u (k+1) ∈ finish
        (traceState r L 1 k :: [traceState s (L+1) 1 k, traceState t (L+2) 0 k])
        none [1,1,0] (badPrefix u k)
      rw [hEven]
      apply finish_trace_even_overflow r k (by simpa [←hEven] using ar.2.2.1)
        (by simpa [←hEven] using cr)
      simpa only [←hEven] using hf2
    have hneq : ns k%2=ns k/2 := by
      have hb := carry_bounded r L ar.2.2.1 k (by omega)
      have he : L-k=k := by omega
      simp only [ns,he]
      omega
    have hb := hsafe _ (finals_mem_none [1,1,0] ⟨ns k,layers k,badPrefix u k⟩
      _ hneq hf1)
    have hp := (badPrefix_eq_false_iff u (k+1)).mp hb
    intro i hi
    by_cases hil : i<k+1
    · exact hp i hil
    · rw [au.2.2.2.1 i hi]
      exact hp _ (by omega)
  · have hf3 : badPrefix u (k+2) ∈
        finish [traceState t (L+2) 0 (k+1)] (some (t (k+1))) [0] (badPrefix u (k+1)) := by
      have he : L+2=2*(k+1)+1 := by omega
      rw [he]
      apply finish_trace_odd_no_overflow t (k+1) (by simpa [←he] using at_.2.2.1)
        (by simpa [←he] using ct) [] []
      simpa only [←he] using finish_empty_some (badPrefix u (k+1)) (u (k+1))
    have hf2 : badPrefix u (k+2) ∈
        finish [traceState s (L+1) 1 (k+1),traceState t (L+2) 0 (k+1)]
          none [1,0] (badPrefix u (k+1)) := by
      have he : L+1=2*(k+1) := by omega
      rw [he]
      apply finish_trace_even_overflow s (k+1) (by simpa [←he] using as_.2.2.1)
        (by simpa [←he] using cs)
      simpa only [←he] using hf3
    have hfeed23 : ([traceState s (L+1) 1 (k+1),traceState t (L+2) 0 (k+1)],u k) ∈
        feed [traceState s (L+1) 1 k,traceState t (L+2) 0 k] (s k) [1,0] := by
      exact feed_cons_mem _ _ _ _ _ _ _ _ _
        (edge_trace s (L+1) 1 k as_.2.2.1 as_.2.2.2.1 (by omega) (Or.inr rfl) cs)
        (feed_cons_mem _ _ _ _ _ _ _ _ _
          (edge_trace t (L+2) 0 k at_.2.2.1 at_.2.2.2.1 (by omega) (Or.inl rfl) ct)
          (by simp [feed,u]))
    have hf1 : badPrefix u (k+2) ∈ finish (layers k) (some (r k)) [1,1,0] (badPrefix u k) := by
      change badPrefix u (k+2) ∈ finish
        (traceState r L 1 k :: [traceState s (L+1) 1 k,traceState t (L+2) 0 k])
        (some (r k)) [1,1,0] (badPrefix u k)
      rw [hOdd]
      apply finish_trace_odd_overflow r k (by simpa [←hOdd] using ar.2.2.1)
        (by simpa [←hOdd] using cr) _ _ _ (u k)
      · simpa only [←hOdd] using hfeed23
      · simpa only [←hOdd] using hf2
    have hcenter : r k=10*(ns k/2) := by
      have ha := carry_bounded r L ar.2.2.1 k (by omega)
      have hb := carry_bounded r L ar.2.2.1 (L-k) (by omega)
      have hnsc : ns k/2=carry r (L-k) := by simp only [ns]; omega
      rw [hnsc]
      change normalizedZero q L k = 10*carry (normalizedZero q L) (L-k)
      rw [hOdd]
      exact normalizedZero_odd_center q k (by simpa [←hOdd] using hq) (by simpa [←hOdd] using hs)
    rw [hcenter] at hf1
    have hb := hsafe _ (finals_mem_some [1,1,0] ⟨ns k,layers k,badPrefix u k⟩ _ hf1)
    have hp := (badPrefix_eq_false_iff u (k+2)).mp hb
    intro i hi
    by_cases hil : i<k+2
    · exact hp i hil
    · rw [au.2.2.2.1 i hi]
      exact hp _ (by omega)

#print axioms normalized9_low_after_three

theorem normalized9_iterPairs_low_after_three (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L-1-i))
    (hc : carry q L = 1)
    (ho : normalizedZero q L 0 = 9) :
    ∀ i, i < (iterPairs (normalizedZero q L) L 3).1 →
      (iterPairs (normalizedZero q L) L 3).2 i ≤ 9 := by
  let r := normalizedZero q L
  let s := nextColumns r L
  let t := nextColumns s (L+1)
  let u := nextColumns t (L+2)
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have wr : nextWidth r L=L+1 := by simp [nextWidth,cr]
  have os : s 0=10 := by
    have he := next_column_overflow_outer r L hL cr
    have hr : carry r 1=0 := by simp [carry,r,ho]
    change r 0=9 at ho
    change s 0+10*carry r 1=r 0+1 at he
    omega
  have as_ : Admissible (L+1) s := by simpa only [wr] using admissible_next r L ar
  have cs : carry s (L+1)=1 := outer_large_overflow s (L+1) as_ (by omega)
  have ws : nextWidth s (L+1)=L+2 := by simp [nextWidth,cs,Nat.add_assoc]
  have ot : t 0=1 := by
    have he := next_column_overflow_outer s (L+1) (by omega) cs
    have hs1 : carry s 1=1 := by simp [carry,os]
    change t 0+10*carry s 1=s 0+1 at he
    omega
  have at_ : Admissible (L+2) t := by simpa only [ws] using admissible_next s (L+1) as_
  have ct : carry t (L+2)=0 := outer_small_no_overflow t (L+2) at_ (by omega)
  have wt : nextWidth t (L+2)=L+2 := by simp [nextWidth,ct]
  have hiw : iterPairs r L 3=(L+2,u) := by
    simp only [iterPairs,wr]
    change (nextWidth (nextColumns s (L+1)) (nextWidth s (L+1)),
      nextColumns (nextColumns s (L+1)) (nextWidth s (L+1)))=(L+2,u)
    rw [ws]
    change (nextWidth t (L+2),u)=(L+2,u)
    rw [wt]
  change ∀ i, i < (iterPairs r L 3).1 → (iterPairs r L 3).2 i ≤ 9
  rw [hiw]
  exact normalized9_low_after_three q L hL hq hs hc ho

#print axioms normalized9_iterPairs_low_after_three
end OverflowNormalizationNine

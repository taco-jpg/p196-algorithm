import resume_normalization_bridge
import resume_normalization_reach
import resume_renewal_extraction
namespace NormalizationTen
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate OverflowCarryNormalization
open NormalizationBridge NormalizationReach
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem normalized10_low_after_two (q : Nat → Nat) (L : Nat)
    (hL : 0<L) (hq : ∀ i, i<L → q i≤18)
    (hs : ∀ i, i<L → q i=q (L-1-i)) (hc : carry q L=1)
    (hfirst : normalizedZero q L 0=10) :
    ∀ i, i<(iterPairs (normalizedZero q L) L 2).1 →
      (iterPairs (normalizedZero q L) L 2).2 i≤9 := by
  let r := normalizedZero q L
  let u := nextColumns r L
  let v := nextColumns u (L+1)
  change r 0=10 at hfirst
  have ar : Admissible L r := normalizedZero_admissible q L hL hc
  have cr : carry r L=1 := (normalizedZero_preserves_carry q L hq hs L (by omega)).trans hc
  have wr : nextWidth r L=L+1 := by simp [nextWidth,cr]
  have au : Admissible (L+1) u := by simpa only [wr] using admissible_next r L ar
  have u0 : u 0=1 := by
    have he := next_column_overflow_outer r L hL cr
    have c1 : carry r 1=1 := by change (r 0+0)/10=1; rw [hfirst]
    change u 0+10*carry r 1=r 0+1 at he
    rw [c1,hfirst] at he
    omega
  have cu : carry u (L+1)=0 := outer_small_no_overflow u (L+1) au (by omega)
  have wu : nextWidth u (L+1)=L+1 := by simp [nextWidth,cu]
  have av : Admissible (L+1) v := by simpa only [wu] using admissible_next u (L+1) au
  have hiw : iterPairs r L 2=(L+1,v) := by
    simp only [iterPairs,wr]
    change (nextWidth u (L+1),v)=(L+1,v)
    rw [wu]
  change ∀ i, i<(iterPairs r L 2).1 → (iterPairs r L 2).2 i≤9
  rw [hiw]
  simp only
  by_cases hsmall : L=1
  · subst L
    intro i hi
    have ui : u i=1 := by
      have us := au.2.2.2.1 i hi
      have hi' : i=0 ∨ i=1 := by omega
      rcases hi' with rfl | rfl
      · exact u0
      · simpa using us.trans u0
    have he := next_column_no_overflow u 2 i hi au.2.2.2.1 cu
    have c0 := carry_bounded u 2 au.2.2.1 i (by omega)
    have cm := carry_bounded u 2 au.2.2.1 (2-1-i) (by omega)
    change v i+10*(carry u (i+1)+carry u (2-i))=2*u i+carry u i+carry u (2-1-i) at he
    rw [ui] at he
    omega
  · let k := L/2
    have hk : 0<k := by dsimp [k]; omega
    let ns := fun i => carry r i+2*carry r (L-i)
    let layers := fun i => [traceState r L 1 i,traceState u (L+1) 0 i]
    have hr : Reach 10 [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
      apply reach_of_traces 10 [1,0] ns layers r v k
      · dsimp [ns]; simp [carry,cr]
      · simp only [layers,traceState_initial r L 1 cr,traceState_initial u (L+1) 0 cu]
        decide
      · exact hfirst
      · intro i hi
        exact normalizedZero_folded_edge q L i hq hs (by dsimp [k] at hi; omega)
      · intro i hi
        have hir : i<L := by dsimp [k] at hi; omega
        have hiu : i<L+1 := by omega
        apply feed_cons_mem
        · exact edge_trace r L 1 i ar.2.2.1 ar.2.2.2.1 hir (Or.inr rfl) cr
        · apply feed_cons_mem
          · exact edge_trace u (L+1) 0 i au.2.2.1 au.2.2.2.1 hiu (Or.inl rfl) cu
          · simp [feed,v]
      · exact hk
    have hcases : L=2*k ∨ L=2*k+1 := by dsimp [k]; omega
    rcases hcases with heven | hodd
    · have huwid : L+1=2*k+1 := by omega
      have fm : (badPrefix v k || decide (v k>9)) ∈ finals [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
        apply finals_mem_none
        · change (carry r k+2*carry r (L-k))%2=(carry r k+2*carry r (L-k))/2
          have cb := carry_bounded r L ar.2.2.1 k (by omega)
          have hind : L-k=k := by omega
          rw [hind]; omega
        · change (badPrefix v k || decide (v k>9)) ∈
            finish [traceState r L 1 k,traceState u (L+1) 0 k] none [1,0] (badPrefix v k)
          have f0 := finish_empty_some (badPrefix v k) (v k)
          have f1 := finish_trace_odd_no_overflow u k (by simpa only [←huwid] using au.2.2.1)
            (by simpa only [←huwid] using cu) [] [] (badPrefix v k) _ (by simpa only [←huwid] using f0)
          have f2 := finish_trace_even_overflow r k (by simpa only [←heven] using ar.2.2.1)
            (by simpa only [←heven] using cr) [traceState u (L+1) 0 k] [0]
            (badPrefix v k) _ (by simpa only [←heven,←huwid] using f1)
          simpa only [←heven] using f2
      have hz := normalized10_graph_safe _ hr _ fm
      have hb : badPrefix v k=false := by simp only [Bool.or_eq_false_iff] at hz; exact hz.1
      have hmid : v k≤9 := by simp only [Bool.or_eq_false_iff,decide_eq_false_iff_not] at hz; omega
      have hp := (badPrefix_eq_false_iff v k).mp hb
      intro i hi
      by_cases hil : i<k
      · exact hp i hil
      · by_cases hie : i=k
        · simpa [hie] using hmid
        · have hs' := av.2.2.2.1 i hi
          rw [hs']
          exact hp (L+1-1-i) (by omega)
    · have huwid : L+1=2*(k+1) := by omega
      have fm : (badPrefix v k || decide (v k>9)) ∈ finals [1,0] ⟨ns k,layers k,badPrefix v k⟩ := by
        apply finals_mem_some
        have cb := carry_bounded r L ar.2.2.1 k (by omega)
        have db := carry_bounded r L ar.2.2.1 (L-k) (by omega)
        have nsfield : ns k/2=carry r (L-k) := by dsimp [ns]; omega
        have center : r k=10*(ns k/2) := by
          rw [nsfield]
          have hh := normalizedZero_odd_center q k (by simpa only [←hodd] using hq)
            (by simpa only [←hodd] using hs)
          simpa only [←hodd] using hh
        change (badPrefix v k || decide (v k>9)) ∈
          finish [traceState r L 1 k,traceState u (L+1) 0 k] (some (10*(ns k/2))) [1,0] (badPrefix v k)
        rw [←center]
        have he : ([traceState u (L+1) 0 (k+1)],v k) ∈ feed [traceState u (L+1) 0 k] (u k) [0] := by
          apply feed_cons_mem
          · exact edge_trace u (L+1) 0 k au.2.2.1 au.2.2.2.1 (by omega) (Or.inl rfl) cu
          · simp [feed,v]
        have f0 := finish_empty_none (badPrefix v k || decide (v k>9))
        have f1 := finish_trace_even_no_overflow u (k+1) (by simpa only [←huwid] using au.2.2.1)
          [] [] (badPrefix v k || decide (v k>9)) _ f0
        have f2 := finish_trace_odd_overflow r k (by simpa only [←hodd] using ar.2.2.1)
          (by simpa only [←hodd] using cr) [traceState u (L+1) 0 k] [0]
          [traceState u (L+1) 0 (k+1)] (v k) (badPrefix v k) _
          (by simpa only [←hodd] using he) (by simpa only [←huwid] using f1)
        simpa only [←hodd] using f2
      have hz := normalized10_graph_safe _ hr _ fm
      have hb : badPrefix v (k+1)=false := by simpa only [badPrefix] using hz
      have hp := (badPrefix_eq_false_iff v (k+1)).mp hb
      intro i hi
      by_cases hil : i<k+1
      · exact hp i hil
      · have hs' := av.2.2.2.1 i hi
        rw [hs']
        exact hp (L+1-1-i) (by omega)

#print axioms normalized10_low_after_two
end NormalizationTen

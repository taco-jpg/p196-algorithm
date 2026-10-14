import Lychrel196Research
import resume_renewal_certificate
namespace NormalizationBridge
open DecimalDigits FoldedDecimal OverflowNormalizationCertificate
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

def traceState (q : Nat → Nat) (L h i : Nat) : Nat :=
  carry q i + 2 * carry q (L-i) + if h=1 then 4*extended q L (L-i) else 0

theorem traceState_fields (q : Nat → Nat) (L h i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : i ≤ L) :
    traceState q L h i % 2 = carry q i ∧
    traceState q L h i / 2 % 2 = carry q (L-i) ∧
    traceState q L h i / 4 = if h=1 then extended q L (L-i) else 0 := by
  have ha := carry_bounded q L hq i hi
  have hb := carry_bounded q L hq (L-i) (by omega)
  unfold traceState
  split <;> omega

theorem traceState_initial (q : Nat → Nat) (L h : Nat)
    (hc : carry q L = h) : traceState q L h 0 = 2*h + if h=1 then 4 else 0 := by
  simp [traceState, carry, extended, hc]
  split <;> simp_all

theorem edge_trace (q : Nat → Nat) (L h i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18)
    (hs : ∀ j, j < L → q j = q (L-1-j))
    (hi : i < L) (hh : h=0 ∨ h=1) (hc : carry q L = h) :
    (traceState q L h (i+1), nextColumns q L i) ∈ edge (traceState q L h i) (q i) h := by
  have hf := traceState_fields q L h i hq (by omega)
  have hn := traceState_fields q L h (i+1) hq (by omega)
  have hb := carry_bounded q L hq (L-1-i) (by omega)
  have hmem : carry q (L-1-i) ∈ [0,1] := by simp; omega
  have ht := folded_carry_transition q L i hi hs
  have hid : L-(i+1)=L-1-i := by omega
  simp only [edge, hf.1, hf.2.1, hf.2.2, List.mem_flatMap]
  refine ⟨carry q (L-1-i), hmem, ?_⟩
  rw [← ht.2]
  simp only [if_true, List.mem_singleton, Prod.mk.injEq]
  constructor
  · simp only [traceState, hid, ht.1]
    rcases hh with rfl | rfl
    · simp
    · simp only [if_true]
      rw [← folded_delay_update q L i hi hs, hid]
  · rcases hh with rfl | rfl
    · simp only [Nat.zero_ne_one, if_false]
      exact folded_emission_no_overflow q L i hi hs hc
    · simp only [if_true]
      exact folded_emission_overflow q L i hi hc

theorem feed_cons_mem (s q h st r : Nat) (ss hs tail : List Nat) (v : Nat)
    (he : (st,r) ∈ edge s q h) (hf : (tail,v) ∈ feed ss r hs) :
    (st::tail,v) ∈ feed (s::ss) q (h::hs) := by
  simp only [feed, List.mem_flatMap]
  exact ⟨(st,r),he, by simp only [List.mem_map]; exact ⟨(tail,v),hf,rfl⟩⟩

theorem canonical_admissible (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : Admissible L (columnSum d L) := by
  refine ⟨hc.1, ?_, columnSum_bounded d L hc.2.1, columnSum_symmetric d L, ?_⟩
  · have hl := hc.2.2.1
    simp only [columnSum, reflected, Nat.sub_zero]
    omega
  · intro i hi heq
    simp only [columnSum, reflected, ← heq]
    omega

theorem admissible_congr (L : Nat) (q r : Nat → Nat) (ha : Admissible L q)
    (he : ∀ i, i<L → q i=r i) : Admissible L r := by
  refine ⟨ha.1, by rw [←he 0 ha.1]; exact ha.2.1, ?_, ?_, ?_⟩
  · intro i hi; rw [←he i hi]; exact ha.2.2.1 i hi
  · intro i hi; rw [←he i hi, ←he (L-1-i) (by omega)]; exact ha.2.2.2.1 i hi
  · intro i hi hm; rw [←he i hi]; exact ha.2.2.2.2 i hi hm

theorem admissible_next (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    Admissible (nextWidth q L) (nextColumns q L) := by
  obtain ⟨n,d,_,hc,hr⟩ := valid_word_realizable q L ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  obtain ⟨e,he,hr'⟩ := representation_next n d q L hc hr
  exact admissible_congr _ _ _ (canonical_admissible _ _ _ he) hr'

theorem outer_small_no_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hsmall : q 0 ≤ 8) : carry q L=0 := by
  have hp := carry_bounded q L ha.2.2.1 (L-1) (by omega)
  have he : L=L-1+1 := by have := ha.1; omega
  have hs := ha.2.2.2.1 0 ha.1
  simp only [Nat.sub_zero] at hs
  have hf : carry q L = (q (L-1) + carry q (L-1))/10 := by
    exact (congrArg (carry q) he).trans (by rfl)
  rw [hf, ←hs]
  omega


theorem finish_even_overflow (s z : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : s%2=s/2%2) (hz : z=2*(s/4))
    (hf : b ∈ finish ss (some z) hs bad) :
    b ∈ finish (s::ss) none (1::hs) bad := by
  simpa [finish, finishFuel, hc, hz] using hf

theorem finish_even_no_overflow (s : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : s%2=s/2%2)
    (hf : b ∈ finish ss none hs bad) :
    b ∈ finish (s::ss) none (0::hs) bad := by
  simpa [finish, finishFuel, hc] using hf

theorem finish_odd_no_overflow (s z v : Nat) (ss hs : List Nat) (bad b : Bool)
    (hc : (z+s%2)/10=s/2%2) (hv : v=2*((z+s%2)%10))
    (hf : b ∈ finish ss (some v) hs bad) :
    b ∈ finish (s::ss) (some z) (0::hs) bad := by
  simpa [finish, finishFuel, hc, hv] using hf

theorem finish_odd_overflow (s z : Nat) (ss hs tail : List Nat) (v : Nat) (bad b : Bool)
    (hc : (z+s%2)/10=s/2%2)
    (he : (tail,v) ∈ feed ss ((z+s%2)%10+s/4) hs)
    (hf : b ∈ finish tail none hs (bad || decide (v>9))) :
    b ∈ finish (s::ss) (some z) (1::hs) bad := by
  simp only [finish, List.length_cons, Nat.add_comm hs.length 1, finishFuel,
    hc, if_true, List.mem_flatMap]
  refine ⟨(tail,v),he,?_⟩
  simpa only [finish, Nat.add_comm hs.length 1] using hf

theorem finish_empty_none (bad : Bool) : bad ∈ finish [] none [] bad := by
  simp [finish,finishFuel]

theorem finish_empty_some (bad : Bool) (z : Nat) :
    (bad || decide (z>9)) ∈ finish [] (some z) [] bad := by
  simp [finish,finishFuel]


theorem finish_trace_even_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k → q j≤18) (hc : carry q (2*k)=1)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail (some (nextColumns q (2*k) k)) hs bad) :
    b ∈ finish (traceState q (2*k) 1 k::tail) none (1::hs) bad := by
  have hd := traceState_fields q (2*k) 1 k hq (by omega)
  apply finish_even_overflow _ (nextColumns q (2*k) k) tail hs bad b
  · rw [hd.1,hd.2.1]; congr 1; omega
  · rw [hd.2.2]; have hi : 2*k-k=k := by omega
    simpa only [if_true,hi] using even_center_overflow q k hc
  · exact hf

theorem finish_trace_even_no_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k → q j≤18)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail none hs bad) :
    b ∈ finish (traceState q (2*k) 0 k::tail) none (0::hs) bad := by
  have hd := traceState_fields q (2*k) 0 k hq (by omega)
  apply finish_even_no_overflow _ tail hs bad b
  · rw [hd.1,hd.2.1]; congr 1; omega
  · exact hf

theorem finish_trace_odd_no_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k+1 → q j≤18) (hc : carry q (2*k+1)=0)
    (tail hs : List Nat) (bad b : Bool)
    (hf : b ∈ finish tail (some (nextColumns q (2*k+1) k)) hs bad) :
    b ∈ finish (traceState q (2*k+1) 0 k::tail) (some (q k)) (0::hs) bad := by
  have hd := traceState_fields q (2*k+1) 0 k hq (by omega)
  apply finish_odd_no_overflow _ (q k) (nextColumns q (2*k+1) k) tail hs bad b
  · rw [hd.1,hd.2.1]; exact (odd_center_carry q k).symm
  · rw [hd.1]; exact odd_center_no_overflow q k hc
  · exact hf

theorem finish_trace_odd_overflow (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j<2*k+1 → q j≤18) (hc : carry q (2*k+1)=1)
    (tail hs rest : List Nat) (v : Nat) (bad b : Bool)
    (he : (rest,v) ∈ feed tail (nextColumns q (2*k+1) k) hs)
    (hf : b ∈ finish rest none hs (bad || decide (v>9))) :
    b ∈ finish (traceState q (2*k+1) 1 k::tail) (some (q k)) (1::hs) bad := by
  have hd := traceState_fields q (2*k+1) 1 k hq (by omega)
  apply finish_odd_overflow _ (q k) tail hs rest v bad b
  · rw [hd.1,hd.2.1]; exact (odd_center_carry q k).symm
  · rw [hd.1,hd.2.2]
    have heq := odd_center_overflow q k hc
    have hi : 2*k+1-k=k+1 := by omega
    simp only [if_true,hi]
    rw [←heq]
    exact he
  · exact hf

#print axioms edge_trace
#print axioms admissible_next
end NormalizationBridge

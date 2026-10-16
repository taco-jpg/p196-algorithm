import NoAlternatingReturn

/-! STATIC_REPAIR_NOT_COMPILER_OBSERVED.
Exact frozen source headers, with every explicit argument supplied to the
original theorem. This is a review harness, not a new mathematical result.
Compilation is pending the separate executor; the initial file is preserved. -/
namespace Agent104.TemporalStripExactTypesApplied
open P196.Agent4.TemporalStrip

theorem left_scalar_type (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=0) (ly : (y+b)/10=r)
    (rx : x/10=u) (ry : (y+1)/10=v)
    (hd : (y+1)%10+r=4)
    (time : y=(x+a)%10+x%10) :
    (r=0 ∧ x=1 ∧ y=3 ∧ a=1 ∧ u=0 ∧ v=0) ∨
    (r=1 ∧ x=6 ∧ y=12 ∧ a=0 ∧ u=0 ∧ v=1) :=
  P196.Agent4.TemporalStrip.left_scalar x y a b r u v _hx _hy ha hb hr hu hv lx ly rx ry hd time

theorem right_scalar_type (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=1) (ly : (y+b)/10=r)
    (rx : (x+1)/10=u) (ry : y/10=v)
    (hd : y%10+r=6)
    (time : y=(x+a)%10+(x+1)%10) :
    (r=0 ∧ x=12 ∧ y=6 ∧ a=1 ∧ u=1 ∧ v=0) ∨
    (r=1 ∧ x=17 ∧ y=15 ∧ a=0 ∧ u=1 ∧ v=1) :=
  P196.Agent4.TemporalStrip.right_scalar x y a b r u v _hx _hy ha hb hr hu hv lx ly rx ry hd time

theorem left_backward_type {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : LeftAligned t) : LeftAligned s :=
  P196.Agent4.TemporalStrip.left_backward (J := J) next onto s t x y hs ht hc hgood

theorem right_backward_type {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : RightAligned t) : RightAligned s :=
  P196.Agent4.TemporalStrip.right_backward (J := J) next onto s t x y hs ht hc hgood

theorem no_alternating_six_twelve_strip_type {J : Type} (j0 : J) (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (cuts : Nat → Cut J)
    (x y : Nat → J → Nat) (width : Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column next (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False :=
  P196.Agent4.TemporalStrip.no_alternating_six_twelve_strip (J := J) j0 next onto cuts x y width hv hc outside tail

theorem cyclic_successor_onto_type (N : Nat) (hN : 0<N) :
    ∀ j : Fin N, ∃ i : Fin N,
      (⟨(i.val+1)%N, Nat.mod_lt _ hN⟩ : Fin N)=j :=
  P196.Agent4.TemporalStrip.cyclic_successor_onto N hN

theorem no_finite_alternating_six_twelve_strip_type (N width : Nat) (hN : 0<N)
    (cuts : Nat → Cut (Fin N)) (x y : Nat → Fin N → Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column
      (fun j => ⟨(j.val+1)%N,Nat.mod_lt _ hN⟩)
      (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False :=
  P196.Agent4.TemporalStrip.no_finite_alternating_six_twelve_strip N width hN cuts x y hv hc outside tail

end Agent104.TemporalStripExactTypesApplied

import NoAlternatingReturn

/-! Exact source-type checks; uncompiled at the initial semantic checkpoint. -/
namespace Agent104.TemporalStripExactTypes
open P196.Agent4.TemporalStrip

example (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=0) (ly : (y+b)/10=r)
    (rx : x/10=u) (ry : (y+1)/10=v)
    (hd : (y+1)%10+r=4)
    (time : y=(x+a)%10+x%10) :
    (r=0 ∧ x=1 ∧ y=3 ∧ a=1 ∧ u=0 ∧ v=0) ∨
    (r=1 ∧ x=6 ∧ y=12 ∧ a=0 ∧ u=0 ∧ v=1) := left_scalar

example (x y a b r u v : Nat)
    (_hx : x≤18) (_hy : y≤18) (ha : a≤1) (hb : b≤1) (hr : r≤1)
    (hu : u≤1) (hv : v≤1)
    (lx : (x+a)/10=1) (ly : (y+b)/10=r)
    (rx : (x+1)/10=u) (ry : y/10=v)
    (hd : y%10+r=6)
    (time : y=(x+a)%10+(x+1)%10) :
    (r=0 ∧ x=12 ∧ y=6 ∧ a=1 ∧ u=1 ∧ v=0) ∨
    (r=1 ∧ x=17 ∧ y=15 ∧ a=0 ∧ u=1 ∧ v=1) := right_scalar

example {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : LeftAligned t) : LeftAligned s := left_backward

example {J : Type} (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (s t : Cut J) (x y : J → Nat)
    (hs : Valid s) (ht : Valid t) (hc : Column next s t x y)
    (hgood : RightAligned t) : RightAligned s := right_backward

example {J : Type} (j0 : J) (next : J → J)
    (onto : ∀ j, ∃ i, next i=j) (cuts : Nat → Cut J)
    (x y : Nat → J → Nat) (width : Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column next (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False := no_alternating_six_twelve_strip

example (N : Nat) (hN : 0<N) :
    ∀ j : Fin N, ∃ i : Fin N,
      (⟨(i.val+1)%N, Nat.mod_lt _ hN⟩ : Fin N)=j := cyclic_successor_onto

example (N width : Nat) (hN : 0<N)
    (cuts : Nat → Cut (Fin N)) (x y : Nat → Fin N → Nat)
    (hv : ∀ i, i≤width → Valid (cuts i))
    (hc : ∀ i, i<width → Column
      (fun j => ⟨(j.val+1)%N,Nat.mod_lt _ hN⟩)
      (cuts i) (cuts (i+1)) (x i) (y i))
    (outside : Outside (cuts 0))
    (tail : LeftAligned (cuts width) ∨ RightAligned (cuts width)) : False := no_finite_alternating_six_twelve_strip

end Agent104.TemporalStripExactTypes

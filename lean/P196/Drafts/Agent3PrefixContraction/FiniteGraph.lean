import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ActualPrefixLift

namespace ScalarFinite
open ActualPrefixLift

/-- Zero transition code means absent; target v is stored as v+1.
Functions may be implemented by finite arrays with zero defaults. -/
structure Data where
  size : Nat
  phase : Nat → Nat
  last : Nat → Nat
  low : Nat → Nat
  next : Nat → Nat → Nat

def graph (D : Data) : Graph Nat where
  valid v := v < D.size
  phase := D.phase
  last := D.last
  low := D.low
  edge u v bit := bit ≤ 1 ∧ D.next u bit = v+1

def bounded {V : Type} (G : Graph V) : Graph V :=
  { G with edge := fun u v bit => bit ≤ 1 ∧ G.edge u v bit }

def CoverageRow (P : Data) (component : Nat → Nat) (selected count : Nat)
    (members memberIndex : Nat → Nat) (u : Nat) : Prop :=
  component u = selected → memberIndex u < count ∧ members (memberIndex u) = u

def FieldRow (P H : Data) (members : Nat → Nat) (z : Nat) : Prop :=
  H.phase z = P.phase (members (z/19)) ∧
  H.last z = z%19 ∧
  H.low z = (z%19 + P.low (members (z/19)))/10

def LiftRow (P H : Data) (component : Nat → Nat) (selected : Nat)
    (members memberIndex : Nat → Nat) (z bit : Nat) : Prop :=
  let parent := members (z/19)
  let coefficient := z%19
  let gamma := (coefficient+bit)/10
  let code := P.next parent gamma
  let target := code-1
  let nextCoefficient := PrefixExtension.nextCoefficient
    (P.last parent) coefficient (P.low parent) gamma
    (ScalarClock.overflowValue (P.phase parent)) bit
  code ≠ 0 → target < P.size → component target = selected →
  nextCoefficient < 19 →
    H.next z bit = 19*memberIndex target+nextCoefficient+1

/-- The finite certificate only needs a covering encoding; it need not
certify SCC construction or a converse realization of graph edges. -/
structure LiftCertificate (P H : Data) (component : Nat → Nat) (selected : Nat) where
  members : Nat → Nat
  memberIndex : Nat → Nat
  count : Nat
  size_eq : H.size = 19*count
  coverage : ∀ u, u < P.size → CoverageRow P component selected count members memberIndex u
  fields : ∀ z, z < H.size → FieldRow P H members z
  transitions : ∀ z, z < H.size → ∀ bit, bit ≤ 1 →
    LiftRow P H component selected members memberIndex z bit

def encode {P H : Data} {component : Nat → Nat} {selected : Nat}
    (certificate : LiftCertificate P H component selected) (v : Nat × Fin 19) : Nat :=
  19*certificate.memberIndex v.1+v.2.val

theorem encode_div {P H : Data} {component : Nat → Nat} {selected : Nat}
    (certificate : LiftCertificate P H component selected) (v : Nat × Fin 19) :
    encode certificate v / 19 = certificate.memberIndex v.1 := by
  have hv := v.2.isLt
  unfold encode
  omega

theorem encode_mod {P H : Data} {component : Nat → Nat} {selected : Nat}
    (certificate : LiftCertificate P H component selected) (v : Nat × Fin 19) :
    encode certificate v % 19 = v.2.val := by
  have hv := v.2.isLt
  unfold encode
  omega

theorem encode_valid {P H : Data} {component : Nat → Nat} {selected : Nat}
    (certificate : LiftCertificate P H component selected) (v : Nat × Fin 19)
    (hv : v.1 < P.size) (hc : component v.1 = selected) :
    encode certificate v < H.size := by
  have hi := (certificate.coverage v.1 hv hc).1
  have ha := v.2.isLt
  rw [certificate.size_eq]
  unfold encode
  omega

/-- Finite row checks imply every bounded analytic lift edge is present.
This avoids quantifying over all pairs of finite target vertices. -/
theorem lift_realization {P H : Data} {component : Nat → Nat} {selected : Nat}
    (certificate : LiftCertificate P H component selected) :
    Realization (bounded (lift (select (graph P) (fun v => component v=selected))))
      (graph H) (encode certificate) := by
  have hfields : ∀ v : Nat × Fin 19, v.1 < P.size → component v.1=selected →
      H.phase (encode certificate v) = P.phase v.1 ∧
      H.last (encode certificate v) = v.2.val ∧
      H.low (encode certificate v) = (v.2.val + P.low v.1)/10 := by
    intro v hv hc
    have hf := certificate.fields (encode certificate v) (encode_valid certificate v hv hc)
    unfold FieldRow at hf
    rw [encode_div,encode_mod,(certificate.coverage v.1 hv hc).2] at hf
    exact hf
  refine ⟨?_,?_,?_,?_,?_⟩
  · intro v hv
    exact encode_valid certificate v hv.1 hv.2
  · intro v hv
    exact (hfields v hv.1 hv.2).1
  · intro v hv
    exact (hfields v hv.1 hv.2).2.1
  · intro v hv
    exact (hfields v hv.1 hv.2).2.2
  · intro u v bit hu hv hedge
    obtain ⟨hbit,gamma,hparent,hchoice⟩ := hedge
    obtain ⟨hgamma,hnext,hlow⟩ := hchoice
    have htable : P.next u.1 ((u.2.val+bit)/10) = v.1+1 := by
      rw [← hgamma]
      exact hparent.2
    have hrow := certificate.transitions (encode certificate u)
      (encode_valid certificate u hu.1 hu.2) bit hbit
    simp only [LiftRow,encode_div,encode_mod,(certificate.coverage u.1 hu.1 hu.2).2] at hrow
    rw [htable,Nat.add_sub_cancel] at hrow
    have hn : PrefixExtension.nextCoefficient (P.last u.1) u.2.val (P.low u.1)
        ((u.2.val+bit)/10) (ScalarClock.overflowValue (P.phase u.1)) bit = v.2.val := by
      rw [← hgamma]
      exact hnext.symm
    rw [hn] at hrow
    exact ⟨hbit,hrow (by omega) hv.1 hv.2 v.2.isLt⟩

end ScalarFinite

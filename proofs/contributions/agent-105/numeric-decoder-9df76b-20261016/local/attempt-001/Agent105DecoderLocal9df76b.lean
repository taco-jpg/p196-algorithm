import Std

/-!
Agent 105：有限双端扫描使用的精确局部解码器。
输入参数均可为任意自然数；有效边的两条完整等式与输出范围
决定唯一结果，不依赖调用者额外提供输入数位或输入进位界。
-/

namespace Agent105DecoderLocal9df76b

structure Edge where
  coeff : Nat
  low : Nat
  high : Nat
  deriving DecidableEq, BEq, Repr

def ValidEdge (u v a b : Nat) (E : Edge) : Prop :=
  E.coeff ≤ 18 ∧ E.low ≤ 1 ∧ E.high ≤ 1 ∧
    E.coeff + a = u + 10 * E.low ∧
    E.coeff + E.high = v + 10 * b

instance (u v a b : Nat) (E : Edge) : Decidable (ValidEdge u v a b E) := by
  unfold ValidEdge
  infer_instance

private def edgeCandidates (u a : Nat) : List Edge :=
  [⟨u - a, 0, 0⟩, ⟨u - a, 0, 1⟩,
   ⟨u + 10 - a, 1, 0⟩, ⟨u + 10 - a, 1, 1⟩]

/-- 只遍历四组输出进位；截断减法的候选仍必须通过完整等式检查。 -/
def decodePair (u v a b : Nat) : Option Edge :=
  (edgeCandidates u a).find? (fun E => decide (ValidEdge u v a b E))

def ValidCenter (u a b q : Nat) : Prop :=
  q ≤ 18 ∧ q % 2 = 0 ∧ q + a = u + 10 * b

instance (u a b q : Nat) : Decidable (ValidCenter u a b q) := by
  unfold ValidCenter
  infer_instance

def decodeCenter (u a b : Nat) : Option Nat :=
  let q := u + 10 * b - a
  if ValidCenter u a b q then some q else none

/-- 任意自然数输入下，两条列等式决定唯一有效边。 -/
theorem validEdge_unique {u v a b : Nat} {E F : Edge}
    (hE : ValidEdge u v a b E) (hF : ValidEdge u v a b F) : E = F := by
  rcases E with ⟨q, low, high⟩
  rcases F with ⟨r, low', high'⟩
  simp only [ValidEdge] at hE hF
  have hq : q = r := by omega
  have hl : low = low' := by omega
  have hh : high = high' := by omega
  subst r
  subst low'
  subst high'
  rfl

theorem validCenter_unique {u a b q r : Nat}
    (hq : ValidCenter u a b q) (hr : ValidCenter u a b r) : q = r := by
  have hqe := hq.2.2
  have hre := hr.2.2
  omega

private theorem validEdge_mem_candidates {u v a b : Nat} {E : Edge}
    (hE : ValidEdge u v a b E) : E ∈ edgeCandidates u a := by
  rcases E with ⟨q, low, high⟩
  simp only [ValidEdge] at hE
  simp only [edgeCandidates, List.mem_cons, List.not_mem_nil, or_false,
    Edge.mk.injEq]
  omega

theorem decodePair_sound {u v a b : Nat} {E : Edge}
    (h : decodePair u v a b = some E) : ValidEdge u v a b E := by
  change (edgeCandidates u a).find? (fun E => decide (ValidEdge u v a b E)) = some E at h
  simpa only [decide_eq_true_eq] using List.find?_some h

theorem decodePair_complete {u v a b : Nat} {E : Edge}
    (hE : ValidEdge u v a b E) : decodePair u v a b = some E := by
  cases h : decodePair u v a b with
  | none =>
      have hall : ∀ F ∈ edgeCandidates u a, ¬ decide (ValidEdge u v a b F) :=
        List.find?_eq_none.mp h
      have hbad := hall E (validEdge_mem_candidates hE)
      exact False.elim (hbad (by simpa only [decide_eq_true_eq] using hE))
  | some F =>
      have hF := decodePair_sound h
      have heq := validEdge_unique hF hE
      simpa only [heq] using h

/-- 完整规格；没有额外的输入范围假设。 -/
theorem decodePair_eq_some_iff {u v a b : Nat} {E : Edge} :
    decodePair u v a b = some E ↔ ValidEdge u v a b E :=
  ⟨decodePair_sound, decodePair_complete⟩

theorem decodeCenter_eq_some_iff {u a b q : Nat} :
    decodeCenter u a b = some q ↔ ValidCenter u a b q := by
  constructor
  · intro h
    unfold decodeCenter at h
    split at h
    · rename_i hvalid
      have heq := Option.some.inj h
      simpa only [heq] using hvalid
    · cases h
  · intro hq
    have heq : u + 10 * b - a = q := by
      have h := hq.2.2
      omega
    simp only [decodeCenter, heq, if_pos hq]

theorem decodePair_eq_none_iff {u v a b : Nat} :
    decodePair u v a b = none ↔ ¬ ∃ E, ValidEdge u v a b E := by
  constructor
  · intro hnone ⟨E, hE⟩
    have hsome := decodePair_complete hE
    rw [hnone] at hsome
    cases hsome
  · intro hnone
    cases h : decodePair u v a b with
    | none => rfl
    | some E => exact False.elim (hnone ⟨E, decodePair_sound h⟩)

theorem decodeCenter_eq_none_iff {u a b : Nat} :
    decodeCenter u a b = none ↔ ¬ ∃ q, ValidCenter u a b q := by
  constructor
  · intro hnone ⟨q, hq⟩
    have hsome := decodeCenter_eq_some_iff.mpr hq
    rw [hnone] at hsome
    cases hsome
  · intro hnone
    cases h : decodeCenter u a b with
    | none => rfl
    | some q => exact False.elim (hnone ⟨q, decodeCenter_eq_some_iff.mp h⟩)

#print axioms validEdge_unique
#print axioms validCenter_unique
#print axioms decodePair_sound
#print axioms decodePair_complete
#print axioms decodePair_eq_some_iff
#print axioms decodeCenter_eq_some_iff
#print axioms decodePair_eq_none_iff
#print axioms decodeCenter_eq_none_iff

end Agent105DecoderLocal9df76b

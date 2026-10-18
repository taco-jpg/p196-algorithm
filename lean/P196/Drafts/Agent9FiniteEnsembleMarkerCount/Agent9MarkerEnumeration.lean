import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9MarkerWords

/-! Complete digit-list enumeration for the complement of selected markers. -/

namespace P196.Agent9.Ensemble

open Agent101

def unmarkedPairs (r J q : Nat) : List (List (Nat × Nat)) :=
  blockChoices (goodBlocks r) (wordChoices pairAlphabet q) J

theorem unmarkedPairs_nodup (r J q : Nat) : (unmarkedPairs r J q).Nodup :=
  blockChoices_nodup _ _ r J (goodBlocks_nodup r)
    (wordChoices_nodup _ pairAlphabet_nodup q) (goodBlocks_word_length r)

theorem unmarkedPairs_word_length (r J q : Nat) (ps : List (Nat × Nat))
    (hp : ps ∈ unmarkedPairs r J q) : ps.length = J * r + q :=
  blockChoices_word_length _ _ r q J (goodBlocks_word_length r)
    (fun s hs => ((mem_wordChoices _ _ s).mp hs).1) ps hp

theorem unmarkedPairs_bounded (r J q : Nat) (ps : List (Nat × Nat))
    (hp : ps ∈ unmarkedPairs r J q) : ∀ p ∈ ps, p ∈ pairAlphabet := by
  induction J generalizing ps with
  | zero => exact ((mem_wordChoices _ _ ps).mp hp).2
  | succ J ih =>
    obtain ⟨b, hb, s, hs, rfl⟩ := (mem_appendProduct _ _ ps).mp hp
    intro p hpm
    rcases List.mem_append.mp hpm with hpb | hps
    · exact ((mem_goodBlocks r b).mp hb).2.1 p hpb
    · exact ih s hs p hps

theorem length_unmarkedPairs (r J q : Nat) :
    (unmarkedPairs r J q).length = (10 ^ (2 * r) - 1) ^ J * 100 ^ q := by
  rw [unmarkedPairs, length_blockChoices, length_goodBlocks, length_wordChoices,
    length_pairAlphabet]

theorem mem_unmarkedPairs (r J q : Nat) (ps : List (Nat × Nat)) :
    ps ∈ unmarkedPairs r J q ↔ ps.length = J * r + q ∧
      (∀ p ∈ ps, p ∈ pairAlphabet) ∧
      ∀ j, j < J → (ps.drop (j * r)).take r ≠ List.replicate r (9, 9) := by
  have hmem := mem_blockChoices (goodBlocks r) (wordChoices pairAlphabet q)
    r q J (goodBlocks_word_length r)
    (fun s hs => ((mem_wordChoices _ _ s).mp hs).1) ps
  constructor
  · intro hp
    obtain ⟨hlen, _, hblocks⟩ := hmem.mp hp
    exact ⟨hlen, unmarkedPairs_bounded r J q ps hp,
      fun j hj => ((mem_goodBlocks r _).mp (hblocks j hj)).2.2⟩
  · rintro ⟨hlen, hb, hblocks⟩
    apply hmem.mpr
    refine ⟨hlen, ?_, ?_⟩
    · apply (mem_wordChoices _ _ _).mpr
      refine ⟨by rw [List.length_drop, hlen]; omega, ?_⟩
      exact fun p hp => hb p (List.mem_of_mem_drop hp)
    · intro j hj
      have hbound := Nat.mul_le_mul_right r (show j + 1 ≤ J by omega)
      rw [Nat.succ_mul] at hbound
      apply (mem_goodBlocks r _).mpr
      refine ⟨?_, ?_, hblocks j hj⟩
      · simp only [List.length_take, List.length_drop, hlen]
        omega
      · exact fun p hp => hb p (List.mem_of_mem_drop (List.mem_of_mem_take hp))

def frameChoices (r J q : Nat) : List (List (Nat × Nat)) :=
  outerAlphabet.flatMap fun p => (unmarkedPairs r J q).map (p :: ·)

theorem mem_frameChoices (r J q : Nat) (ps : List (Nat × Nat)) :
    ps ∈ frameChoices r J q ↔ ∃ p ∈ outerAlphabet,
      ∃ qs ∈ unmarkedPairs r J q, p :: qs = ps := by
  simp [frameChoices, List.mem_flatMap, List.mem_map]

theorem frameChoices_nodup (r J q : Nat) : (frameChoices r J q).Nodup :=
  nodup_flatMap_map _ _ _ outerAlphabet_nodup (unmarkedPairs_nodup r J q)
    (fun _ _ _ _ _ _ _ _ h => List.cons.inj h)

theorem frameChoices_word_length (r J q : Nat) (ps : List (Nat × Nat))
    (hp : ps ∈ frameChoices r J q) : ps.length = J * r + q + 1 := by
  obtain ⟨p, _, qs, hq, rfl⟩ := (mem_frameChoices r J q ps).mp hp
  simp [unmarkedPairs_word_length r J q qs hq]

theorem length_frameChoices (r J q : Nat) :
    (frameChoices r J q).length = 90 * ((10 ^ (2 * r) - 1) ^ J * 100 ^ q) := by
  rw [frameChoices, length_flatMap_map, length_outerAlphabet, length_unmarkedPairs]

def markerWords (r J q e : Nat) : List (List Nat) :=
  wrappedPairsProduct (frameChoices r J q) (wordChoices (List.range 10) e)

theorem markerWords_nodup (r J q e : Nat) : (markerWords r J q e).Nodup :=
  wrappedPairsProduct_nodup _ _ (J * r + q + 1) (frameChoices_nodup r J q)
    (wordChoices_nodup _ List.nodup_range e) (frameChoices_word_length r J q)

theorem length_markerWords (r J q e : Nat) :
    (markerWords r J q e).length =
      90 * ((10 ^ (2 * r) - 1) ^ J * 100 ^ q) * 10 ^ e := by
  rw [markerWords, length_wrappedPairsProduct, length_frameChoices, length_wordChoices,
    List.length_range]

theorem mem_markerWords_repr (r J q e : Nat) (ds : List Nat) :
    ds ∈ markerWords r J q e ↔ ∃ ps ∈ frameChoices r J q,
      ∃ cs ∈ wordChoices (List.range 10) e, wrapPairs ps cs = ds := by
  simp [markerWords, wrappedPairsProduct, List.mem_flatMap, List.mem_map]

theorem markerWords_word_length (r J q e : Nat) (ds : List Nat)
    (hd : ds ∈ markerWords r J q e) : ds.length = 2 * (J * r + q + 1) + e := by
  obtain ⟨ps, hp, cs, hc, rfl⟩ := (mem_markerWords_repr r J q e ds).mp hd
  rw [length_wrapPairs, frameChoices_word_length r J q ps hp,
    ((mem_wordChoices _ _ cs).mp hc).1]

theorem markerWords_canonical (r J q e : Nat) (ds : List Nat)
    (hd : ds ∈ markerWords r J q e) : canonicalDigits ds := by
  obtain ⟨ps, hp, cs, hc, rfl⟩ := (mem_markerWords_repr r J q e ds).mp hd
  obtain ⟨p, hpo, qs, hq, rfl⟩ := (mem_frameChoices r J q ps).mp hp
  obtain ⟨ha, hb, hpos⟩ := (mem_outerAlphabet p).mp hpo
  apply (canonicalDigits_wrapDigits _ _ _).mpr
  refine ⟨ha, (digitsBounded_wrapPairs qs cs).mpr ⟨unmarkedPairs_bounded r J q qs hq, ?_⟩,
    hb, hpos⟩
  intro a ham
  have hh := ((mem_wordChoices _ _ cs).mp hc).2 a ham
  simpa only [List.mem_range, Nat.lt_succ_iff] using hh

theorem ninesChunk_iff (ps : List (Nat × Nat)) (a r : Nat)
    (har : a + r ≤ ps.length) :
    (ps.drop a).take r = List.replicate r (9, 9) ↔
      ∀ i, (hi : i < r) → ps[a + i]'(by omega) = (9, 9) := by
  constructor
  · intro h i hi
    have he := congrArg (fun xs : List (Nat × Nat) => xs[i]?) h
    simpa [List.getElem?_take, List.getElem?_drop, hi,
      List.getElem?_eq_getElem (show a + i < ps.length by omega)] using he
  · intro h
    have hlen : ((ps.drop a).take r).length = (List.replicate r (9, 9)).length := by
      simp only [List.length_take, List.length_drop, List.length_replicate]
      omega
    apply List.ext_getElem hlen
    intro i hi hj
    have hir : i < r := by simpa only [List.length_replicate] using hj
    simpa only [List.getElem_take, List.getElem_drop, List.getElem_replicate] using h i hir

/-- The selected paired positions all contain nine, using finite decimal digits. -/
def WordMarker (ds : List Nat) (a r : Nat) : Prop :=
  ∀ i, i < r → ds[a + i]?.getD 0 = 9 ∧ ds[ds.length - 1 - (a + i)]?.getD 0 = 9

theorem wrapPairs_wordMarker_iff (ps : List (Nat × Nat)) (cs : List Nat) (a r : Nat)
    (har : a + r ≤ ps.length) :
    WordMarker (wrapPairs ps cs) a r ↔
      (ps.drop a).take r = List.replicate r (9, 9) := by
  rw [ninesChunk_iff ps a r har]
  constructor
  · intro h i hi
    have hm := h i hi
    rw [wrapPairs_low ps cs (a + i) (by omega), wrapPairs_high ps cs (a + i) (by omega)] at hm
    exact Prod.ext hm.1 hm.2
  · intro h i hi
    rw [wrapPairs_low ps cs (a + i) (by omega), wrapPairs_high ps cs (a + i) (by omega)]
    have he := h i hi
    exact ⟨congrArg Prod.fst he, congrArg Prod.snd he⟩

/-- All canonical words of the stated width satisfying exactly the selected
marker-complement condition. No restricted digit-split subfamily remains. -/
theorem mem_markerWords (r J q e : Nat) (ds : List Nat) :
    ds ∈ markerWords r J q e ↔
      canonicalDigits ds ∧ ds.length = 2 * (J * r + q + 1) + e ∧
      ∀ j, j < J → ¬ WordMarker ds (1 + j * r) r := by
  constructor
  · intro hd
    refine ⟨markerWords_canonical r J q e ds hd,
      markerWords_word_length r J q e ds hd, ?_⟩
    obtain ⟨ps, hp, cs, _, rfl⟩ := (mem_markerWords_repr r J q e ds).mp hd
    obtain ⟨p, _, qs, hq, rfl⟩ := (mem_frameChoices r J q ps).mp hp
    obtain ⟨hql, _, hmarks⟩ := (mem_unmarkedPairs r J q qs).mp hq
    intro j hj hm
    have hbound := Nat.mul_le_mul_right r (show j + 1 ≤ J by omega)
    rw [Nat.succ_mul] at hbound
    have he := (wrapPairs_wordMarker_iff (p :: qs) cs (1 + j * r) r
      (by simp only [List.length_cons, hql]; omega)).mp hm
    apply hmarks j hj
    simpa only [Nat.add_comm 1, List.drop_succ_cons] using he
  · rintro ⟨hc, hlen, hmarks⟩
    obtain ⟨ps, cs, hpl, hcl, rfl⟩ := exists_wrapPairs ds (J * r + q + 1) e hlen
    cases ps with
    | nil => simp at hpl
    | cons p ps =>
      have hpsl : ps.length = J * r + q := by simpa using hpl
      obtain ⟨ha, hb, hz, hpos⟩ := (canonicalDigits_wrapDigits p.1 p.2 (wrapPairs ps cs)).mp hc
      obtain ⟨hpsb, hcsb⟩ := (digitsBounded_wrapPairs ps cs).mp hb
      have hpm : ps ∈ unmarkedPairs r J q := by
        apply (mem_unmarkedPairs r J q ps).mpr
        refine ⟨hpsl, hpsb, ?_⟩
        intro j hj he
        apply hmarks j hj
        have hbound := Nat.mul_le_mul_right r (show j + 1 ≤ J by omega)
        rw [Nat.succ_mul] at hbound
        apply (wrapPairs_wordMarker_iff (p :: ps) cs (1 + j * r) r
          (by simp only [List.length_cons, hpsl]; omega)).mpr
        simpa only [Nat.add_comm 1, List.drop_succ_cons] using he
      apply (mem_markerWords_repr r J q e _).mpr
      refine ⟨p :: ps, (mem_frameChoices r J q _).mpr ?_, cs, ?_, rfl⟩
      · exact ⟨p, (mem_outerAlphabet p).mpr ⟨ha, hz, hpos⟩, ps, hpm, rfl⟩
      · apply (mem_wordChoices _ _ cs).mpr
        exact ⟨hcl, fun a ham => List.mem_range.mpr (by have hh := hcsb a ham; omega)⟩

end P196.Agent9.Ensemble

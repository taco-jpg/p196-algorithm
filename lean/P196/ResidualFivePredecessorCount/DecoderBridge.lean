import P196.Agent105NumericDecoder.Agent105NumericDecoder9df76b
import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveFibers

/-!
# Positive predecessors in the residual-five fiber

The executable test checks the only two possible predecessor widths. Its
semantics comes from the existing numerical decoder and actual-width theorem.
Filtering the original canonical digit enumeration therefore retains exactly
the fiber members that have a positive ordinary reverse-and-add predecessor.
No bounded numerical search, new carry algorithm, or infinite-orbit claim is
used here.
-/

namespace P196.ResidualFivePredecessorCount

open DecimalDigits Lychrel196

/-- Test both possible source widths of a canonical decimal target. -/
def hasPositivePredecessorB (ds : List Nat) : Bool :=
  (Agent105NumericDecoder9df76b.decodeNumerical
    (Agent101.digitFn ds) ds.length ds.length).isSome ||
  (Agent105NumericDecoder9df76b.decodeNumerical
    (Agent101.digitFn ds) ds.length (ds.length - 1)).isSome

/-- The two-width Boolean test is complete for every canonical target list,
including one-digit targets, where the shorter candidate width is zero. -/
theorem hasPositivePredecessorB_iff (ds : List Nat)
    (hd : Agent101.canonicalDigits ds) :
    hasPositivePredecessorB ds = true ↔
      ∃ m, 0 < m ∧ step m = Agent101.natValue ds := by
  have htarget := (Agent101.canonicalDigits_iff ds).mp hd
  unfold hasPositivePredecessorB
  rw [Bool.or_eq_true,
    Agent105NumericDecoder9df76b.decodeNumerical_isSome_iff
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length ds.length htarget,
    Agent105NumericDecoder9df76b.decodeNumerical_isSome_iff
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length (ds.length - 1) htarget]
  constructor
  · rintro (⟨m, d, hm, _, hs⟩ | ⟨m, d, hm, _, hs⟩)
    · exact ⟨m, hm, hs⟩
    · exact ⟨m, hm, hs⟩
  · rintro ⟨m, hm, hs⟩
    obtain ⟨d, L, hsource⟩ := canonical_exists m hm
    have hout : Canonical (step m) (Agent101.digitFn ds) ds.length := by
      simpa only [hs] using htarget
    rcases Agent105WidthSupport9df76b.step_width_cases hsource hout with
      ⟨hwidth, _⟩ | ⟨hwidth, _⟩
    · left
      exact ⟨m, d, hm, by simpa only [hwidth] using hsource, hs⟩
    · right
      have hshort : ds.length - 1 = L := by omega
      exact ⟨m, d, hm, by simpa only [hshort] using hsource, hs⟩

/-- Retain the original canonical digit words with a positive predecessor. -/
def survivorWords (r : Nat) : List (List Nat) :=
  (Agent101.canonicalWords (Agent103.ResidualFiveFibers.half r) none).filter
    hasPositivePredecessorB

/-- Ordinary integer values of the retained canonical words. -/
def survivors (r : Nat) : List Nat :=
  (survivorWords r).map Agent101.natValue

/-- Exact digit-list membership, preserving the original enumeration. -/
theorem mem_survivorWords (r : Nat) (ds : List Nat) :
    ds ∈ survivorWords r ↔
      ds ∈ Agent101.canonicalWords (Agent103.ResidualFiveFibers.half r) none ∧
      ∃ m, 0 < m ∧ step m = Agent101.natValue ds := by
  simp only [survivorWords, List.mem_filter]
  constructor
  · rintro ⟨hmem, hsuccess⟩
    have hd := ((Agent101.mem_canonicalWords
      (Agent103.ResidualFiveFibers.half r) none ds).mp hmem).1
    exact ⟨hmem, (hasPositivePredecessorB_iff ds hd).mp hsuccess⟩
  · rintro ⟨hmem, hpredecessor⟩
    have hd := ((Agent101.mem_canonicalWords
      (Agent103.ResidualFiveFibers.half r) none ds).mp hmem).1
    exact ⟨hmem, (hasPositivePredecessorB_iff ds hd).mpr hpredecessor⟩

/-- Every retained word is an ordinary positive canonical decimal numeral. -/
theorem survivorWords_canonical (r : Nat) (ds : List Nat)
    (hds : ds ∈ survivorWords r) : Agent101.canonicalDigits ds := by
  have hmem := ((mem_survivorWords r ds).mp hds).1
  exact ((Agent101.mem_canonicalWords
    (Agent103.ResidualFiveFibers.half r) none ds).mp hmem).1

/-- The original integer fiber is filtered by the existence of an actual
positive predecessor, without any prescribed source-width restriction. -/
theorem mem_survivors (r n : Nat) :
    n ∈ survivors r ↔
      n ∈ Agent103.ResidualFiveFibers.fiber r ∧
      ∃ m, 0 < m ∧ step m = n := by
  constructor
  · intro hn
    obtain ⟨ds, hds, rfl⟩ := List.mem_map.mp hn
    obtain ⟨hmem, hpredecessor⟩ := (mem_survivorWords r ds).mp hds
    refine ⟨?_, hpredecessor⟩
    change Agent101.natValue ds ∈
      (Agent101.canonicalWords (Agent103.ResidualFiveFibers.half r) none).map
        Agent101.natValue
    exact List.mem_map.mpr ⟨ds, hmem, rfl⟩
  · rintro ⟨hmem, hpredecessor⟩
    change n ∈
      (Agent101.canonicalWords (Agent103.ResidualFiveFibers.half r) none).map
        Agent101.natValue at hmem
    obtain ⟨ds, hds, hvalue⟩ := List.mem_map.mp hmem
    apply List.mem_map.mpr
    refine ⟨ds, (mem_survivorWords r ds).mpr ⟨hds, ?_⟩, hvalue⟩
    simpa only [hvalue] using hpredecessor

/-- Filtering does not introduce repeated digit words. -/
theorem survivorWords_nodup (r : Nat) : (survivorWords r).Nodup :=
  (Agent101.canonicalWords_nodup
    (Agent103.ResidualFiveFibers.half r) none).filter hasPositivePredecessorB

/-- Every ordinary integer is counted once, using canonical-digit injectivity. -/
theorem survivors_nodup (r : Nat) : (survivors r).Nodup := by
  exact Agent101.nodup_map_natValue (survivorWords r)
    (survivorWords_canonical r) (survivorWords_nodup r)

/-- Counting retained words counts their ordinary integer values exactly. -/
theorem survivors_length_eq_words (r : Nat) :
    (survivors r).length = (survivorWords r).length := by
  simp only [survivors, List.length_map]

#print axioms hasPositivePredecessorB_iff
#print axioms mem_survivorWords
#print axioms survivorWords_canonical
#print axioms mem_survivors
#print axioms survivorWords_nodup
#print axioms survivors_nodup
#print axioms survivors_length_eq_words

end P196.ResidualFivePredecessorCount

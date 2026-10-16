import Agent102RunDefs

/-!
Agent #102：逐段展开词的区间语义。
这些结论只使用字面拼接，不要求段长为正，也不要求相邻数字不同。
所有区间均采用左闭右开的自然数端点。
-/

namespace Agent102

@[simp] theorem word_nil : word [] = [] := rfl

@[simp] theorem word_cons (r : Run) (rs : List Run) :
    word (r :: rs) = List.replicate r.count r.digit ++ word rs := by
  simp [word]

@[simp] theorem word_append (rs ts : List Run) :
    word (rs ++ ts) = word rs ++ word ts := by
  simp [word]

theorem word_length (rs : List Run) :
    (word rs).length = (rs.map Run.count).sum := by
  simp [word]

theorem word_reverse (rs : List Run) :
    word rs.reverse = (word rs).reverse := by
  simp only [word, List.flatMap_reverse, Function.comp_def, List.reverse_replicate]

/-- 同时平移左右端点，保持区间数字。 -/
def Span.shift (s : Span) (offset : Nat) : Span :=
  ⟨s.digit, s.lo + offset, s.hi + offset⟩

@[simp] theorem Span.shift_covers (s : Span) (offset i : Nat) :
    (s.shift offset).covers (i + offset) ↔ s.covers i := by
  simp [Span.shift, Span.covers]

@[simp] theorem Span.shift_overlaps (s t : Span) (offset : Nat) :
    (s.shift offset).overlaps (t.shift offset) ↔ s.overlaps t := by
  simp [Span.shift, Span.overlaps]

theorem spansFrom_shift (rs : List Run) (start offset : Nat) :
    spansFrom (start + offset) rs =
      (spansFrom start rs).map (fun s => s.shift offset) := by
  induction rs generalizing start with
  | nil => rfl
  | cons r rs ih =>
      simp only [spansFrom, List.map_cons, Span.shift]
      have heq : start + offset + r.count = start + r.count + offset := by omega
      rw [heq, ih]

theorem spansFrom_eq_map_spans (rs : List Run) (start : Nat) :
    spansFrom start rs = (spans rs).map (fun s => s.shift start) := by
  simpa only [Nat.zero_add, spans] using spansFrom_shift rs 0 start

theorem spansFrom_append (rs ts : List Run) (start : Nat) :
    spansFrom start (rs ++ ts) =
      spansFrom start rs ++ spansFrom (start + (word rs).length) ts := by
  induction rs generalizing start with
  | nil => simp [spansFrom]
  | cons r rs ih => simp [spansFrom, ih, Nat.add_assoc]

@[simp] theorem length_spansFrom (rs : List Run) (start : Nat) :
    (spansFrom start rs).length = rs.length := by
  induction rs generalizing start with
  | nil => rfl
  | cons r rs ih => simp [spansFrom, ih]

@[simp] theorem length_spans (rs : List Run) : (spans rs).length = rs.length := by
  simp [spans]

/-- 属于区间表的每段均位于整个展开词的端点之间。 -/
theorem mem_spansFrom_bounds {rs : List Run} {start : Nat} {s : Span}
    (hs : s ∈ spansFrom start rs) :
    start ≤ s.lo ∧ s.lo ≤ s.hi ∧ s.hi ≤ start + (word rs).length := by
  induction rs generalizing start with
  | nil => simp [spansFrom] at hs
  | cons r rs ih =>
      simp only [spansFrom, List.mem_cons] at hs
      simp only [word_cons, List.length_append, List.length_replicate]
      rcases hs with rfl | hs
      · simp only
        omega
      · have hb := ih hs
        omega

/-- 从任意起点开始，词内每个自然数位置都由某一段覆盖。 -/
theorem exists_mem_spansFrom_covers {rs : List Run} {start i : Nat}
    (hstart : start ≤ i) (hi : i < start + (word rs).length) :
    ∃ s ∈ spansFrom start rs, s.covers i := by
  induction rs generalizing start with
  | nil => simp only [word_nil, List.length_nil, Nat.add_zero] at hi; omega
  | cons r rs ih =>
      have hi' : i < (start + r.count) + (word rs).length := by
        simpa only [word_cons, List.length_append, List.length_replicate,
          Nat.add_assoc] using hi
      by_cases hfront : i < start + r.count
      · refine ⟨⟨r.digit, start, start + r.count⟩, ?_, hstart, hfront⟩
        simp [spansFrom]
      · obtain ⟨s, hs, hcov⟩ := ih (by omega) hi'
        refine ⟨s, ?_, hcov⟩
        simp only [spansFrom, List.mem_cons]
        exact Or.inr hs

/-- 区间覆盖的并集精确等于整个展开词占用的半开区间。 -/
theorem exists_mem_spansFrom_covers_iff (rs : List Run) (start i : Nat) :
    (∃ s ∈ spansFrom start rs, s.covers i) ↔
      start ≤ i ∧ i < start + (word rs).length := by
  constructor
  · rintro ⟨s, hs, hlo, hhi⟩
    have hb := mem_spansFrom_bounds hs
    omega
  · rintro ⟨hstart, hi⟩
    exact exists_mem_spansFrom_covers hstart hi

theorem mem_spans_bounds {rs : List Run} {s : Span} (hs : s ∈ spans rs) :
    s.lo ≤ s.hi ∧ s.hi ≤ (word rs).length := by
  have hb := mem_spansFrom_bounds (start := 0) hs
  simpa only [Nat.zero_add] using hb.2

theorem exists_mem_spans_covers {rs : List Run} {i : Nat}
    (hi : i < (word rs).length) : ∃ s ∈ spans rs, s.covers i := by
  exact exists_mem_spansFrom_covers (Nat.zero_le i) (by simpa using hi)

theorem exists_mem_spans_covers_iff (rs : List Run) (i : Nat) :
    (∃ s ∈ spans rs, s.covers i) ↔ i < (word rs).length := by
  simpa only [spans, Nat.zero_le, true_and, Nat.zero_add]
    using exists_mem_spansFrom_covers_iff rs 0 i

/-- 同一个区间表中，覆盖给定位置的区间唯一。 -/
theorem eq_of_mem_spansFrom_covers {rs : List Run} {start i : Nat} {s t : Span}
    (hs : s ∈ spansFrom start rs) (ht : t ∈ spansFrom start rs)
    (hsi : s.covers i) (hti : t.covers i) : s = t := by
  induction rs generalizing start with
  | nil => simp [spansFrom] at hs
  | cons r rs ih =>
      simp only [spansFrom, List.mem_cons] at hs ht
      rcases hs with rfl | hs
      · rcases ht with rfl | ht
        · rfl
        · have hb := mem_spansFrom_bounds ht
          have his : i < start + r.count := hsi.2
          have hit : t.lo ≤ i := hti.1
          omega
      · rcases ht with rfl | ht
        · have hb := mem_spansFrom_bounds hs
          have his : s.lo ≤ i := hsi.1
          have hit : i < start + r.count := hti.2
          omega
        · exact ih hs ht

theorem eq_of_mem_spans_covers {rs : List Run} {i : Nat} {s t : Span}
    (hs : s ∈ spans rs) (ht : t ∈ spans rs)
    (hsi : s.covers i) (hti : t.covers i) : s = t :=
  eq_of_mem_spansFrom_covers hs ht hsi hti

/-- 绝对位置减去起点后，展开词中读出的值就是覆盖该位置的段数字。 -/
theorem getElem?_word_of_mem_spansFrom {rs : List Run} {start i : Nat} {s : Span}
    (hs : s ∈ spansFrom start rs) (hi : s.covers i) :
    (word rs)[i - start]? = some s.digit := by
  induction rs generalizing start with
  | nil => simp [spansFrom] at hs
  | cons r rs ih =>
      simp only [spansFrom, List.mem_cons] at hs
      rcases hs with rfl | hs
      · simp only [Span.covers] at hi
        rw [word_cons, List.getElem?_append_left
          (by simp only [List.length_replicate]; omega)]
        exact List.getElem?_replicate_of_lt (by omega)
      · have hb := mem_spansFrom_bounds hs
        have hlo : s.lo ≤ i := hi.1
        have hcount : r.count ≤ i - start := by omega
        rw [word_cons, List.getElem?_append_right
          (by simpa only [List.length_replicate] using hcount),
          List.length_replicate, Nat.sub_sub]
        exact ih hs

theorem getElem?_word_of_covers {rs : List Run} {s : Span} {i : Nat}
    (hs : s ∈ spans rs) (hi : s.covers i) :
    (word rs)[i]? = some s.digit := by
  simpa only [Nat.sub_zero]
    using getElem?_word_of_mem_spansFrom (start := 0) hs hi

/-- 正长度交叠等价于存在共同覆盖的自然数位置。 -/
theorem Span.overlaps_iff_exists_covers (s t : Span) :
    s.overlaps t ↔ ∃ i : Nat, s.covers i ∧ t.covers i := by
  constructor
  · intro h
    have hlt := Nat.lt_min.mp h
    exact ⟨max s.lo t.lo,
      ⟨Nat.le_max_left _ _, hlt.1⟩,
      ⟨Nat.le_max_right _ _, hlt.2⟩⟩
  · rintro ⟨i, hs, ht⟩
    have hmax : max s.lo t.lo ≤ i := Nat.max_le.mpr ⟨hs.1, ht.1⟩
    exact Nat.lt_min.mpr
      ⟨Nat.lt_of_le_of_lt hmax hs.2, Nat.lt_of_le_of_lt hmax ht.2⟩

theorem Span.overlaps_of_covers {s t : Span} {i : Nat}
    (hs : s.covers i) (ht : t.covers i) : s.overlaps t :=
  (Span.overlaps_iff_exists_covers s t).mpr ⟨i, hs, ht⟩

/-- 两个展开词相等，当且仅当总长相等且每对实际交叠段数字相等。 -/
theorem word_eq_iff_length_and_overlap_digits (A B : List Run) :
    word A = word B ↔
      (word A).length = (word B).length ∧
      ∀ s ∈ spans A, ∀ t ∈ spans B, s.overlaps t → s.digit = t.digit := by
  constructor
  · intro hw
    refine ⟨congrArg List.length hw, ?_⟩
    intro s hs t ht hover
    obtain ⟨i, hsi, hti⟩ := (Span.overlaps_iff_exists_covers s t).mp hover
    have ha := getElem?_word_of_covers hs hsi
    have hb := getElem?_word_of_covers ht hti
    rw [hw] at ha
    exact Option.some.inj (ha.symm.trans hb)
  · rintro ⟨hlen, hagree⟩
    apply List.ext_getElem?
    intro i
    by_cases hi : i < (word A).length
    · obtain ⟨s, hs, hsi⟩ := exists_mem_spans_covers hi
      obtain ⟨t, ht, hti⟩ := exists_mem_spans_covers (rs := B) (i := i) (by omega)
      calc
        (word A)[i]? = some s.digit := getElem?_word_of_covers hs hsi
        _ = some t.digit := by rw [hagree s hs t ht (Span.overlaps_of_covers hsi hti)]
        _ = (word B)[i]? := (getElem?_word_of_covers ht hti).symm
    · rw [List.getElem?_eq_none (by omega), List.getElem?_eq_none (by omega)]

theorem word_eq_iff_count_sum_and_overlap_digits (A B : List Run) :
    word A = word B ↔
      (A.map Run.count).sum = (B.map Run.count).sum ∧
      ∀ s ∈ spans A, ∀ t ∈ spans B, s.overlaps t → s.digit = t.digit := by
  simpa only [word_length] using word_eq_iff_length_and_overlap_digits A B

end Agent102

#print axioms Agent102.word_nil
#print axioms Agent102.word_cons
#print axioms Agent102.word_append
#print axioms Agent102.word_length
#print axioms Agent102.word_reverse
#print axioms Agent102.Span.shift_covers
#print axioms Agent102.Span.shift_overlaps
#print axioms Agent102.spansFrom_shift
#print axioms Agent102.spansFrom_eq_map_spans
#print axioms Agent102.spansFrom_append
#print axioms Agent102.length_spansFrom
#print axioms Agent102.length_spans
#print axioms Agent102.mem_spansFrom_bounds
#print axioms Agent102.exists_mem_spansFrom_covers
#print axioms Agent102.exists_mem_spansFrom_covers_iff
#print axioms Agent102.mem_spans_bounds
#print axioms Agent102.exists_mem_spans_covers
#print axioms Agent102.exists_mem_spans_covers_iff
#print axioms Agent102.eq_of_mem_spansFrom_covers
#print axioms Agent102.eq_of_mem_spans_covers
#print axioms Agent102.getElem?_word_of_mem_spansFrom
#print axioms Agent102.getElem?_word_of_covers
#print axioms Agent102.Span.overlaps_iff_exists_covers
#print axioms Agent102.Span.overlaps_of_covers
#print axioms Agent102.word_eq_iff_length_and_overlap_digits
#print axioms Agent102.word_eq_iff_count_sum_and_overlap_digits

import P196.Foundations.LychrelDigitSums

/-!
# Agent #113: an overflowing step cannot produce a small descending word

Written source: Lemma 1, second half, of
`proofs/chat-6acee928/originals/p196_thirteen_prefix_theorem.md`.

Let `n ≥ 1` digits `d` (each at most nine) overflow under reverse-and-add,
so the next canonical numeral is `extended (columnSum d n) n` of width
`n + 1`. If every pair sum of that next numeral is at most nine, then its
second pair sum is not smaller than its first. The proof is the 9-run carry
induction: the low carries are forced to one and the high carries to zero,
column by column, until they meet at column one.

No claim about 196 or decimal Lychrel existence is made here.
-/

namespace Agent113.TwoDigit

open DecimalDigits FoldedDecimal

theorem extended_columnSum (q : Nat → Nat) (n j : Nat) :
    columnSum (extended q n) (n + 1) j =
      extended q n j + extended q n (n - j) := by
  simp only [columnSum, reflected, show n + 1 - 1 - j = n - j by omega]

theorem overflow_not_descending (d : Nat → Nat) (n : Nat) (hn : 1 ≤ n)
    (hd : ∀ i, i < n → d i ≤ 9)
    (hc : carry (columnSum d n) n = 1)
    (hsmall : ∀ i, i < n + 1 →
      columnSum (extended (columnSum d n) n) (n + 1) i ≤ 9) :
    columnSum (extended (columnSum d n) n) (n + 1) 0 ≤
      columnSum (extended (columnSum d n) n) (n + 1) 1 := by
  -- Abbreviations as plain local functions.
  have hq18 : ∀ i, i < n → columnSum d n i ≤ 18 := columnSum_bounded d n hd
  have hcb := carry_bounded (columnSum d n) n hq18
  have hcol : ∀ i, output (columnSum d n) i + 10 * carry (columnSum d n) (i + 1) =
      columnSum d n i + carry (columnSum d n) i :=
    fun i => column_equation (columnSum d n) i
  have hsym : ∀ i, i < n → columnSum d n i = columnSum d n (n - 1 - i) :=
    columnSum_symmetric d n
  have hob : ∀ i, output (columnSum d n) i ≤ 9 := output_bounded (columnSum d n)
  have hm : ∀ i, i < n → extended (columnSum d n) n i = output (columnSum d n) i := by
    intro i hi; simp [extended, hi]
  have hmn : extended (columnSum d n) n n = 1 := by simp [extended, hc]
  have hQ := extended_columnSum (columnSum d n) n
  have hc0 : carry (columnSum d n) 0 = 0 := rfl
  -- Width one: the two pair sums of the two-digit successor coincide.
  by_cases h1 : n = 1
  · subst h1
    rw [hQ 0, hQ 1]
    simp only [Nat.sub_zero, Nat.sub_self]
    omega
  -- From now on n ≥ 2.
  have hn2 : 2 ≤ n := by omega
  -- First pair sum: output 0 + 1 ≤ 9.
  have hQ0 : columnSum (extended (columnSum d n) n) (n + 1) 0 =
      output (columnSum d n) 0 + 1 := by
    rw [hQ 0, hm 0 (by omega), Nat.sub_zero, hmn]
  have hQ1 : columnSum (extended (columnSum d n) n) (n + 1) 1 =
      output (columnSum d n) 1 + output (columnSum d n) (n - 1) := by
    rw [hQ 1, hm 1 (by omega), hm (n - 1) (by omega)]
  -- Suppose the word descends; derive a contradiction.
  apply Nat.not_lt.mp
  intro hdesc
  rw [hQ0, hQ1] at hdesc
  have hs0 := hsmall 0 (by omega)
  rw [hQ0] at hs0
  -- Column 0 and the top column n - 1.
  have hcol0 : output (columnSum d n) 0 + 10 * carry (columnSum d n) 1 =
      columnSum d n 0 + 0 := hcol 0
  have hcolTop := hcol (n - 1)
  rw [show n - 1 + 1 = n by omega, hc] at hcolTop
  have hsymTop : columnSum d n (n - 1) = columnSum d n 0 := by
    have := hsym 0 (by omega); rw [Nat.sub_zero] at this; exact this.symm
  rw [hsymTop] at hcolTop
  have hcTop := hcb (n - 1) (by omega)
  have hc1 := hcb 1 (by omega)
  have hq0 := hq18 0 (by omega)
  have ho0 := hob 0
  have ho1 := hob 1
  have hoTop := hob (n - 1)
  -- Base facts: carry 1 = 1, output 1 = 0, carry (n - 1) = 0.
  have hbase1 : carry (columnSum d n) 1 = 1 ∧ output (columnSum d n) 1 = 0 ∧
      carry (columnSum d n) (n - 1) = 0 := by
    omega
  obtain ⟨hcar1, hout1, hcarTop⟩ := hbase1
  -- The induction: q (j+1) = 9, carry (j+2) = 1, carry (n - (j+1)) = 0.
  have key : ∀ j, j + 2 ≤ n →
      columnSum d n (j + 1) = 9 ∧ carry (columnSum d n) (j + 2) = 1 ∧
        carry (columnSum d n) (n - (j + 1)) = 0 := by
    intro j
    induction j with
    | zero =>
      intro _
      show columnSum d n 1 = 9 ∧ carry (columnSum d n) 2 = 1 ∧
        carry (columnSum d n) (n - 1) = 0
      have hcolA : output (columnSum d n) 1 + 10 * carry (columnSum d n) 2 =
          columnSum d n 1 + carry (columnSum d n) 1 := hcol 1
      have hq1 := hq18 1 (by omega)
      have hc2 := hcb 2 (by omega)
      exact ⟨by omega, by omega, hcarTop⟩
    | succ j ih =>
      intro hj
      show columnSum d n (j + 2) = 9 ∧ carry (columnSum d n) (j + 3) = 1 ∧
        carry (columnSum d n) (n - (j + 2)) = 0
      obtain ⟨hqj, hcj, hcnj⟩ := ih (by omega)
      -- High column n - 1 - (j + 1): its pair sum is q (j + 1) = 9.
      have hsymj : columnSum d n (n - 1 - (j + 1)) = 9 := by
        rw [← hsym (j + 1) (by omega)]; exact hqj
      have hcolH := hcol (n - 1 - (j + 1))
      rw [show n - 1 - (j + 1) + 1 = n - (j + 1) by omega, hcnj, hsymj] at hcolH
      have hcH := hcb (n - 1 - (j + 1)) (by omega)
      have hoH := hob (n - 1 - (j + 1))
      have hcarH : carry (columnSum d n) (n - 1 - (j + 1)) = 0 := by omega
      have houtH : output (columnSum d n) (n - 1 - (j + 1)) = 9 := by omega
      -- The pair sum j + 2 of the successor is at most nine.
      have hsj := hsmall (j + 2) (by omega)
      rw [hQ (j + 2), hm (j + 2) (by omega), hm (n - (j + 2)) (by omega),
        show n - (j + 2) = n - 1 - (j + 1) by omega, houtH] at hsj
      have hout2 : output (columnSum d n) (j + 2) = 0 := by omega
      have hcolL : output (columnSum d n) (j + 2) +
          10 * carry (columnSum d n) (j + 3) =
          columnSum d n (j + 2) + carry (columnSum d n) (j + 2) := hcol (j + 2)
      rw [hcj, hout2] at hcolL
      have hq2 := hq18 (j + 2) (by omega)
      have hc3 := hcb (j + 3) (by omega)
      refine ⟨by omega, by omega, ?_⟩
      rw [show n - (j + 2) = n - 1 - (j + 1) by omega]
      exact hcarH
  -- At j = n - 2 the high-side carry is carry 1, which must be zero.
  obtain ⟨_, _, hlast⟩ := key (n - 2) (by omega)
  rw [show n - (n - 2 + 1) = 1 by omega] at hlast
  omega

#print axioms overflow_not_descending

end Agent113.TwoDigit

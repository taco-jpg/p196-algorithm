import P196.Sprint.Agent03.EnrichedNoGain
import P196.Agent117P2641.Agent124PrefixL
import P196.Agent117RemainingCycles.PrefixCycle
import P196.Agent124ForwardInvariant.Agent124Forward

/-!
# 196's prefix state lies on a cycle of the forward abstraction (sprint agent 03)

`Agent124.Forward.no_196_outside` excludes every `k`-digit word *outside* a
forward-closed set containing the width-`k` projection of `orbit 196 100`.
This file proves the matching limitation of the backward rank method
(`Agent124.PrefixR.RowsClosed`, used by every `no_196_of_entries` certificate):

* `rank_none_of_cycle`: if a word `w0` returns to itself under the forward
  prefix map (a forward walk of positive length), then **no** rank function
  satisfying `RowsClosed k` assigns a rank to `w0` or to any word forward-reachable
  from `w0`;
* for `k = 3, 4, 5, 6, 7` the projection of `orbit 196 100` does return to itself
  (explicit carry witnesses, 17 / 22 / 28 / 28 / 42 steps, kernel-checked), so
  every word of `Reach (wordPrefix q100 k)` is uncertifiable at width `k`
  (`no_rank_k`), and every batch entry `(pre, bound)` with such a `k`-digit
  `pre` fails `entryOK k R` (`entryOK_false_k`).

Together with `Agent124.Forward.no_196_outside` this says: at these widths every
`k`-digit word the backward route can certify at width `k` lies outside the
forward closure, so the forward route excludes it too (backward ⊆ forward).
The converse — that the two exclusion sets are *equal* — was only measured by
computation in `sprint/agent-03/REPORT.md`; it is not proved here.  The prefix
statements `entryOK_false_k` cover prefixes of length exactly `k`; shorter
prefixes at width `k` are not formalised here.

Nothing here proves or disproves any palindrome statement about 196.
-/

namespace Sprint.Agent03

open SevenColumnProjection SevenColumn SevenColumn.Certificate
open Agent124.PrefixR Agent124.PrefixK Agent124.PrefixL

/-! ## Basic facts about one forward step -/

theorem lowDigits_length' : ∀ (s : List Nat) (x : Nat), (lowDigits s x).length = s.length
  | [], _ => rfl
  | _ :: s, _ => by simp only [lowDigits, List.length_cons, lowDigits_length' s]

theorem highDigits_length' : ∀ (s : List Nat) (e : Nat), (highDigits s e).2.length = s.length
  | [], _ => rfl
  | _ :: s, e => by simp only [highDigits, List.length_cons, highDigits_length' s e]

theorem lowDigits_lt : ∀ (s : List Nat) (x : Nat), ∀ d ∈ lowDigits s x, d < 10
  | [], _, d, h => by simp [lowDigits] at h
  | a :: s, x, d, h => by
      simp only [lowDigits, List.mem_cons] at h
      rcases h with rfl | h
      · exact Nat.mod_lt _ (by decide)
      · exact lowDigits_lt s _ d h

theorem highDigits_lt : ∀ (s : List Nat) (e : Nat), ∀ d ∈ (highDigits s e).2, d < 10
  | [], _, d, h => by simp [highDigits] at h
  | a :: s, e, d, h => by
      simp only [highDigits, List.mem_cons] at h
      rcases h with rfl | h
      · exact Nat.mod_lt _ (by decide)
      · exact highDigits_lt s e d h

theorem zipWith_add_lt : ∀ (l m : List Nat), (∀ d ∈ l, d < 10) → (∀ d ∈ m, d < 10) →
    ∀ d ∈ List.zipWith (· + ·) l m, d < 19
  | [], _, _, _, d, h => by simp at h
  | _ :: _, [], _, _, d, h => by simp at h
  | a :: l, b :: m, hl, hm, d, h => by
      simp only [List.zipWith_cons_cons, List.mem_cons] at h
      rcases h with rfl | h
      · have := hl a (List.mem_cons_self ..)
        have := hm b (List.mem_cons_self ..)
        omega
      · exact zipWith_add_lt l m (fun x hx => hl x (List.mem_cons_of_mem _ hx))
          (fun x hx => hm x (List.mem_cons_of_mem _ hx)) d h

theorem fp_length (s : List Nat) (e : Nat) : (forwardPrefix s e).length = s.length := by
  unfold forwardPrefix
  dsimp only
  split
  · simp only [List.length_zipWith, lowDigits_length', highDigits_length', Nat.min_self]
  · simp only [List.length_zipWith, lowDigits_length', List.length_cons, highDigits_length']
    omega

theorem fp_lt19 (s : List Nat) (e : Nat) : ∀ d ∈ forwardPrefix s e, d < 19 := by
  unfold forwardPrefix
  dsimp only
  split
  · exact zipWith_add_lt _ _ (lowDigits_lt s 0) (highDigits_lt s e)
  · refine zipWith_add_lt _ _ (lowDigits_lt s 0) ?_
    intro d hd
    simp only [List.mem_cons] at hd
    rcases hd with rfl | hd
    · decide
    · exact highDigits_lt s e d hd

theorem fp_head_pos {a : Nat} {t : List Nat} {e : Nat} (ha : 0 < a)
    (ht : ∀ x ∈ t, x < 19) (he : e < 2) :
    0 < (forwardPrefix (a :: t) e).headD 0 := by
  have hc := Agent117.highDigits_carry_lt ht he
  unfold forwardPrefix
  rw [Agent117.highDigits_cons, Agent117.lowDigits_cons]
  dsimp only
  split
  · rename_i h
    simp only [List.zipWith_cons_cons, List.headD_cons]
    simp only [SevenColumn.carry, SevenColumn.lowDigit] at h ⊢
    omega
  · simp only [List.zipWith_cons_cons, List.headD_cons]
    omega

/-- Words handled by the rank machinery at width `k`. -/
def Good (k : Nat) (w : List Nat) : Prop :=
  w.length = k ∧ (∀ a ∈ w, a < 19) ∧ 0 < w.headD 0

theorem good_fp {k : Nat} {s : List Nat} {e : Nat} (hs : Good k s) (he : e < 2) :
    Good k (forwardPrefix s e) := by
  obtain ⟨hl, hlt, hpos⟩ := hs
  refine ⟨by rw [fp_length]; exact hl, fp_lt19 s e, ?_⟩
  cases s with
  | nil => simp at hpos
  | cons a t =>
      exact fp_head_pos (by simpa using hpos)
        (fun x hx => hlt x (List.mem_cons_of_mem _ hx)) he

/-! ## Forward walks and rank descent -/

/-- A forward walk of exactly `n` abstract steps. -/
inductive FPath (u : List Nat) : Nat → List Nat → Prop
  | refl : FPath u 0 u
  | step {n : Nat} {v : List Nat} (e : Nat) : e < 2 → FPath u n v →
      FPath u (n + 1) (forwardPrefix v e)

theorem good_of_fpath {k n : Nat} {u v : List Nat} (hu : Good k u) (p : FPath u n v) :
    Good k v := by
  induction p with
  | refl => exact hu
  | step e he _ ih => exact good_fp ih he

/-- Along a forward walk the rank of any `RowsClosed` function drops by at least
one per step when read backwards. -/
theorem rank_descent {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {n : Nat} {u v : List Nat} (hu : Good k u) (p : FPath u n v) :
    ∀ {r : Nat}, R v = some r → ∃ s, R u = some s ∧ s + n ≤ r := by
  induction p with
  | refl => intro r h; exact ⟨r, h, by omega⟩
  | @step n v e he p ih =>
      intro r hr
      have hv : Good k v := good_of_fpath hu p
      obtain ⟨hvl, hvlt, hvpos⟩ := hv
      have hW : (forwardPrefix v e).length = k := by rw [fp_length]; exact hvl
      have hmem : v ∈ longPred k (forwardPrefix v e) := by
        simp only [longPred, hW, if_true]
        exact Agent117.forwardPrefix_mem_prefixPredecessors hvlt hvpos he
      obtain ⟨s', hs', hlt⟩ := rows _ r (fp_lt19 v e) hr v hmem
      obtain ⟨s, hs, hle⟩ := ih hs'
      exact ⟨s, hs, by omega⟩

/-- A word on a forward cycle, and everything forward-reachable from it, has no
rank under any `RowsClosed` function. -/
theorem rank_none_of_cycle {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {w0 : List Nat} (h0 : Good k w0) {n : Nat} (hn : 0 < n) (cyc : FPath w0 n w0) :
    ∀ m w, FPath w0 m w → R w = none := by
  intro m w p
  cases hR : R w with
  | none => rfl
  | some r =>
      obtain ⟨s, hs, _⟩ := rank_descent rows h0 p hR
      obtain ⟨s', hs', hle⟩ := rank_descent rows h0 cyc hs
      rw [hs] at hs'
      cases hs'
      omega

theorem fpath_of_reach {w0 w : List Nat} (h : Reach w0 w) : ∃ n, FPath w0 n w := by
  induction h with
  | refl => exact ⟨0, FPath.refl⟩
  | step e he _ ih =>
      obtain ⟨n, p⟩ := ih
      exact ⟨n + 1, FPath.step e (by omega) p⟩

theorem no_rank_of_cycle_reach {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {w0 : List Nat} (h0 : Good k w0) {n : Nat} (hn : 0 < n) (cyc : FPath w0 n w0) :
    ∀ w, Reach w0 w → R w = none := by
  intro w h
  obtain ⟨m, p⟩ := fpath_of_reach h
  exact rank_none_of_cycle rows h0 hn cyc m w p

/-! ## Executable cycle witnesses -/

/-- Apply the forward prefix map with the listed carries, in order. -/
def run (w : List Nat) (es : List Nat) : List Nat := es.foldl (fun v e => forwardPrefix v e) w

theorem fpath_prepend {u : List Nat} {e : Nat} (he : e < 2) :
    ∀ {n : Nat} {v : List Nat}, FPath (forwardPrefix u e) n v → FPath u (n + 1) v := by
  intro n v p
  induction p with
  | refl => exact FPath.step e he FPath.refl
  | step e' he' _ ih => exact FPath.step e' he' ih

theorem fpath_run : ∀ (es : List Nat) (w : List Nat), (∀ e ∈ es, e < 2) →
    FPath w es.length (run w es)
  | [], w, _ => FPath.refl
  | e :: es, w, h => by
      have he : e < 2 := h e (List.mem_cons_self ..)
      have ih := fpath_run es (forwardPrefix w e) (fun x hx => h x (List.mem_cons_of_mem _ hx))
      simp only [run, List.foldl_cons, List.length_cons] at ih ⊢
      exact fpath_prepend he ih

/-- Packaged witness check. -/
def cycleOK (k : Nat) (w : List Nat) (es : List Nat) : Bool :=
  decide (w.length = k) && w.all (fun a => decide (a < 19)) && decide (0 < w.headD 0) &&
    decide (0 < es.length) && es.all (fun e => decide (e < 2)) && run w es == w

theorem cycleOK_sound {k : Nat} {w es : List Nat} (h : cycleOK k w es = true) :
    Good k w ∧ 0 < es.length ∧ FPath w es.length w := by
  unfold cycleOK at h
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at h
  obtain ⟨⟨⟨⟨⟨hl, hlt⟩, hpos⟩, hn⟩, hes⟩, hrun⟩ := h
  refine ⟨⟨hl, hlt, hpos⟩, hn, ?_⟩
  have := fpath_run es w hes
  rwa [hrun] at this

/-- Main generic endpoint: a verified cycle through `w0` makes every word of the
forward closure of `w0` uncertifiable at width `k`. -/
theorem no_rank_of_cycleOK {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {w0 es : List Nat} (h : cycleOK k w0 es = true) : ∀ w, Reach w0 w → R w = none := by
  obtain ⟨hg, hn, hc⟩ := cycleOK_sound h
  exact no_rank_of_cycle_reach rows hg hn hc

/-- At full width a `k`-digit prefix is its own only initial word. -/
theorem mem_initialWordsL_self {k : Nat} {pre : List Nat} (hlen : pre.length = k) :
    pre ∈ initialWordsL k pre := by
  unfold initialWordsL
  rw [List.mem_filter]
  refine ⟨?_, ?_⟩
  · rw [List.mem_flatMap]
    refine ⟨0, List.mem_range.mpr (by omega), ?_⟩
    simp [digitLists]
  · simp [initialOK, hlen]

/-- No batch entry `(pre, bound)` with a `k`-digit `pre` in the forward closure of a
cyclic word passes the width-`k` entry check, for any `RowsClosed` rank function. -/
theorem entryOK_false_of_cycleOK {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    {w0 es : List Nat} (h : cycleOK k w0 es = true) {pre : List Nat} (hlen : pre.length = k)
    (hreach : Reach w0 pre) (bound : Nat) : entryOK k R (pre, bound) = false := by
  have hnone := no_rank_of_cycleOK rows h pre hreach
  cases hc : entryOK k R (pre, bound) with
  | false => rfl
  | true =>
      exfalso
      unfold entryOK at hc
      simp only [Bool.and_eq_true] at hc
      have hall := List.all_eq_true.mp hc.2 pre (mem_initialWordsL_self hlen)
      simp only [hnone] at hall
      exact Bool.false_ne_true hall

/-! ## The 196 instances (k = 3 .. 7) -/

/-- Width-`k` projection of `orbit 196 100` (leading entries of the pair word `q100`). -/
def w100 : List Nat := [8, 8, 13, 9, 14, 14, 14]

theorem wordPrefix_q100 (k : Nat) (hk : k ≤ 7) :
    wordPrefix Agent124.Forward.q100 k = w100.take k := by
  have : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 ∨ k = 7 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- Carry witnesses of forward cycles through the projection (generated by
`sprint/agent-03/entry_and_cycle.py`, untrusted; checked by `decide`). -/
def cyc3 : List Nat := [0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1]
def cyc4 : List Nat := [1,0,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,1,1]
def cyc5 : List Nat := [0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1]
def cyc6 : List Nat := [0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1]
def cyc7 : List Nat :=
  [0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1]

theorem cyc3_ok : cycleOK 3 (w100.take 3) cyc3 = true := by decide +kernel
theorem cyc4_ok : cycleOK 4 (w100.take 4) cyc4 = true := by decide +kernel
theorem cyc5_ok : cycleOK 5 (w100.take 5) cyc5 = true := by decide +kernel
theorem cyc6_ok : cycleOK 6 (w100.take 6) cyc6 = true := by decide +kernel
theorem cyc7_ok : cycleOK 7 (w100.take 7) cyc7 = true := by decide +kernel

/-- Width 3: no word of the forward closure of 196's time-100 projection has a rank. -/
theorem no_rank_3 {R : List Nat → Option Nat} (rows : RowsClosed 3 R) :
    ∀ w, Reach (wordPrefix Agent124.Forward.q100 3) w → R w = none := by
  rw [wordPrefix_q100 3 (by omega)]; exact no_rank_of_cycleOK rows cyc3_ok

theorem no_rank_4 {R : List Nat → Option Nat} (rows : RowsClosed 4 R) :
    ∀ w, Reach (wordPrefix Agent124.Forward.q100 4) w → R w = none := by
  rw [wordPrefix_q100 4 (by omega)]; exact no_rank_of_cycleOK rows cyc4_ok

theorem no_rank_5 {R : List Nat → Option Nat} (rows : RowsClosed 5 R) :
    ∀ w, Reach (wordPrefix Agent124.Forward.q100 5) w → R w = none := by
  rw [wordPrefix_q100 5 (by omega)]; exact no_rank_of_cycleOK rows cyc5_ok

theorem no_rank_6 {R : List Nat → Option Nat} (rows : RowsClosed 6 R) :
    ∀ w, Reach (wordPrefix Agent124.Forward.q100 6) w → R w = none := by
  rw [wordPrefix_q100 6 (by omega)]; exact no_rank_of_cycleOK rows cyc6_ok

theorem no_rank_7 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    ∀ w, Reach (wordPrefix Agent124.Forward.q100 7) w → R w = none := by
  rw [wordPrefix_q100 7 (by omega)]; exact no_rank_of_cycleOK rows cyc7_ok

/-- Prefix form: a `k`-digit prefix in the forward closure can never be certified
by a width-`k` batch entry. -/
theorem entryOK_false_3 {R : List Nat → Option Nat} (rows : RowsClosed 3 R)
    {pre : List Nat} (hlen : pre.length = 3)
    (hreach : Reach (wordPrefix Agent124.Forward.q100 3) pre) (bound : Nat) :
    entryOK 3 R (pre, bound) = false := by
  rw [wordPrefix_q100 3 (by omega)] at hreach
  exact entryOK_false_of_cycleOK rows cyc3_ok hlen hreach bound

theorem entryOK_false_4 {R : List Nat → Option Nat} (rows : RowsClosed 4 R)
    {pre : List Nat} (hlen : pre.length = 4)
    (hreach : Reach (wordPrefix Agent124.Forward.q100 4) pre) (bound : Nat) :
    entryOK 4 R (pre, bound) = false := by
  rw [wordPrefix_q100 4 (by omega)] at hreach
  exact entryOK_false_of_cycleOK rows cyc4_ok hlen hreach bound

theorem entryOK_false_5 {R : List Nat → Option Nat} (rows : RowsClosed 5 R)
    {pre : List Nat} (hlen : pre.length = 5)
    (hreach : Reach (wordPrefix Agent124.Forward.q100 5) pre) (bound : Nat) :
    entryOK 5 R (pre, bound) = false := by
  rw [wordPrefix_q100 5 (by omega)] at hreach
  exact entryOK_false_of_cycleOK rows cyc5_ok hlen hreach bound

theorem entryOK_false_6 {R : List Nat → Option Nat} (rows : RowsClosed 6 R)
    {pre : List Nat} (hlen : pre.length = 6)
    (hreach : Reach (wordPrefix Agent124.Forward.q100 6) pre) (bound : Nat) :
    entryOK 6 R (pre, bound) = false := by
  rw [wordPrefix_q100 6 (by omega)] at hreach
  exact entryOK_false_of_cycleOK rows cyc6_ok hlen hreach bound

theorem entryOK_false_7 {R : List Nat → Option Nat} (rows : RowsClosed 7 R)
    {pre : List Nat} (hlen : pre.length = 7)
    (hreach : Reach (wordPrefix Agent124.Forward.q100 7) pre) (bound : Nat) :
    entryOK 7 R (pre, bound) = false := by
  rw [wordPrefix_q100 7 (by omega)] at hreach
  exact entryOK_false_of_cycleOK rows cyc7_ok hlen hreach bound

end Sprint.Agent03

#print axioms Sprint.Agent03.fp_head_pos
#print axioms Sprint.Agent03.rank_descent
#print axioms Sprint.Agent03.rank_none_of_cycle
#print axioms Sprint.Agent03.no_rank_of_cycleOK
#print axioms Sprint.Agent03.entryOK_false_of_cycleOK
#print axioms Sprint.Agent03.wordPrefix_q100
#print axioms Sprint.Agent03.no_rank_3
#print axioms Sprint.Agent03.no_rank_4
#print axioms Sprint.Agent03.no_rank_5
#print axioms Sprint.Agent03.no_rank_6
#print axioms Sprint.Agent03.entryOK_false_3
#print axioms Sprint.Agent03.entryOK_false_4
#print axioms Sprint.Agent03.entryOK_false_5
#print axioms Sprint.Agent03.entryOK_false_6
#print axioms Sprint.Agent03.no_rank_7
#print axioms Sprint.Agent03.entryOK_false_7

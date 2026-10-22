import P196.Sprint.Agent04.Trap

/-!
# Sprint agent 04: cycles of the width-7 abstraction realized by actual integers

`RealizedAt k n w e` says: `n` has canonical decimal digits `dg n` of width `wd n ≥ k`
(`DecimalDigits.Canonical`), its outer `k` column sums are `w`
(`SevenColumnProjection.wordPrefix (columnSum …) k`, the projection used by every prefix
certificate) and the actual low-scan carry into column `wd n - k` is `e` (the boundary carry that
`forwardPrefix` leaves free).

* `realized_10097`, `closedA`, `backA_ok`, `backA_words`: the width-7 words of `orbit 10097 t` for
  `t = 220 … 228` return to their start, and these eight actual steps (actual carries) are a closed
  walk of the abstraction.  Hence the realized word has no rank in any `RowsClosed 7` function.
* `realized_10151`, `backB_ok`, `backB_actual`, `trajectory_no_rank`: every width-7 word of
  `orbit 10151 t`, `t = 5 … 80`, lies in no `RowsClosed 7` rank function: the actual trajectory is a
  backward walk from `t = 80` to `t = 5`, continued by an abstract walk (63 steps) to the length-7 cycle.
  `trajectory_nodup`: these 76 words are pairwise distinct (no closed walk is realized on this stretch).
* `palindrome_81`: `orbit 10151 81` is a palindrome beginning 1337, so `no_certificate_1337_from_orbit`
  obtains the width-7 method limit for 1337 from the actual last predecessor word.

Nothing here is about 196, and a closed walk realized once is not an orbit that repeats forever.
-/

namespace Sprint04.Realized

open DecimalDigits Lychrel196 SevenColumn.Certificate Agent117
open Agent124.PrefixR Agent124.PrefixL Sprint04

/-- Little-endian decimal digits (fuel bounds the number of digits). -/
def digitsFuel : Nat → Nat → List Nat
  | 0, _ => []
  | f + 1, n => if n = 0 then [] else n % 10 :: digitsFuel f (n / 10)

def dg (n : Nat) (i : Nat) : Nat := (digitsFuel 512 n).getD i 0
def wd (n : Nat) : Nat := (digitsFuel 512 n).length

instance (n : Nat) (d : Nat → Nat) (L : Nat) : Decidable (Canonical n d L) :=
  inferInstanceAs (Decidable (0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧ 0 < d (L - 1) ∧ value d L = n))

/-- `n` is canonical with digits `dg n`, width at least `k`, outer `k`-column word `w`, and actual
carry `e` into column `wd n - k`. -/
def RealizedAt (k n : Nat) (w : List Nat) (e : Nat) : Prop :=
  Canonical n (dg n) (wd n) ∧ k ≤ wd n ∧
    SevenColumnProjection.wordPrefix (columnSum (dg n) (wd n)) k = w ∧
    DecimalDigits.carry (columnSum (dg n) (wd n)) (wd n - k) = e

instance (k n : Nat) (w : List Nat) (e : Nat) : Decidable (RealizedAt k n w e) :=
  inferInstanceAs (Decidable (Canonical n (dg n) (wd n) ∧ k ≤ wd n ∧
    SevenColumnProjection.wordPrefix (columnSum (dg n) (wd n)) k = w ∧
    DecimalDigits.carry (columnSum (dg n) (wd n)) (wd n - k) = e))

/-! ## A closed walk realized by the orbit of 10097, t = 220 … 228 -/

def wordsA : List (List Nat) := [[8, 14, 8, 4, 3, 2, 9], [17, 8, 17, 8, 6, 5, 9], [8, 16, 16, 16, 14, 11, 15], [17, 13, 14, 14, 10, 4, 11], [8, 12, 9, 10, 6, 5, 6], [17, 5, 0, 1, 13, 10, 12], [8, 13, 5, 1, 5, 5, 4], [17, 6, 11, 2, 10, 10, 8], [8, 14, 8, 4, 3, 2, 9]]
def carriesA : List Nat := [1, 1, 0, 0, 0, 1, 0, 1, 0]

theorem realized_10097 : ∀ i, i < 9 →
    RealizedAt 7 (orbit 10097 (220 + i)) (wordsA.getD i []) (carriesA.getD i 0) := by
  decide +kernel

theorem closedA : wordsA.getD 8 [] = wordsA.getD 0 [] := by decide +kernel

/-- Backward closed walk `w228 ← w227 ← … ← w220` (packed by `Agent117.unpack 7`). -/
def backAData : List Nat := [804898137, 402449086, 1182025413, 591019564, 1057627282, 1469731260, 873273057, 857573377]
def backA : List (List Nat × Nat) := backAData.map (unpack 7)

theorem backA_words :
    backA = (List.range 8).reverse.map (fun i => (wordsA.getD i [], carriesA.getD i 0)) := by
  decide +kernel
theorem backA_ok : walkOKk 7 ((wordsA.getD 8 [], 0) :: backA) = true := by decide +kernel
theorem backA_end : (backA.getLastD (wordsA.getD 8 [], 0)).1 = wordsA.getD 8 [] := by
  decide +kernel

/-- The word realized at `t = 220` (and `t = 228`) has no rank in any `RowsClosed 7` function. -/
theorem realized_10097_no_rank {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R (wordsA.getD 0 []) = none := by
  rw [← closedA]
  exact R_none_of_walks rows [] backA (wordsA.getD 8 []) (wordsA.getD 8 []) 0 0
    (by decide +kernel) rfl backA_ok backA_end (by decide +kernel)

/-! ## The orbit of 10151 inside the trap, t = 5 … 80, and the palindrome at t = 81 -/

def wordsB : List (List Nat) := [[10, 0, 2, 2, 2, 0, 10], [1, 1, 2, 4, 4, 2, 1], [2, 2, 4, 8, 8, 4, 2], [4, 4, 8, 16, 16, 8, 4], [8, 8, 17, 13, 13, 17, 8], [16, 17, 15, 8, 8, 15, 17], [7, 15, 14, 14, 16, 14, 14], [15, 11, 10, 10, 14, 10, 10], [6, 8, 3, 2, 6, 6, 2], [12, 16, 6, 4, 12, 12, 4], [3, 10, 13, 10, 7, 6, 7], [7, 1, 8, 1, 15, 12, 15], [14, 2, 16, 3, 11, 6, 11], [5, 7, 9, 10, 5, 8, 8], [10, 15, 9, 0, 11, 16, 16], [1, 7, 5, 10, 2, 9, 14], [2, 14, 11, 0, 6, 9, 8], [5, 9, 3, 1, 12, 18, 16], [10, 18, 6, 3, 5, 18, 14], [1, 10, 15, 9, 8, 14, 14], [3, 1, 11, 9, 18, 9, 10], [6, 3, 3, 0, 18, 0, 2], [12, 6, 6, 1, 16, 1, 4], [3, 9, 12, 7, 8, 8, 5], [7, 9, 4, 15, 16, 16, 10], [14, 18, 9, 11, 14, 14, 2], [5, 14, 9, 2, 7, 10, 7], [11, 8, 9, 5, 15, 0, 15], [2, 10, 17, 14, 11, 6, 6], [5, 1, 16, 10, 3, 13, 13], [10, 3, 13, 1, 8, 7, 7], [1, 4, 7, 5, 9, 15, 14], [2, 8, 14, 11, 9, 11, 10], [4, 17, 9, 4, 0, 4, 2], [9, 14, 9, 9, 0, 8, 4], [10, 4, 4, 9, 10, 8, 12], [1, 5, 8, 14, 0, 9, 11], [2, 10, 17, 8, 2, 9, 2], [5, 1, 15, 17, 4, 18, 5], [10, 3, 11, 15, 10, 16, 12], [1, 4, 5, 8, 7, 8, 10], [2, 8, 10, 16, 14, 17, 0], [4, 17, 1, 14, 10, 15, 1], [9, 14, 4, 9, 2, 11, 4], [10, 4, 9, 13, 11, 4, 6], [1, 5, 14, 3, 6, 6, 10], [2, 11, 8, 7, 12, 13, 1], [5, 2, 17, 15, 5, 7, 3], [10, 5, 15, 11, 11, 14, 6], [1, 6, 11, 8, 4, 7, 11], [2, 13, 2, 17, 8, 15, 3], [5, 6, 6, 14, 18, 10, 7], [10, 12, 13, 9, 18, 1, 15], [1, 4, 7, 4, 9, 10, 7], [2, 8, 14, 9, 9, 0, 16], [4, 17, 8, 9, 9, 2, 12], [9, 14, 17, 18, 18, 5, 5], [10, 4, 13, 17, 18, 14, 10], [1, 5, 8, 12, 17, 14, 6], [2, 10, 17, 5, 16, 9, 13], [5, 1, 15, 12, 13, 0, 8], [10, 3, 11, 6, 7, 1, 16], [1, 4, 5, 8, 13, 8, 8], [2, 8, 10, 17, 6, 17, 17], [4, 17, 1, 15, 14, 15, 15], [9, 14, 4, 11, 10, 12, 12], [10, 4, 9, 6, 3, 4, 6], [1, 5, 13, 15, 9, 7, 10], [2, 11, 7, 11, 9, 16, 1], [5, 2, 16, 3, 0, 13, 3], [10, 5, 12, 7, 1, 6, 7], [1, 6, 8, 10, 8, 7, 13], [2, 12, 17, 0, 17, 15, 6], [5, 5, 15, 2, 15, 11, 14], [10, 11, 10, 6, 11, 4, 10], [1, 3, 3, 7, 8, 6, 5]]
def carriesB : List Nat := [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0]

theorem realized_10151 : ∀ i, i < 76 →
    RealizedAt 7 (orbit 10151 (5 + i)) (wordsB.getD i []) (carriesB.getD i 0) := by
  decide +kernel

theorem trajectory_nodup : wordsB.Nodup := by decide +kernel

/-- `w80 ← w79 ← … ← w5` with the actual carries, then an abstract walk from `w5` to `z7`. -/
def backBData : List Nat := [963683441, 1375706943, 643277191, 1260086614, 688721064, 346706652, 175829082, 978144133, 585230268, 1191288276, 1489515535, 1685551906, 795853535, 1512335269, 756297936, 1272014209, 638482842, 1015182712, 500171104, 1141481211, 1507947848, 710570173, 1421153509, 713052492, 358878540, 1070835253, 636910345, 318462012, 161700264, 972246115, 587411431, 431489411, 171174581, 88063370, 982473206, 1211156579, 560885027, 233396993, 1079777184, 1171451670, 416115142, 208054340, 997898891, 1393987215, 695416094, 1288502186, 597335533, 1415361475, 710023284, 261321393, 1024532075, 512266568, 385507820, 192877372, 990310407, 1388835251, 1407773633, 1597751697, 798876208, 1362516792, 1587577511, 793798844, 1067642442, 1474731982, 690326969, 438980964, 219490482, 994233437, 1390988457, 1676049313, 840500736, 420380328, 210190164, 105095082, 941467804, 47321000, 896107487, 450533072, 225266554, 1007671047, 1398873635, 606397028, 1192346614, 687803646, 296979747, 101444353, 53191416, 920467087, 1161134214, 683766964, 1059918532, 532435346, 269860162, 90229979, 938989959, 893651227, 1117198688, 1262587124, 633769642, 272315039, 91463915, 984296940, 851470581, 804704130, 534210458, 1208022488, 604141222, 1240512474, 1561043536, 793149586, 1112303566, 1173072158, 1525101062, 1700992070, 849329986, 428307122, 1002198188, 1212143170, 1356838486, 1616860764, 1750514050, 874090976, 1379129138, 1764836680, 1786598138, 1787679712, 893839856, 1389003596, 1631777270, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def backB : List (List Nat × Nat) := backBData.map (unpack 7)

theorem backB_actual :
    backB.take 75 = (List.range 75).reverse.map (fun i => (wordsB.getD i [], carriesB.getD i 0)) := by
  decide +kernel
theorem backB_ok : walkOKk 7 ((wordsB.getD 75 [], 0) :: backB) = true := by decide +kernel
theorem backB_end : (((wordsB.getD 75 [], 0) :: backB).getLastD ([], 0)).1 = z7 := by
  decide +kernel

/-- Every width-7 word of `orbit 10151 t`, `t = 5 … 80`, has no rank in any `RowsClosed 7` function. -/
theorem trajectory_no_rank {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    ∀ i, i < 76 → R (wordsB.getD i []) = none := by
  intro i hi
  have hall := R_none_of_mem_walk7 rows ((wordsB.getD 75 [], 0) :: backB) backB_ok backB_end
  by_cases h75 : i = 75
  · subst h75
    exact hall _ List.mem_cons_self
  · have hmem : (wordsB.getD i [], carriesB.getD i 0) ∈ backB.take 75 := by
      rw [backB_actual]
      simp only [List.mem_map, List.mem_reverse, List.mem_range]
      exact ⟨i, by omega, rfl⟩
    exact hall _ (List.mem_cons_of_mem _ (List.mem_of_mem_take hmem))

theorem palindrome_81 : PalStartsL [1, 3, 3, 7] (orbit 10151 81) := by
  refine ⟨by decide +kernel, dg (orbit 10151 81), wd (orbit 10151 81), by decide +kernel,
    by decide +kernel, by decide +kernel⟩

theorem orbit_81_value : orbit 10151 81 = 13378652542289211298224525687331 := by decide +kernel

theorem w80_eq : wordsB.getD 75 [] = [1, 3, 3, 7] ++ [8, 6, 5] := by decide +kernel

theorem w80_initial : wordsB.getD 75 [] ∈ initialWordsL 7 [1, 3, 3, 7] := by
  rw [w80_eq]
  exact mem_initialWordsL_of_full 7 [1, 3, 3, 7] [8, 6, 5] (by decide) (by decide)

/-- The width-7 method limit for 1337, obtained from the actual last predecessor word
(`orbit 10151 80`) of the palindrome `orbit 10151 81`. -/
theorem no_certificate_1337_from_orbit {R : List Nat → Option Nat} (rows : RowsClosed 7 R)
    (bound : Nat) : entryOK 7 R ([1, 3, 3, 7], bound) = false :=
  entryOK_false_of_none [1, 3, 3, 7] bound w80_initial (trajectory_no_rank rows 75 (by decide))

end Sprint04.Realized

#print axioms Sprint04.Realized.realized_10097
#print axioms Sprint04.Realized.closedA
#print axioms Sprint04.Realized.backA_words
#print axioms Sprint04.Realized.realized_10097_no_rank
#print axioms Sprint04.Realized.realized_10151
#print axioms Sprint04.Realized.trajectory_nodup
#print axioms Sprint04.Realized.backB_actual
#print axioms Sprint04.Realized.trajectory_no_rank
#print axioms Sprint04.Realized.palindrome_81
#print axioms Sprint04.Realized.w80_initial
#print axioms Sprint04.Realized.no_certificate_1337_from_orbit

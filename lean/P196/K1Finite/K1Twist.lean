/-!
# K1Twist -- finite complement-twist mismatch tables for the four stored decimal lattices

SCOPE (read before citing).  This file kernel-checks, by `decide +kernel`, an *exhaustive table* about the four
stored lattice-row matrices `W` (period-8 `rec0`, `rec1`: spatial period 20; `rec2`: spatial period 48;
period-12 `p12m9`: spatial period 9; the rows are copied from `lattice_formats/p8_scc.txt` and
`lattice_kinks/data/lat_p12m9.txt`).  The mathematical content is a comparison of those stored tables against
*definitions written in this file* (it does not prove the physical claim "no parity-preserving
complement-twisted centre return": the translation of that claim into the table question
`W[(t+d)%p][(j+G/2)%m] = 18 - W[t][j]` for all j is the paper argument of `reports/Agent14ComplementTwist.md`):

  `G t d      = sum_{i<d} g[(t+i) % p]`            (overflow count; the centre moves by G/2 when G is even)
  `L          = p * (2m / gcd(2m, S))`, `S = sum g`   (return length used in `Agent14ComplementTwist`)
  `mis t d s  = #{ j < m | W[(t+d)%p][(j + s) % m] + W[t][j] != 18 }`   (complement mismatches)
  `ordMis t d s = #{ j < m | W[(t+d)%p][(j + s) % m] != W[t][j] }`        (ordinary mismatches)

Proved (names `<lat>_...`, `<lat>` in `rec0 rec1 rec2 p12m9`):
* `<lat>_shape`: the stored data have the stated shape (p rows of m entries, all <= 18) and `L` equals 80, 80,
  192, 72 (kernel computation of the gcd formula).
* `<lat>_t<t>_table` (one theorem per start phase `t < p`): over the advances `1 <= d <= L` with even `G t d`,
  the number of such `d` is the stated count (summing over t: 320 / 320 / 768 / 432), every one has at least
  the stated number of complement mismatches and some `d` attains it (the minimum over t is 16 / 16 / 39 / 7),
  the advances with `ordMis = 0` (ordinary returns, positive control) are exactly the listed `(t, d)` (only
  `d = L`), and the odd-`G` exact complement coincidences `(t, parity, d, G, shift = (G+1-parity)/2)` are exactly
  the listed quintuples (rec0, rec1: 16 of them with d = 18 / 62 mod 80; rec2, p12m9: none).
* general lemmas `G_add`, `G_mod`, `G_period`, `reduce`, `mis_congr`, `scan_complete`, `no_complement_all_d`
  (proved for an arbitrary `Lat`, no sorry): periodicity reduces every advance `d >= 1` to some `d0 in [1, L]`
  with the same row and `G t d = G t d0 + 2 m X` (this uses `S`-periodicity and `2m | (L/p) S`, both
  checked by kernel computation per lattice), and the scan table covers every even-`G` advance.
* `<lat>_no_complement_all_d`: for ALL start phases `t < p` and ALL advances `d >= 1` with `G t d` even,
  `mis t d (G t d / 2) >= 1`, i.e. no exact complement return with the parity-preserving centre displacement.

NOT proved here: that the table question is the right translation of the dynamical claim (paper), the
carry-compatibility part of the Python `complement_carry_glides` check, any statement about parity-flipping
returns for ALL `d` (the `flip`/`ordinary` lists above are for `d <= L` only; for odd `G` the reduction to
`d <= L` is not formalised), anything about other lattices, the existence/non-existence of centres, or the
orbit of 196.  Note (as in the audit): rec0 and rec1 DO have exact complement coincidences when `G` is odd,
see the listed quintuples; they are not excluded by this file.
-/

namespace K1Twist

structure Lat where
  p : Nat
  m : Nat
  g : List Nat
  W : List (List Nat)

def Lat.S (L : Lat) : Nat := L.g.sum
/-- return length `p * (2m / gcd(2m, S))` -/
def Lat.L (L : Lat) : Nat := L.p * (2 * L.m / Nat.gcd (2 * L.m) L.S)

def Lat.G (L : Lat) (t : Nat) : Nat → Nat
  | 0 => 0
  | d + 1 => L.G t d + L.g.getD ((t + d) % L.p) 0

def Lat.row (L : Lat) (t : Nat) : List Nat := L.W.getD (t % L.p) []

/-- number of positions `j` with `a_j + b_j != 18` (one pass; lists are compared position by position) -/
def cntC : List Nat → List Nat → Nat
  | a :: as, b :: bs => (if a + b = 18 then 0 else 1) + cntC as bs
  | _, _ => 0

/-- number of positions `j` with `a_j != b_j` -/
def cntO : List Nat → List Nat → Nat
  | a :: as, b :: bs => (if a = b then 0 else 1) + cntO as bs
  | _, _ => 0

/-- complement mismatches for start phase `t`, advance `d`, centre shift `s`:
`#{ j < m | W[(t+d)%p][(j+s)%m] + W[t][j] != 18 }`.  Implementation: `(row ++ row).drop (s % m)` is the list
`j ↦ row[(j+s)%m]` (truncated by the shorter list in `cntC`). -/
def Lat.mis (L : Lat) (t d s : Nat) : Nat :=
  cntC (L.row t) (((L.row (t + d)) ++ (L.row (t + d))).drop (s % L.m))

/-- ordinary mismatches `#{ j < m | W[(t+d)%p][(j+s)%m] != W[t][j] }` -/
def Lat.ordMis (L : Lat) (t d s : Nat) : Nat :=
  cntO (L.row t) (((L.row (t + d)) ++ (L.row (t + d))).drop (s % L.m))

/-- One scan row `(t, d, G, a, b)` per advance `d = 1, 2, ...`, where `G = G t d`.
* `G` even (centre displacement `G/2`):  `a` = complement mismatches `mis t d (G/2)`, `b` = ordinary mismatches `ordMis t d (G/2)`;
* `G` odd:  `a` = `mis t d ((G+1)/2)` (parity 0), `b` = `mis t d (G/2)` (parity 1; `(G+1-1)/2 = G/2`). -/
def Lat.scan (L : Lat) (t : Nat) : Nat → Nat → Nat → List (Nat × Nat × Nat × Nat × Nat)
  | 0, _, _ => []
  | f + 1, d, G =>
    (if G % 2 = 0 then (t, d, G, L.mis t d (G / 2), L.ordMis t d (G / 2))
     else (t, d, G, L.mis t d ((G + 1) / 2), L.mis t d (G / 2))) ::
      L.scan t f (d + 1) (G + L.g.getD ((t + d) % L.p) 0)

/-- all scan rows for `t < p`, `1 <= d <= L` -/
def Lat.table (L : Lat) : List (Nat × Nat × Nat × Nat × Nat) :=
  (List.range L.p).flatMap fun t => L.scan t L.L 1 (L.g.getD (t % L.p) 0)

/-- complement mismatch counts at the eligible (even `G`) pairs -/
def misEven (T : List (Nat × Nat × Nat × Nat × Nat)) : List Nat :=
  (T.filter fun r => r.2.2.1 % 2 == 0).map fun r => r.2.2.2.1

/-- pairs `(t, d)` with even `G` and zero ordinary mismatches -/
def ordRet (T : List (Nat × Nat × Nat × Nat × Nat)) : List (Nat × Nat) :=
  ((T.filter fun r => r.2.2.1 % 2 == 0).filter fun r => r.2.2.2.2 == 0).map fun r => (r.1, r.2.1)

/-- odd-`G` exact complement coincidences `(t, parity, d, G, shift)` with shift `(G+1-parity)/2` -/
def flipList (T : List (Nat × Nat × Nat × Nat × Nat)) : List (Nat × Nat × Nat × Nat × Nat) :=
  (T.filter fun r => r.2.2.1 % 2 == 1).flatMap fun r =>
    (if r.2.2.2.1 == 0 then [(r.1, 0, r.2.1, r.2.2.1, (r.2.2.1 + 1) / 2)] else []) ++
    (if r.2.2.2.2 == 0 then [(r.1, 1, r.2.1, r.2.2.1, r.2.2.1 / 2)] else [])


theorem G_add (L : Lat) (t a b : Nat) : L.G t (a + b) = L.G t a + L.G ((t + a) % L.p) b := by
  induction b with
  | zero => simp [Lat.G]
  | succ b ih =>
    have e : ((t + a) % L.p + b) % L.p = (t + (a + b)) % L.p := by
      rw [Nat.mod_add_mod, Nat.add_assoc]
    show L.G t (a + b) + L.g.getD ((t + (a + b)) % L.p) 0 =
      L.G t a + (L.G ((t + a) % L.p) b + L.g.getD (((t + a) % L.p + b) % L.p) 0)
    rw [ih, e]
    omega

theorem G_mod (L : Lat) (t d : Nat) : L.G (t % L.p) d = L.G t d := by
  induction d with
  | zero => rfl
  | succ d ih =>
    show L.G (t % L.p) d + L.g.getD ((t % L.p + d) % L.p) 0 = L.G t d + L.g.getD ((t + d) % L.p) 0
    rw [ih, Nat.mod_add_mod]

theorem G_period (L : Lat) (hp : 0 < L.p) (hG : ∀ t, t < L.p → L.G t L.p = L.S) (t k : Nat) :
    L.G t (k * L.p) = k * L.S := by
  induction k with
  | zero => simp [Lat.G]
  | succ k ih =>
    rw [Nat.succ_mul, G_add, ih]
    have e : (t + k * L.p) % L.p = t % L.p := by rw [Nat.add_mul_mod_self_right]
    rw [e, G_mod, ← G_mod L t]
    rw [hG (t % L.p) (Nat.mod_lt _ hp)]
    rw [Nat.succ_mul]

theorem mis_congr (L : Lat) (t d d' s s' : Nat) (h1 : (t + d) % L.p = (t + d') % L.p)
    (h2 : s % L.m = s' % L.m) : L.mis t d s = L.mis t d' s' := by
  unfold Lat.mis Lat.row
  rw [h1, h2]

theorem ordMis_congr (L : Lat) (t d d' s s' : Nat) (h1 : (t + d) % L.p = (t + d') % L.p)
    (h2 : s % L.m = s' % L.m) : L.ordMis t d s = L.ordMis t d' s' := by
  unfold Lat.ordMis Lat.row
  rw [h1, h2]

/-- Periodic reduction: every advance `d ≥ 1` has an equivalent advance `d0 ∈ [1, L]` with the same row
`(t+d) % p` and `G t d = G t d0 + 2 m X`. -/
theorem reduce (L : Lat) (hp : 0 < L.p) (c : Nat) (hLc : L.L = L.p * c) (hLpos : 0 < L.L)
    (hG : ∀ t, t < L.p → L.G t L.p = L.S) (hc : (c * L.S) % (2 * L.m) = 0) (t d : Nat) (hd : 1 ≤ d) :
    ∃ d0 X, 1 ≤ d0 ∧ d0 ≤ L.L ∧ (t + d) % L.p = (t + d0) % L.p ∧ L.G t d = L.G t d0 + 2 * (L.m * X) := by
  have h1 := Nat.div_add_mod (d - 1) L.L
  have h2 := Nat.mod_lt (d - 1) hLpos
  generalize (d - 1) / L.L = q at h1
  generalize (d - 1) % L.L = r at h1 h2
  obtain ⟨u, hu⟩ := Nat.dvd_of_mod_eq_zero hc
  have hd' : d = L.L * q + (r + 1) := by omega
  have hLq : L.L * q = (c * q) * L.p := by rw [hLc]; simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
  refine ⟨r + 1, u * q, by omega, by omega, ?_, ?_⟩
  · rw [hd', hLq, ← Nat.add_assoc, Nat.add_assoc t, Nat.add_comm (c * q * L.p) (r + 1), ← Nat.add_assoc,
      Nat.add_mul_mod_self_right]
  · rw [hd', G_add, hLq, G_period L hp hG]
    have e : (t + (c * q) * L.p) % L.p = t % L.p := by rw [Nat.add_mul_mod_self_right]
    rw [e, G_mod]
    have : c * q * L.S = 2 * (L.m * (u * q)) := by
      calc c * q * L.S = (c * L.S) * q := by simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
        _ = (2 * L.m * u) * q := by rw [hu]
        _ = 2 * (L.m * (u * q)) := by simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
    omega


theorem misEven_cons (e : Nat × Nat × Nat × Nat × Nat) (T : List (Nat × Nat × Nat × Nat × Nat)) :
    misEven (e :: T) = (if e.2.2.1 % 2 = 0 then [e.2.2.2.1] else []) ++ misEven T := by
  unfold misEven
  rw [List.filter_cons]
  by_cases h : e.2.2.1 % 2 = 0 <;> simp [h]

/-- completeness of the scan: every even-`G` advance `d' ∈ [d, d+f)` contributes its complement-mismatch count. -/
theorem scan_complete (L : Lat) (t : Nat) : ∀ f d d', d ≤ d' → d' < d + f → L.G t d' % 2 = 0 →
    L.mis t d' (L.G t d' / 2) ∈ misEven (L.scan t f d (L.G t d)) := by
  intro f
  induction f with
  | zero => intro d d' h1 h2; omega
  | succ f ih =>
    intro d d' h1 h2 h3
    have hs : L.scan t (f + 1) d (L.G t d) =
        (if L.G t d % 2 = 0 then (t, d, L.G t d, L.mis t d (L.G t d / 2), L.ordMis t d (L.G t d / 2))
         else (t, d, L.G t d, L.mis t d ((L.G t d + 1) / 2), L.mis t d (L.G t d / 2))) ::
          L.scan t f (d + 1) (L.G t (d + 1)) := rfl
    rw [hs, misEven_cons]
    by_cases hd : d' = d
    · subst hd
      simp [h3]
    · have := ih (d + 1) d' (by omega) (by omega) h3
      exact List.mem_append_right _ this

/-- Every advance `d ≥ 1` (not only `d ≤ L`): no exact complement return, provided the finite scan table has
all complement-mismatch counts ≥ 1 for each start phase. -/
theorem no_complement_all_d (L : Lat) (hp : 0 < L.p) (c : Nat) (hLc : L.L = L.p * c) (hLpos : 0 < L.L)
    (hG : ∀ t, t < L.p → L.G t L.p = L.S) (hc : (c * L.S) % (2 * L.m) = 0)
    (hT : ∀ t, t < L.p → (misEven (L.scan t L.L 1 (L.G t 1))).all (fun x => 1 ≤ x) = true) :
    ∀ t, t < L.p → ∀ d, 1 ≤ d → L.G t d % 2 = 0 → 1 ≤ L.mis t d (L.G t d / 2) := by
  intro t ht d hd hev
  obtain ⟨d0, X, h1, h2, h3, h4⟩ := reduce L hp c hLc hLpos hG hc t d hd
  have hev0 : L.G t d0 % 2 = 0 := by omega
  have hmem := scan_complete L t L.L 1 d0 h1 (by omega) hev0
  have hall := List.all_eq_true.mp (hT t ht) _ hmem
  have hmis : L.mis t d (L.G t d / 2) = L.mis t d0 (L.G t d0 / 2) := by
    apply mis_congr L t d d0 _ _ h3
    rw [h4]
    have : (L.G t d0 + 2 * (L.m * X)) / 2 = L.G t d0 / 2 + L.m * X := by omega
    rw [this, Nat.add_mul_mod_self_left]
  rw [hmis]
  simpa using hall

/-- weaken a lower bound -/
theorem all_weaken {l : List Nat} {a b : Nat} (h : l.all (fun x => a ≤ x) = true) (hab : b ≤ a) :
    l.all (fun x => b ≤ x) = true := by
  simp only [List.all_eq_true, decide_eq_true_eq] at h ⊢
  intro x hx
  have := h x hx
  omega

def W_rec0 : List (List Nat) := [
  [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13],
  [12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11],
  [6,3,9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4],
  [10,9,13,1,7,6,7,14,13,6,8,11,10,6,8,15,16,11,8,10],
  [2,0,7,3,14,12,15,9,7,13,17,3,1,13,17,11,14,3,18,1],
  [3,2,7,10,8,8,9,5,17,11,12,11,4,5,12,10,7,8,12,10],
  [7,4,15,0,17,16,18,11,15,4,6,3,9,11,5,1,15,17,5,1],
  [8,11,10,6,8,15,16,11,8,10,10,9,13,1,7,6,7,14,13,6]]
def lat_rec0 : Lat := ⟨8, 20, [1,0,1,0,1,0,1,0], W_rec0⟩

def W_rec1 : List (List Nat) := [
  [16,18,11,15,4,6,3,9,11,5,1,15,17,5,1,7,4,15,0,17],
  [15,16,11,8,10,10,9,13,1,7,6,7,14,13,6,8,11,10,6,8],
  [11,14,3,18,1,2,0,7,3,14,12,15,9,7,13,17,3,1,13,17],
  [10,7,8,12,10,3,2,7,10,8,8,9,5,17,11,12,11,4,5,12],
  [1,15,17,5,1,7,4,15,0,17,16,18,11,15,4,6,3,9,11,5],
  [6,7,14,13,6,8,11,10,6,8,15,16,11,8,10,10,9,13,1,7],
  [12,15,9,7,13,17,3,1,13,17,11,14,3,18,1,2,0,7,3,14],
  [8,9,5,17,11,12,11,4,5,12,10,7,8,12,10,3,2,7,10,8]]
def lat_rec1 : Lat := ⟨8, 20, [1,0,1,0,1,0,1,0], W_rec1⟩

def W_rec2 : List (List Nat) := [
  [4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3],
  [7,8,9,6,6,7,9,8,7,9,10,17,9,2,8,9,4,6,11,13,12,3,17,10,7,5,5,8,9,6,10,13,6,8,13,10,10,14,10,7,6,6,6,8,7,2,0,13],
  [15,16,18,12,12,14,18,16,15,9,1,15,9,5,16,18,8,13,3,8,5,8,15,1,15,10,10,16,18,13,1,7,13,17,7,2,2,10,1,15,12,12,12,16,14,4,1,6],
  [12,13,16,12,6,8,14,16,13,5,11,7,5,15,12,16,17,12,7,11,13,13,14,7,7,7,2,8,16,13,5,8,11,12,15,9,4,3,2,7,9,6,6,10,12,9,5,7],
  [5,8,14,5,13,17,9,14,7,12,2,15,11,11,6,14,16,5,16,3,8,8,9,15,14,14,4,17,13,7,11,17,3,6,11,9,9,6,4,14,18,12,13,1,5,9,11,15],
  [11,13,13,10,9,12,8,5,12,10,5,8,8,4,8,11,12,12,12,10,11,16,18,5,11,10,9,12,12,11,9,10,11,9,8,1,9,16,10,9,14,12,7,5,6,15,1,8],
  [3,8,8,2,0,5,17,11,5,1,11,16,16,8,17,3,6,6,6,2,4,14,17,12,3,2,0,6,6,4,0,2,3,9,17,3,9,13,2,0,10,5,15,10,13,10,3,17],
  [11,11,16,10,2,5,13,10,7,6,3,9,14,15,16,11,9,12,12,8,6,9,13,11,6,5,2,6,12,10,4,2,5,13,7,11,13,3,6,2,1,6,11,7,5,5,4,11]]
def lat_rec2 : Lat := ⟨8, 48, [1,0,1,0,1,0,1,0], W_rec2⟩

def W_p12m9 : List (List Nat) := [
  [5,18,4,8,1,15,4,0,5],
  [10,14,13,12,9,7,10,4,5],
  [1,10,8,5,9,16,0,9,11],
  [4,0,17,11,9,12,2,9,2],
  [8,1,15,4,0,5,5,18,4],
  [12,9,7,10,4,5,10,14,13],
  [5,9,16,0,9,11,1,10,8],
  [11,9,12,2,9,2,4,0,17],
  [4,0,5,5,18,4,8,1,15],
  [10,4,5,10,14,13,12,9,7],
  [0,9,11,1,10,8,5,9,16],
  [2,9,2,4,0,17,11,9,12]]
def lat_p12m9 : Lat := ⟨12, 9, [1,0,0,0,1,0,0,0,1,0,0,0], W_p12m9⟩

theorem rec0_shape : lat_rec0.p = 8 ∧ lat_rec0.m = 20 ∧ lat_rec0.W.length = 8 ∧
    (∀ r ∈ lat_rec0.W, r.length = 20) ∧ (∀ r ∈ lat_rec0.W, ∀ x ∈ r, x ≤ 18) ∧ lat_rec0.L = 80 := by
  decide +kernel

/-- `rec0`, start phase 0: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t0_table :
    (misEven (lat_rec0.scan 0 lat_rec0.L 1 (lat_rec0.G 0 1))).length = 40 ∧
    (misEven (lat_rec0.scan 0 lat_rec0.L 1 (lat_rec0.G 0 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 0 lat_rec0.L 1 (lat_rec0.G 0 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 0 lat_rec0.L 1 (lat_rec0.G 0 1)) = [(0,80)] ∧
    flipList (lat_rec0.scan 0 lat_rec0.L 1 (lat_rec0.G 0 1)) = [(0,0,18,9,5), (0,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 1: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t1_table :
    (misEven (lat_rec0.scan 1 lat_rec0.L 1 (lat_rec0.G 1 1))).length = 40 ∧
    (misEven (lat_rec0.scan 1 lat_rec0.L 1 (lat_rec0.G 1 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 1 lat_rec0.L 1 (lat_rec0.G 1 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 1 lat_rec0.L 1 (lat_rec0.G 1 1)) = [(1,80)] ∧
    flipList (lat_rec0.scan 1 lat_rec0.L 1 (lat_rec0.G 1 1)) = [(1,0,18,9,5), (1,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 2: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t2_table :
    (misEven (lat_rec0.scan 2 lat_rec0.L 1 (lat_rec0.G 2 1))).length = 40 ∧
    (misEven (lat_rec0.scan 2 lat_rec0.L 1 (lat_rec0.G 2 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 2 lat_rec0.L 1 (lat_rec0.G 2 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 2 lat_rec0.L 1 (lat_rec0.G 2 1)) = [(2,80)] ∧
    flipList (lat_rec0.scan 2 lat_rec0.L 1 (lat_rec0.G 2 1)) = [(2,0,18,9,5), (2,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 3: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t3_table :
    (misEven (lat_rec0.scan 3 lat_rec0.L 1 (lat_rec0.G 3 1))).length = 40 ∧
    (misEven (lat_rec0.scan 3 lat_rec0.L 1 (lat_rec0.G 3 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 3 lat_rec0.L 1 (lat_rec0.G 3 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 3 lat_rec0.L 1 (lat_rec0.G 3 1)) = [(3,80)] ∧
    flipList (lat_rec0.scan 3 lat_rec0.L 1 (lat_rec0.G 3 1)) = [(3,0,18,9,5), (3,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 4: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t4_table :
    (misEven (lat_rec0.scan 4 lat_rec0.L 1 (lat_rec0.G 4 1))).length = 40 ∧
    (misEven (lat_rec0.scan 4 lat_rec0.L 1 (lat_rec0.G 4 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 4 lat_rec0.L 1 (lat_rec0.G 4 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 4 lat_rec0.L 1 (lat_rec0.G 4 1)) = [(4,80)] ∧
    flipList (lat_rec0.scan 4 lat_rec0.L 1 (lat_rec0.G 4 1)) = [(4,0,18,9,5), (4,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 5: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t5_table :
    (misEven (lat_rec0.scan 5 lat_rec0.L 1 (lat_rec0.G 5 1))).length = 40 ∧
    (misEven (lat_rec0.scan 5 lat_rec0.L 1 (lat_rec0.G 5 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 5 lat_rec0.L 1 (lat_rec0.G 5 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 5 lat_rec0.L 1 (lat_rec0.G 5 1)) = [(5,80)] ∧
    flipList (lat_rec0.scan 5 lat_rec0.L 1 (lat_rec0.G 5 1)) = [(5,0,18,9,5), (5,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 6: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t6_table :
    (misEven (lat_rec0.scan 6 lat_rec0.L 1 (lat_rec0.G 6 1))).length = 40 ∧
    (misEven (lat_rec0.scan 6 lat_rec0.L 1 (lat_rec0.G 6 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 6 lat_rec0.L 1 (lat_rec0.G 6 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 6 lat_rec0.L 1 (lat_rec0.G 6 1)) = [(6,80)] ∧
    flipList (lat_rec0.scan 6 lat_rec0.L 1 (lat_rec0.G 6 1)) = [(6,0,18,9,5), (6,1,62,31,15)] := by decide +kernel

/-- `rec0`, start phase 7: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec0_t7_table :
    (misEven (lat_rec0.scan 7 lat_rec0.L 1 (lat_rec0.G 7 1))).length = 40 ∧
    (misEven (lat_rec0.scan 7 lat_rec0.L 1 (lat_rec0.G 7 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec0.scan 7 lat_rec0.L 1 (lat_rec0.G 7 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec0.scan 7 lat_rec0.L 1 (lat_rec0.G 7 1)) = [(7,80)] ∧
    flipList (lat_rec0.scan 7 lat_rec0.L 1 (lat_rec0.G 7 1)) = [(7,0,18,9,5), (7,1,62,31,15)] := by decide +kernel

theorem rec0_no_complement_all_d :
    ∀ t, t < lat_rec0.p → ∀ d, 1 ≤ d → lat_rec0.G t d % 2 = 0 → 1 ≤ lat_rec0.mis t d (lat_rec0.G t d / 2) := by
  apply no_complement_all_d lat_rec0 (by decide) 10 (by decide +kernel) (by decide +kernel)
    (by decide +kernel) (by decide +kernel)
  intro t ht
  have h : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 := by
    have : t < 8 := ht
    omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact all_weaken (rec0_t0_table.2.1) (by decide)
  · exact all_weaken (rec0_t1_table.2.1) (by decide)
  · exact all_weaken (rec0_t2_table.2.1) (by decide)
  · exact all_weaken (rec0_t3_table.2.1) (by decide)
  · exact all_weaken (rec0_t4_table.2.1) (by decide)
  · exact all_weaken (rec0_t5_table.2.1) (by decide)
  · exact all_weaken (rec0_t6_table.2.1) (by decide)
  · exact all_weaken (rec0_t7_table.2.1) (by decide)

theorem rec1_shape : lat_rec1.p = 8 ∧ lat_rec1.m = 20 ∧ lat_rec1.W.length = 8 ∧
    (∀ r ∈ lat_rec1.W, r.length = 20) ∧ (∀ r ∈ lat_rec1.W, ∀ x ∈ r, x ≤ 18) ∧ lat_rec1.L = 80 := by
  decide +kernel

/-- `rec1`, start phase 0: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t0_table :
    (misEven (lat_rec1.scan 0 lat_rec1.L 1 (lat_rec1.G 0 1))).length = 40 ∧
    (misEven (lat_rec1.scan 0 lat_rec1.L 1 (lat_rec1.G 0 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 0 lat_rec1.L 1 (lat_rec1.G 0 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 0 lat_rec1.L 1 (lat_rec1.G 0 1)) = [(0,80)] ∧
    flipList (lat_rec1.scan 0 lat_rec1.L 1 (lat_rec1.G 0 1)) = [(0,0,18,9,5), (0,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 1: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t1_table :
    (misEven (lat_rec1.scan 1 lat_rec1.L 1 (lat_rec1.G 1 1))).length = 40 ∧
    (misEven (lat_rec1.scan 1 lat_rec1.L 1 (lat_rec1.G 1 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 1 lat_rec1.L 1 (lat_rec1.G 1 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 1 lat_rec1.L 1 (lat_rec1.G 1 1)) = [(1,80)] ∧
    flipList (lat_rec1.scan 1 lat_rec1.L 1 (lat_rec1.G 1 1)) = [(1,0,18,9,5), (1,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 2: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t2_table :
    (misEven (lat_rec1.scan 2 lat_rec1.L 1 (lat_rec1.G 2 1))).length = 40 ∧
    (misEven (lat_rec1.scan 2 lat_rec1.L 1 (lat_rec1.G 2 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 2 lat_rec1.L 1 (lat_rec1.G 2 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 2 lat_rec1.L 1 (lat_rec1.G 2 1)) = [(2,80)] ∧
    flipList (lat_rec1.scan 2 lat_rec1.L 1 (lat_rec1.G 2 1)) = [(2,0,18,9,5), (2,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 3: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t3_table :
    (misEven (lat_rec1.scan 3 lat_rec1.L 1 (lat_rec1.G 3 1))).length = 40 ∧
    (misEven (lat_rec1.scan 3 lat_rec1.L 1 (lat_rec1.G 3 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 3 lat_rec1.L 1 (lat_rec1.G 3 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 3 lat_rec1.L 1 (lat_rec1.G 3 1)) = [(3,80)] ∧
    flipList (lat_rec1.scan 3 lat_rec1.L 1 (lat_rec1.G 3 1)) = [(3,0,18,9,5), (3,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 4: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t4_table :
    (misEven (lat_rec1.scan 4 lat_rec1.L 1 (lat_rec1.G 4 1))).length = 40 ∧
    (misEven (lat_rec1.scan 4 lat_rec1.L 1 (lat_rec1.G 4 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 4 lat_rec1.L 1 (lat_rec1.G 4 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 4 lat_rec1.L 1 (lat_rec1.G 4 1)) = [(4,80)] ∧
    flipList (lat_rec1.scan 4 lat_rec1.L 1 (lat_rec1.G 4 1)) = [(4,0,18,9,5), (4,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 5: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t5_table :
    (misEven (lat_rec1.scan 5 lat_rec1.L 1 (lat_rec1.G 5 1))).length = 40 ∧
    (misEven (lat_rec1.scan 5 lat_rec1.L 1 (lat_rec1.G 5 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 5 lat_rec1.L 1 (lat_rec1.G 5 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 5 lat_rec1.L 1 (lat_rec1.G 5 1)) = [(5,80)] ∧
    flipList (lat_rec1.scan 5 lat_rec1.L 1 (lat_rec1.G 5 1)) = [(5,0,18,9,5), (5,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 6: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t6_table :
    (misEven (lat_rec1.scan 6 lat_rec1.L 1 (lat_rec1.G 6 1))).length = 40 ∧
    (misEven (lat_rec1.scan 6 lat_rec1.L 1 (lat_rec1.G 6 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 6 lat_rec1.L 1 (lat_rec1.G 6 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 6 lat_rec1.L 1 (lat_rec1.G 6 1)) = [(6,80)] ∧
    flipList (lat_rec1.scan 6 lat_rec1.L 1 (lat_rec1.G 6 1)) = [(6,0,18,9,5), (6,1,62,31,15)] := by decide +kernel

/-- `rec1`, start phase 7: (40 eligible advances `d ≤ 80` with even `G`; every one has ≥ 16 complement
mismatches and some has exactly 16; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec1_t7_table :
    (misEven (lat_rec1.scan 7 lat_rec1.L 1 (lat_rec1.G 7 1))).length = 40 ∧
    (misEven (lat_rec1.scan 7 lat_rec1.L 1 (lat_rec1.G 7 1))).all (fun x => 16 ≤ x) = true ∧
    (misEven (lat_rec1.scan 7 lat_rec1.L 1 (lat_rec1.G 7 1))).any (fun x => x == 16) = true ∧
    ordRet (lat_rec1.scan 7 lat_rec1.L 1 (lat_rec1.G 7 1)) = [(7,80)] ∧
    flipList (lat_rec1.scan 7 lat_rec1.L 1 (lat_rec1.G 7 1)) = [(7,0,18,9,5), (7,1,62,31,15)] := by decide +kernel

theorem rec1_no_complement_all_d :
    ∀ t, t < lat_rec1.p → ∀ d, 1 ≤ d → lat_rec1.G t d % 2 = 0 → 1 ≤ lat_rec1.mis t d (lat_rec1.G t d / 2) := by
  apply no_complement_all_d lat_rec1 (by decide) 10 (by decide +kernel) (by decide +kernel)
    (by decide +kernel) (by decide +kernel)
  intro t ht
  have h : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 := by
    have : t < 8 := ht
    omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact all_weaken (rec1_t0_table.2.1) (by decide)
  · exact all_weaken (rec1_t1_table.2.1) (by decide)
  · exact all_weaken (rec1_t2_table.2.1) (by decide)
  · exact all_weaken (rec1_t3_table.2.1) (by decide)
  · exact all_weaken (rec1_t4_table.2.1) (by decide)
  · exact all_weaken (rec1_t5_table.2.1) (by decide)
  · exact all_weaken (rec1_t6_table.2.1) (by decide)
  · exact all_weaken (rec1_t7_table.2.1) (by decide)

theorem rec2_shape : lat_rec2.p = 8 ∧ lat_rec2.m = 48 ∧ lat_rec2.W.length = 8 ∧
    (∀ r ∈ lat_rec2.W, r.length = 48) ∧ (∀ r ∈ lat_rec2.W, ∀ x ∈ r, x ≤ 18) ∧ lat_rec2.L = 192 := by
  decide +kernel

/-- `rec2`, start phase 0: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 42 complement
mismatches and some has exactly 42; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t0_table :
    (misEven (lat_rec2.scan 0 lat_rec2.L 1 (lat_rec2.G 0 1))).length = 96 ∧
    (misEven (lat_rec2.scan 0 lat_rec2.L 1 (lat_rec2.G 0 1))).all (fun x => 42 ≤ x) = true ∧
    (misEven (lat_rec2.scan 0 lat_rec2.L 1 (lat_rec2.G 0 1))).any (fun x => x == 42) = true ∧
    ordRet (lat_rec2.scan 0 lat_rec2.L 1 (lat_rec2.G 0 1)) = [(0,192)] ∧
    flipList (lat_rec2.scan 0 lat_rec2.L 1 (lat_rec2.G 0 1)) = [] := by decide +kernel

/-- `rec2`, start phase 1: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 39 complement
mismatches and some has exactly 39; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t1_table :
    (misEven (lat_rec2.scan 1 lat_rec2.L 1 (lat_rec2.G 1 1))).length = 96 ∧
    (misEven (lat_rec2.scan 1 lat_rec2.L 1 (lat_rec2.G 1 1))).all (fun x => 39 ≤ x) = true ∧
    (misEven (lat_rec2.scan 1 lat_rec2.L 1 (lat_rec2.G 1 1))).any (fun x => x == 39) = true ∧
    ordRet (lat_rec2.scan 1 lat_rec2.L 1 (lat_rec2.G 1 1)) = [(1,192)] ∧
    flipList (lat_rec2.scan 1 lat_rec2.L 1 (lat_rec2.G 1 1)) = [] := by decide +kernel

/-- `rec2`, start phase 2: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 41 complement
mismatches and some has exactly 41; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t2_table :
    (misEven (lat_rec2.scan 2 lat_rec2.L 1 (lat_rec2.G 2 1))).length = 96 ∧
    (misEven (lat_rec2.scan 2 lat_rec2.L 1 (lat_rec2.G 2 1))).all (fun x => 41 ≤ x) = true ∧
    (misEven (lat_rec2.scan 2 lat_rec2.L 1 (lat_rec2.G 2 1))).any (fun x => x == 41) = true ∧
    ordRet (lat_rec2.scan 2 lat_rec2.L 1 (lat_rec2.G 2 1)) = [(2,192)] ∧
    flipList (lat_rec2.scan 2 lat_rec2.L 1 (lat_rec2.G 2 1)) = [] := by decide +kernel

/-- `rec2`, start phase 3: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 41 complement
mismatches and some has exactly 41; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t3_table :
    (misEven (lat_rec2.scan 3 lat_rec2.L 1 (lat_rec2.G 3 1))).length = 96 ∧
    (misEven (lat_rec2.scan 3 lat_rec2.L 1 (lat_rec2.G 3 1))).all (fun x => 41 ≤ x) = true ∧
    (misEven (lat_rec2.scan 3 lat_rec2.L 1 (lat_rec2.G 3 1))).any (fun x => x == 41) = true ∧
    ordRet (lat_rec2.scan 3 lat_rec2.L 1 (lat_rec2.G 3 1)) = [(3,192)] ∧
    flipList (lat_rec2.scan 3 lat_rec2.L 1 (lat_rec2.G 3 1)) = [] := by decide +kernel

/-- `rec2`, start phase 4: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 42 complement
mismatches and some has exactly 42; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t4_table :
    (misEven (lat_rec2.scan 4 lat_rec2.L 1 (lat_rec2.G 4 1))).length = 96 ∧
    (misEven (lat_rec2.scan 4 lat_rec2.L 1 (lat_rec2.G 4 1))).all (fun x => 42 ≤ x) = true ∧
    (misEven (lat_rec2.scan 4 lat_rec2.L 1 (lat_rec2.G 4 1))).any (fun x => x == 42) = true ∧
    ordRet (lat_rec2.scan 4 lat_rec2.L 1 (lat_rec2.G 4 1)) = [(4,192)] ∧
    flipList (lat_rec2.scan 4 lat_rec2.L 1 (lat_rec2.G 4 1)) = [] := by decide +kernel

/-- `rec2`, start phase 5: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 39 complement
mismatches and some has exactly 39; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t5_table :
    (misEven (lat_rec2.scan 5 lat_rec2.L 1 (lat_rec2.G 5 1))).length = 96 ∧
    (misEven (lat_rec2.scan 5 lat_rec2.L 1 (lat_rec2.G 5 1))).all (fun x => 39 ≤ x) = true ∧
    (misEven (lat_rec2.scan 5 lat_rec2.L 1 (lat_rec2.G 5 1))).any (fun x => x == 39) = true ∧
    ordRet (lat_rec2.scan 5 lat_rec2.L 1 (lat_rec2.G 5 1)) = [(5,192)] ∧
    flipList (lat_rec2.scan 5 lat_rec2.L 1 (lat_rec2.G 5 1)) = [] := by decide +kernel

/-- `rec2`, start phase 6: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 41 complement
mismatches and some has exactly 41; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t6_table :
    (misEven (lat_rec2.scan 6 lat_rec2.L 1 (lat_rec2.G 6 1))).length = 96 ∧
    (misEven (lat_rec2.scan 6 lat_rec2.L 1 (lat_rec2.G 6 1))).all (fun x => 41 ≤ x) = true ∧
    (misEven (lat_rec2.scan 6 lat_rec2.L 1 (lat_rec2.G 6 1))).any (fun x => x == 41) = true ∧
    ordRet (lat_rec2.scan 6 lat_rec2.L 1 (lat_rec2.G 6 1)) = [(6,192)] ∧
    flipList (lat_rec2.scan 6 lat_rec2.L 1 (lat_rec2.G 6 1)) = [] := by decide +kernel

/-- `rec2`, start phase 7: (96 eligible advances `d ≤ 192` with even `G`; every one has ≥ 41 complement
mismatches and some has exactly 41; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem rec2_t7_table :
    (misEven (lat_rec2.scan 7 lat_rec2.L 1 (lat_rec2.G 7 1))).length = 96 ∧
    (misEven (lat_rec2.scan 7 lat_rec2.L 1 (lat_rec2.G 7 1))).all (fun x => 41 ≤ x) = true ∧
    (misEven (lat_rec2.scan 7 lat_rec2.L 1 (lat_rec2.G 7 1))).any (fun x => x == 41) = true ∧
    ordRet (lat_rec2.scan 7 lat_rec2.L 1 (lat_rec2.G 7 1)) = [(7,192)] ∧
    flipList (lat_rec2.scan 7 lat_rec2.L 1 (lat_rec2.G 7 1)) = [] := by decide +kernel

theorem rec2_no_complement_all_d :
    ∀ t, t < lat_rec2.p → ∀ d, 1 ≤ d → lat_rec2.G t d % 2 = 0 → 1 ≤ lat_rec2.mis t d (lat_rec2.G t d / 2) := by
  apply no_complement_all_d lat_rec2 (by decide) 24 (by decide +kernel) (by decide +kernel)
    (by decide +kernel) (by decide +kernel)
  intro t ht
  have h : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 := by
    have : t < 8 := ht
    omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact all_weaken (rec2_t0_table.2.1) (by decide)
  · exact all_weaken (rec2_t1_table.2.1) (by decide)
  · exact all_weaken (rec2_t2_table.2.1) (by decide)
  · exact all_weaken (rec2_t3_table.2.1) (by decide)
  · exact all_weaken (rec2_t4_table.2.1) (by decide)
  · exact all_weaken (rec2_t5_table.2.1) (by decide)
  · exact all_weaken (rec2_t6_table.2.1) (by decide)
  · exact all_weaken (rec2_t7_table.2.1) (by decide)

theorem p12m9_shape : lat_p12m9.p = 12 ∧ lat_p12m9.m = 9 ∧ lat_p12m9.W.length = 12 ∧
    (∀ r ∈ lat_p12m9.W, r.length = 9) ∧ (∀ r ∈ lat_p12m9.W, ∀ x ∈ r, x ≤ 18) ∧ lat_p12m9.L = 72 := by
  decide +kernel

/-- `p12m9`, start phase 0: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t0_table :
    (misEven (lat_p12m9.scan 0 lat_p12m9.L 1 (lat_p12m9.G 0 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 0 lat_p12m9.L 1 (lat_p12m9.G 0 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 0 lat_p12m9.L 1 (lat_p12m9.G 0 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 0 lat_p12m9.L 1 (lat_p12m9.G 0 1)) = [(0,72)] ∧
    flipList (lat_p12m9.scan 0 lat_p12m9.L 1 (lat_p12m9.G 0 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 1: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t1_table :
    (misEven (lat_p12m9.scan 1 lat_p12m9.L 1 (lat_p12m9.G 1 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 1 lat_p12m9.L 1 (lat_p12m9.G 1 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 1 lat_p12m9.L 1 (lat_p12m9.G 1 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 1 lat_p12m9.L 1 (lat_p12m9.G 1 1)) = [(1,72)] ∧
    flipList (lat_p12m9.scan 1 lat_p12m9.L 1 (lat_p12m9.G 1 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 2: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t2_table :
    (misEven (lat_p12m9.scan 2 lat_p12m9.L 1 (lat_p12m9.G 2 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 2 lat_p12m9.L 1 (lat_p12m9.G 2 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 2 lat_p12m9.L 1 (lat_p12m9.G 2 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 2 lat_p12m9.L 1 (lat_p12m9.G 2 1)) = [(2,72)] ∧
    flipList (lat_p12m9.scan 2 lat_p12m9.L 1 (lat_p12m9.G 2 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 3: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t3_table :
    (misEven (lat_p12m9.scan 3 lat_p12m9.L 1 (lat_p12m9.G 3 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 3 lat_p12m9.L 1 (lat_p12m9.G 3 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 3 lat_p12m9.L 1 (lat_p12m9.G 3 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 3 lat_p12m9.L 1 (lat_p12m9.G 3 1)) = [(3,72)] ∧
    flipList (lat_p12m9.scan 3 lat_p12m9.L 1 (lat_p12m9.G 3 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 4: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t4_table :
    (misEven (lat_p12m9.scan 4 lat_p12m9.L 1 (lat_p12m9.G 4 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 4 lat_p12m9.L 1 (lat_p12m9.G 4 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 4 lat_p12m9.L 1 (lat_p12m9.G 4 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 4 lat_p12m9.L 1 (lat_p12m9.G 4 1)) = [(4,72)] ∧
    flipList (lat_p12m9.scan 4 lat_p12m9.L 1 (lat_p12m9.G 4 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 5: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t5_table :
    (misEven (lat_p12m9.scan 5 lat_p12m9.L 1 (lat_p12m9.G 5 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 5 lat_p12m9.L 1 (lat_p12m9.G 5 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 5 lat_p12m9.L 1 (lat_p12m9.G 5 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 5 lat_p12m9.L 1 (lat_p12m9.G 5 1)) = [(5,72)] ∧
    flipList (lat_p12m9.scan 5 lat_p12m9.L 1 (lat_p12m9.G 5 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 6: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t6_table :
    (misEven (lat_p12m9.scan 6 lat_p12m9.L 1 (lat_p12m9.G 6 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 6 lat_p12m9.L 1 (lat_p12m9.G 6 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 6 lat_p12m9.L 1 (lat_p12m9.G 6 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 6 lat_p12m9.L 1 (lat_p12m9.G 6 1)) = [(6,72)] ∧
    flipList (lat_p12m9.scan 6 lat_p12m9.L 1 (lat_p12m9.G 6 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 7: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t7_table :
    (misEven (lat_p12m9.scan 7 lat_p12m9.L 1 (lat_p12m9.G 7 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 7 lat_p12m9.L 1 (lat_p12m9.G 7 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 7 lat_p12m9.L 1 (lat_p12m9.G 7 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 7 lat_p12m9.L 1 (lat_p12m9.G 7 1)) = [(7,72)] ∧
    flipList (lat_p12m9.scan 7 lat_p12m9.L 1 (lat_p12m9.G 7 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 8: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t8_table :
    (misEven (lat_p12m9.scan 8 lat_p12m9.L 1 (lat_p12m9.G 8 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 8 lat_p12m9.L 1 (lat_p12m9.G 8 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 8 lat_p12m9.L 1 (lat_p12m9.G 8 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 8 lat_p12m9.L 1 (lat_p12m9.G 8 1)) = [(8,72)] ∧
    flipList (lat_p12m9.scan 8 lat_p12m9.L 1 (lat_p12m9.G 8 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 9: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t9_table :
    (misEven (lat_p12m9.scan 9 lat_p12m9.L 1 (lat_p12m9.G 9 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 9 lat_p12m9.L 1 (lat_p12m9.G 9 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 9 lat_p12m9.L 1 (lat_p12m9.G 9 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 9 lat_p12m9.L 1 (lat_p12m9.G 9 1)) = [(9,72)] ∧
    flipList (lat_p12m9.scan 9 lat_p12m9.L 1 (lat_p12m9.G 9 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 10: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t10_table :
    (misEven (lat_p12m9.scan 10 lat_p12m9.L 1 (lat_p12m9.G 10 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 10 lat_p12m9.L 1 (lat_p12m9.G 10 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 10 lat_p12m9.L 1 (lat_p12m9.G 10 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 10 lat_p12m9.L 1 (lat_p12m9.G 10 1)) = [(10,72)] ∧
    flipList (lat_p12m9.scan 10 lat_p12m9.L 1 (lat_p12m9.G 10 1)) = [] := by decide +kernel

/-- `p12m9`, start phase 11: (36 eligible advances `d ≤ 72` with even `G`; every one has ≥ 7 complement
mismatches and some has exactly 7; the ordinary returns are the listed ones; the odd-`G` exact complement
coincidences are the listed ones). -/
theorem p12m9_t11_table :
    (misEven (lat_p12m9.scan 11 lat_p12m9.L 1 (lat_p12m9.G 11 1))).length = 36 ∧
    (misEven (lat_p12m9.scan 11 lat_p12m9.L 1 (lat_p12m9.G 11 1))).all (fun x => 7 ≤ x) = true ∧
    (misEven (lat_p12m9.scan 11 lat_p12m9.L 1 (lat_p12m9.G 11 1))).any (fun x => x == 7) = true ∧
    ordRet (lat_p12m9.scan 11 lat_p12m9.L 1 (lat_p12m9.G 11 1)) = [(11,72)] ∧
    flipList (lat_p12m9.scan 11 lat_p12m9.L 1 (lat_p12m9.G 11 1)) = [] := by decide +kernel

theorem p12m9_no_complement_all_d :
    ∀ t, t < lat_p12m9.p → ∀ d, 1 ≤ d → lat_p12m9.G t d % 2 = 0 → 1 ≤ lat_p12m9.mis t d (lat_p12m9.G t d / 2) := by
  apply no_complement_all_d lat_p12m9 (by decide) 6 (by decide +kernel) (by decide +kernel)
    (by decide +kernel) (by decide +kernel)
  intro t ht
  have h : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 ∨ t = 10 ∨ t = 11 := by
    have : t < 12 := ht
    omega
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact all_weaken (p12m9_t0_table.2.1) (by decide)
  · exact all_weaken (p12m9_t1_table.2.1) (by decide)
  · exact all_weaken (p12m9_t2_table.2.1) (by decide)
  · exact all_weaken (p12m9_t3_table.2.1) (by decide)
  · exact all_weaken (p12m9_t4_table.2.1) (by decide)
  · exact all_weaken (p12m9_t5_table.2.1) (by decide)
  · exact all_weaken (p12m9_t6_table.2.1) (by decide)
  · exact all_weaken (p12m9_t7_table.2.1) (by decide)
  · exact all_weaken (p12m9_t8_table.2.1) (by decide)
  · exact all_weaken (p12m9_t9_table.2.1) (by decide)
  · exact all_weaken (p12m9_t10_table.2.1) (by decide)
  · exact all_weaken (p12m9_t11_table.2.1) (by decide)

end K1Twist

#print axioms K1Twist.rec0_shape
#print axioms K1Twist.rec0_t0_table
#print axioms K1Twist.rec0_t1_table
#print axioms K1Twist.rec0_t2_table
#print axioms K1Twist.rec0_t3_table
#print axioms K1Twist.rec0_t4_table
#print axioms K1Twist.rec0_t5_table
#print axioms K1Twist.rec0_t6_table
#print axioms K1Twist.rec0_t7_table
#print axioms K1Twist.rec0_no_complement_all_d
#print axioms K1Twist.rec1_shape
#print axioms K1Twist.rec1_t0_table
#print axioms K1Twist.rec1_t1_table
#print axioms K1Twist.rec1_t2_table
#print axioms K1Twist.rec1_t3_table
#print axioms K1Twist.rec1_t4_table
#print axioms K1Twist.rec1_t5_table
#print axioms K1Twist.rec1_t6_table
#print axioms K1Twist.rec1_t7_table
#print axioms K1Twist.rec1_no_complement_all_d
#print axioms K1Twist.rec2_shape
#print axioms K1Twist.rec2_t0_table
#print axioms K1Twist.rec2_t1_table
#print axioms K1Twist.rec2_t2_table
#print axioms K1Twist.rec2_t3_table
#print axioms K1Twist.rec2_t4_table
#print axioms K1Twist.rec2_t5_table
#print axioms K1Twist.rec2_t6_table
#print axioms K1Twist.rec2_t7_table
#print axioms K1Twist.rec2_no_complement_all_d
#print axioms K1Twist.p12m9_shape
#print axioms K1Twist.p12m9_t0_table
#print axioms K1Twist.p12m9_t1_table
#print axioms K1Twist.p12m9_t2_table
#print axioms K1Twist.p12m9_t3_table
#print axioms K1Twist.p12m9_t4_table
#print axioms K1Twist.p12m9_t5_table
#print axioms K1Twist.p12m9_t6_table
#print axioms K1Twist.p12m9_t7_table
#print axioms K1Twist.p12m9_t8_table
#print axioms K1Twist.p12m9_t9_table
#print axioms K1Twist.p12m9_t10_table
#print axioms K1Twist.p12m9_t11_table
#print axioms K1Twist.p12m9_no_complement_all_d

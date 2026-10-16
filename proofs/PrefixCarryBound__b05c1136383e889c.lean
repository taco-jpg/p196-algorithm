import Std

/-!
Agent #10: two-column necessary dynamics and a checked path-count certificate.
The actual-orbit inclusion is proved separately; this file has no project imports.
The generated rank data are untrusted until all local inequalities below compile.
-/
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace CarryObservability
abbrev State := Nat × Nat

def Valid (s : State) : Prop := 1 ≤ s.1 ∧ s.1 ≤ 18 ∧ s.2 ≤ 18
instance (s : State) : Decidable (Valid s) := inferInstanceAs (Decidable (1 ≤ s.1 ∧ s.1 ≤ 18 ∧ s.2 ≤ 18))

def innerBit (v : Bool) : Nat := if v then 1 else 0

def overflow (s : State) (v : Bool) : Nat :=
  (s.1 + (s.2 + innerBit v) / 10) / 10

def cost (s : State) (v : Bool) : Nat := 1 - overflow s v

def next (s : State) (v : Bool) : State :=
  let p := s.1
  let q := s.2
  let a := p / 10
  let u := (q + innerBit v) / 10
  let b := (q + a) / 10
  let h := (p + u) / 10
  if h = 0 then
    (2 * p + u - 10 * a, 2 * q + a + innerBit v - 10 * (b + u))
  else
    (p - 10 * a + 1, p + q + a + u - 10 * (b + h))

def minCost : Nat → State → Nat
  | 0, _ => 0
  | n + 1, s =>
    min (cost s false + minCost n (next s false))
        (cost s true + minCost n (next s true))

def pathCost : State → List Bool → Nat
  | _, [] => 0
  | s, v :: vs => cost s v + pathCost (next s v) vs

-- Three-bit rank entries, in increasing n, p, q order; generated independently.
-- The data are not trusted: rank_step_fin checks every edge in the kernel.
def rankBlob : Nat := 40847271718323373382255306670358191534539943073260721303878421752305893106318568372732721053193744643292932999220380235192928833431159889984193904036409391084821098087763502935871914992373260234168490156548220684477631144354802829080824691453427448065186768530697358906129934534341015460205089824817506743025809545934794343794212057925662170446702154027123235910511885822462703725213938493882824871794244083879342935904255704703715333107196254382450680700123407374466241201871586673327593249717160055564019848563867814314306307214250923599658831070010680283323939874435912202215286600037140891385940947366961308920269301008575582749249908582080266673708858630910738909069368199006884705061159875878286487572850555696372170615936784690362293422669169180288606146964100547723812507824918874391474325890924878822825133903602805132862756243296765247313183807694529387393827449094871644669932678188803151467163636480713003353287900733783183575351908333217060698360605757857785397977218126578921490814482546875546268194153662058566270140250156444182278054167106864561845014425374888329661978022368096313167288718105877436009900494177134023617543514881309931173079973995880196498592823088477194873394060412245199637931557716716347010185626473030855981476070085496940002172705436853806063299693625277530541893474380393067371259152254621944759995310782878195124175685278981281425798964993133349249084070009365298543769426383212776353032916101820094735944548536328270312574373273381931607481656182664028857490940091027993041152233067488386411925432069857910889896340118794416433175713536372327642665601887997444730661041952470361505511542594636127040947754421498588754472403235822755974414817407144905853367756964422558140777142832657868804912919821614931030371121737774694489617156251018683905076315832770680170869652691283637945294191641974220590250414367504399500184522953373222862848934449720114710142964964236553535655885423798952786728644947150084151065183150808870259504994280665948972238411973819775012089082654253765295203928367538771948748495265174571529384045090878615047268782899976089428364327952458736754429673683553648504894376950626501424936382929416599668977015230410430497523179335888110846400073238960958172444816444810852368156505338228928026982321178306893540824127998058657948720429717948164257405943684432742017194511740306853436133413166562797733514256034477563822740861253921775866713738458416017184474817275990567536768181750258744997173958333471169745481

def rank (n : Nat) (s : State) : Nat :=
  if n = 0 then 0 else if n = 9 then 4 else
    (rankBlob >>> (3 * ((n - 1) * 342 + (s.1 - 1) * 19 + s.2))) % 8

theorem next_valid_fin :
    ∀ p : Fin 18, ∀ q : Fin 19, ∀ v : Bool,
      Valid (next (p.val + 1, q.val) v) := by decide +kernel

theorem next_valid (s : State) (hs : Valid s) (v : Bool) :
    Valid (next s v) := by
  rcases s with ⟨p, q⟩
  rcases hs with ⟨hp, hp', hq⟩
  have h := next_valid_fin ⟨p - 1, by omega⟩ ⟨q, by omega⟩ v
  have he : p - 1 + 1 = p := by omega
  simpa only [he] using h

theorem rank_step_fin :
    ∀ n : Fin 9, ∀ p : Fin 18, ∀ q : Fin 19, ∀ v : Bool,
      rank (n.val + 1) (p.val + 1, q.val) ≤
        cost (p.val + 1, q.val) v + rank n.val (next (p.val + 1, q.val) v) := by
  decide +kernel

theorem rank_step (n : Nat) (s : State) (hn : n < 9)
    (hs : Valid s) (v : Bool) :
    rank (n + 1) s ≤ cost s v + rank n (next s v) := by
  rcases s with ⟨p, q⟩
  rcases hs with ⟨hp, hp', hq⟩
  have h := rank_step_fin ⟨n, hn⟩ ⟨p - 1, by omega⟩ ⟨q, by omega⟩ v
  have he : p - 1 + 1 = p := by omega
  simpa only [he] using h

theorem rank_le_minCost (n : Nat) (s : State) (hn : n ≤ 9) (hs : Valid s) :
    rank n s ≤ minCost n s := by
  induction n generalizing s with
  | zero => simp [rank, minCost]
  | succ n ih =>
    have hfalse := rank_step n s (by omega) hs false
    have htrue := rank_step n s (by omega) hs true
    have hfalse' := ih (next s false) (by omega) (next_valid s hs false)
    have htrue' := ih (next s true) (by omega) (next_valid s hs true)
    change rank (n + 1) s ≤
      min (cost s false + minCost n (next s false))
        (cost s true + minCost n (next s true))
    exact Nat.le_min.mpr ⟨by omega, by omega⟩

theorem minCost_step_le (n : Nat) (s : State) (v : Bool) :
    minCost (n + 1) s ≤ cost s v + minCost n (next s v) := by
  cases v
  · exact Nat.min_le_left _ _
  · exact Nat.min_le_right _ _

theorem minCost_le_pathCost (s : State) (vs : List Bool) :
    minCost vs.length s ≤ pathCost s vs := by
  induction vs generalizing s with
  | nil => exact Nat.le_refl 0
  | cons v vs ih =>
    exact Nat.le_trans (minCost_step_le vs.length s v)
      (Nat.add_le_add_left (ih (next s v)) (cost s v))

/-- All 342 possible initial two-column states are included. -/
theorem nine_step_minimum (s : State) (hs : Valid s) : 4 ≤ minCost 9 s := by
  have h := rank_le_minCost 9 s (by decide) hs
  simpa only [rank, if_neg (by decide : ¬(9:Nat)=0), if_pos rfl] using h

/-- Generic necessary-graph conclusion; no actual-orbit premise is hidden. -/
theorem nine_step_path_bound (s : State) (hs : Valid s)
    (vs : List Bool) (hlen : vs.length = 9) : 4 ≤ pathCost s vs := by
  have h := minCost_le_pathCost s vs
  rw [hlen] at h
  exact Nat.le_trans (nine_step_minimum s hs) h

/-- Telescoping form for any actual or abstract trajectory in the finite graph. -/
theorem nine_step_trajectory_bound
    (states : Nat → State) (bits : Nat → Bool) (count : Nat → Nat)
    (hstart : count 0 = 0)
    (hvalid : ∀ t, t ≤ 9 → Valid (states t))
    (hnext : ∀ t, t < 9 → states (t + 1) = next (states t) (bits t))
    (hcount : ∀ t, t < 9 → count (t + 1) = count t + cost (states t) (bits t)) :
    4 ≤ count 9 := by
  have hpot : ∀ t, t ≤ 9 → 4 ≤ count t + rank (9 - t) (states t) := by
    intro t
    induction t with
    | zero =>
      intro _
      simp [rank, hstart]
    | succ t ih =>
      intro ht
      have hh := ih (by omega)
      have hs := rank_step (8 - t) (states t) (by omega) (hvalid t (by omega)) (bits t)
      have ha : 8 - t + 1 = 9 - t := by omega
      rw [ha, ←hnext t (by omega)] at hs
      have hc := hcount t (by omega)
      have hb : 9 - (t + 1) = 8 - t := by omega
      rw [hb]
      omega
  have h := hpot 9 (by decide)
  simpa [rank] using h

/-- The nonoverflow-counting argument alone cannot use eight steps. -/
def shortPath : List Bool := [false, false, false, false, false, false, false, false]

theorem shortPath_cost : pathCost (13, 6) shortPath = 3 := by decide +kernel

theorem eight_step_counting_obstruction : minCost 8 (13, 6) = 3 := by
  have hlo := rank_le_minCost 8 (13, 6) (by decide) (by decide)
  have hr : rank 8 (13, 6) = 3 := by decide +kernel
  rw [hr] at hlo
  have hhi := minCost_le_pathCost (13, 6) shortPath
  have hlen : shortPath.length = 8 := by decide +kernel
  rw [hlen, shortPath_cost] at hhi
  omega


#print axioms next_valid_fin
#print axioms next_valid
#print axioms rank_step_fin
#print axioms rank_step
#print axioms rank_le_minCost
#print axioms minCost_step_le
#print axioms minCost_le_pathCost
#print axioms nine_step_minimum
#print axioms nine_step_path_bound
#print axioms nine_step_trajectory_bound
#print axioms shortPath_cost
#print axioms eight_step_counting_obstruction
end CarryObservability

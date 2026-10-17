import Lean.Elab.Tactic.Omega

/-! Agent #4: exact three-column saturation obstruction.
The finite relation permits both incoming inner carries. It is a necessary
projection, not a claim that every abstract path has an ordinary integer lift.
-/
namespace P196.Agent4.Saturation

structure Prefix where
  a : Nat
  b : Nat
  c : Nat
  deriving DecidableEq, Repr

def advance (s : Prefix) (e : Nat) : Prefix × Nat :=
  let l1 := s.a / 10
  let l2 := (s.b + l1) / 10
  let d0 := s.a % 10
  let d1 := (s.b + l1) % 10
  let d2 := (s.c + l2) % 10
  let r2 := (s.c + e) / 10
  let r1 := (s.b + r2) / 10
  let gamma := (s.a + r1) / 10
  let h0 := (s.a + r1) % 10
  let h1 := (s.b + r2) % 10
  let h2 := (s.c + e) % 10
  if gamma = 0 then (⟨d0+h0, d1+h1, d2+h2⟩, gamma)
  else (⟨d0+1, d1+h0, d2+h1⟩, gamma)

def potential1 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 => 0
  | _ => 0

def potential2 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 => 1
  | 4 => if c ≤ 8 then 1 else (if c ≤ 9 then 6 else (if c ≤ 13 then 1 else (if c ≤ 17 then 6 else (4))))
  | 5 => if c ≤ 2 then 8 else (if c ≤ 3 then 6 else (if c ≤ 4 then 8 else (6)))
  | 6 => if c ≤ 1 then 6 else (if c ≤ 4 then 8 else (6))
  | 7 => if c ≤ 7 then 6 else (4)
  | 8 => 4
  | 9 => if c ≤ 9 then 4 else (0)
  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 => 0
  | _ => 0

def potential3 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 10 | 11 | 12 | 13 => 1
  | 4 => if c ≤ 8 then 1 else (if c ≤ 9 then 3 else (if c ≤ 13 then 1 else (3)))
  | 5 => 3
  | 6 => if c ≤ 4 then 3 else (if c ≤ 9 then 8 else (if c ≤ 10 then 10 else (if c ≤ 11 then 8 else (if c ≤ 12 then 10 else (8)))))
  | 7 => if c ≤ 0 then 10 else (if c ≤ 1 then 8 else (if c ≤ 2 then 10 else (if c ≤ 4 then 8 else (3))))
  | 8 => if c ≤ 8 then 3 else (if c ≤ 11 then 8 else (if c ≤ 12 then 3 else (if c ≤ 14 then 8 else (if c ≤ 15 then 10 else (if c ≤ 16 then 8 else (if c ≤ 17 then 10 else (8)))))))
  | 9 => if c ≤ 3 then 8 else (if c ≤ 5 then 10 else (if c ≤ 6 then 8 else (if c ≤ 7 then 10 else (if c ≤ 9 then 8 else (if c ≤ 13 then 1 else (3))))))
  | 14 => if c ≤ 13 then 1 else (3)
  | 15 => if c ≤ 14 then 3 else (if c ≤ 16 then 5 else (if c ≤ 17 then 3 else (5)))
  | 16 => if c ≤ 9 then 5 else (10)
  | 17 => if c ≤ 0 then 5 else (if c ≤ 1 then 10 else (if c ≤ 4 then 5 else (if c ≤ 8 then 3 else (if c ≤ 9 then 5 else (3)))))
  | 18 => if c ≤ 1 then 5 else (if c ≤ 2 then 3 else (if c ≤ 14 then 5 else (10)))
  | _ => 0

def potential4 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 => 41
  | 9 => if c ≤ 8 then 41 else (if c ≤ 14 then 46 else (44))
  | 10 => if c ≤ 4 then 48 else (if c ≤ 8 then 46 else (if c ≤ 9 then 48 else (46)))
  | 11 | 13 => 46
  | 12 => if c ≤ 3 then 46 else (if c ≤ 9 then 48 else (46))
  | 14 => if c ≤ 14 then 46 else (44)
  | 15 | 16 | 17 | 18 => 44
  | _ => 0

def potential5 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 => 2
  | 9 | 14 => if c ≤ 8 then 2 else (3)
  | 10 => 3
  | 11 => if c ≤ 2 then 3 else (if c ≤ 3 then 8 else (if c ≤ 6 then 3 else (if c ≤ 7 then 8 else (if c ≤ 8 then 3 else (if c ≤ 9 then 8 else (if c ≤ 10 then 10 else (if c ≤ 13 then 8 else (if c ≤ 14 then 10 else (8)))))))))
  | 12 => if c ≤ 10 then 8 else (if c ≤ 13 then 6 else (if c ≤ 15 then 8 else (6)))
  | 13 => if c ≤ 10 then 6 else (if c ≤ 13 then 2 else (if c ≤ 15 then 6 else (2)))
  | 15 => if c ≤ 12 then 3 else (if c ≤ 13 then 8 else (if c ≤ 16 then 3 else (if c ≤ 17 then 8 else (3))))
  | 16 => if c ≤ 0 then 10 else (if c ≤ 3 then 8 else (if c ≤ 4 then 10 else (if c ≤ 8 then 8 else (if c ≤ 9 then 10 else (if c ≤ 13 then 8 else (if c ≤ 14 then 10 else (8)))))))
  | 17 => if c ≤ 0 then 8 else (if c ≤ 3 then 6 else (if c ≤ 5 then 8 else (if c ≤ 8 then 6 else (if c ≤ 9 then 8 else (6)))))
  | 18 => if c ≤ 0 then 6 else (if c ≤ 3 then 2 else (if c ≤ 5 then 6 else (if c ≤ 8 then 2 else (if c ≤ 9 then 6 else (2)))))
  | _ => 0

def potential6 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 => 41
  | 9 => if c ≤ 8 then 41 else (43)
  | 10 | 11 | 15 | 16 => 43
  | 12 => if c ≤ 10 then 43 else (if c ≤ 14 then 48 else (if c ≤ 15 then 43 else (48)))
  | 13 => if c ≤ 0 then 48 else (if c ≤ 1 then 50 else (if c ≤ 4 then 48 else (if c ≤ 5 then 50 else (48))))
  | 14 => if c ≤ 0 then 50 else (if c ≤ 3 then 48 else (if c ≤ 4 then 50 else (if c ≤ 9 then 48 else (43))))
  | 17 => if c ≤ 0 then 43 else (if c ≤ 3 then 48 else (if c ≤ 5 then 43 else (if c ≤ 10 then 48 else (if c ≤ 11 then 50 else (if c ≤ 14 then 48 else (if c ≤ 15 then 50 else (48)))))))
  | 18 => if c ≤ 8 then 48 else (if c ≤ 10 then 50 else (if c ≤ 13 then 48 else (if c ≤ 14 then 50 else (48))))
  | _ => 0

def potential7 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 => 41
  | 9 => if c ≤ 8 then 41 else (43)
  | 10 | 15 => 43
  | 11 => if c ≤ 11 then 43 else (if c ≤ 14 then 45 else (if c ≤ 16 then 43 else (45)))
  | 12 => 45
  | 13 => if c ≤ 1 then 45 else (if c ≤ 4 then 50 else (if c ≤ 5 then 45 else (50)))
  | 14 => if c ≤ 0 then 50 else (if c ≤ 3 then 45 else (if c ≤ 4 then 50 else (if c ≤ 9 then 45 else (43))))
  | 16 => if c ≤ 1 then 43 else (if c ≤ 3 then 45 else (if c ≤ 6 then 43 else (45)))
  | 17 => if c ≤ 11 then 45 else (if c ≤ 13 then 50 else (if c ≤ 15 then 45 else (50)))
  | 18 => if c ≤ 10 then 50 else (if c ≤ 13 then 45 else (if c ≤ 14 then 50 else (45)))
  | _ => 0

def potential8 (b c : Nat) : Nat :=
  match b with
  | 0 => 43
  | 1 => if c ≤ 2 then 43 else (if c ≤ 4 then 45 else (if c ≤ 7 then 43 else (45)))
  | 2 => if c ≤ 3 then 45 else (if c ≤ 4 then 47 else (if c ≤ 7 then 45 else (47)))
  | 3 => if c ≤ 9 then 52 else (if c ≤ 11 then 47 else (if c ≤ 14 then 45 else (if c ≤ 15 then 47 else (45))))
  | 4 => if c ≤ 9 then 45 else (43)
  | 5 => if c ≤ 12 then 43 else (if c ≤ 14 then 45 else (if c ≤ 17 then 43 else (45)))
  | 6 => if c ≤ 13 then 45 else (if c ≤ 14 then 47 else (if c ≤ 17 then 45 else (47)))
  | 7 => if c ≤ 8 then 47 else (52)
  | 8 => if c ≤ 1 then 47 else (if c ≤ 3 then 45 else (if c ≤ 5 then 47 else (45)))
  | 9 => if c ≤ 8 then 47 else (if c ≤ 14 then 54 else (if c ≤ 17 then 49 else (47)))
  | 10 => if c ≤ 2 then 49 else (if c ≤ 3 then 47 else (if c ≤ 4 then 49 else (if c ≤ 5 then 47 else (if c ≤ 6 then 49 else (if c ≤ 8 then 47 else (if c ≤ 12 then 49 else (if c ≤ 14 then 56 else (if c ≤ 17 then 49 else (56)))))))))
  | 11 => if c ≤ 1 then 51 else (if c ≤ 2 then 49 else (if c ≤ 8 then 51 else (if c ≤ 11 then 53 else (if c ≤ 13 then 55 else (if c ≤ 14 then 57 else (if c ≤ 16 then 53 else (if c ≤ 17 then 55 else (57))))))))
  | 12 => if c ≤ 0 then 72 else (if c ≤ 1 then 64 else (if c ≤ 2 then 68 else (if c ≤ 3 then 62 else (if c ≤ 4 then 72 else (if c ≤ 5 then 70 else (if c ≤ 6 then 68 else (if c ≤ 7 then 60 else (if c ≤ 8 then 62 else (if c ≤ 9 then 66 else (if c ≤ 11 then 58 else (if c ≤ 12 then 60 else (if c ≤ 13 then 55 else (if c ≤ 14 then 60 else (if c ≤ 15 then 58 else (if c ≤ 16 then 60 else (if c ≤ 17 then 55 else (60)))))))))))))))))
  | 13 => if c ≤ 0 then 78 else (if c ≤ 1 then 66 else (if c ≤ 3 then 56 else (if c ≤ 4 then 78 else (if c ≤ 5 then 66 else (if c ≤ 8 then 56 else (if c ≤ 9 then 51 else (if c ≤ 10 then 58 else (if c ≤ 13 then 53 else (if c ≤ 14 then 58 else (53))))))))))
  | 14 => if c ≤ 0 then 76 else (if c ≤ 1 then 70 else (if c ≤ 2 then 76 else (if c ≤ 3 then 72 else (if c ≤ 4 then 76 else (if c ≤ 5 then 74 else (if c ≤ 6 then 70 else (if c ≤ 7 then 76 else (if c ≤ 8 then 66 else (if c ≤ 9 then 64 else (if c ≤ 14 then 54 else (if c ≤ 15 then 47 else (if c ≤ 16 then 49 else (47)))))))))))))
  | 15 => if c ≤ 2 then 49 else (if c ≤ 3 then 56 else (if c ≤ 7 then 49 else (if c ≤ 8 then 56 else (if c ≤ 11 then 51 else (if c ≤ 12 then 49 else (51))))))
  | 16 => if c ≤ 1 then 53 else (if c ≤ 3 then 55 else (if c ≤ 6 then 53 else (if c ≤ 7 then 55 else (if c ≤ 8 then 57 else (if c ≤ 9 then 74 else (if c ≤ 10 then 72 else (if c ≤ 11 then 64 else (if c ≤ 12 then 68 else (if c ≤ 13 then 62 else (if c ≤ 14 then 74 else (if c ≤ 15 then 70 else (if c ≤ 16 then 66 else (if c ≤ 17 then 60 else (62))))))))))))))
  | 17 => if c ≤ 1 then 58 else (if c ≤ 2 then 60 else (if c ≤ 3 then 55 else (if c ≤ 4 then 80 else (if c ≤ 5 then 58 else (if c ≤ 6 then 60 else (if c ≤ 7 then 55 else (if c ≤ 8 then 60 else (if c ≤ 9 then 80 else (if c ≤ 10 then 78 else (if c ≤ 11 then 66 else (if c ≤ 13 then 56 else (if c ≤ 14 then 78 else (if c ≤ 15 then 68 else (56))))))))))))))
  | 18 => if c ≤ 0 then 58 else (if c ≤ 3 then 53 else (if c ≤ 4 then 58 else (if c ≤ 8 then 53 else (if c ≤ 9 then 59 else (if c ≤ 10 then 76 else (if c ≤ 11 then 70 else (if c ≤ 12 then 76 else (if c ≤ 13 then 72 else (if c ≤ 14 then 76 else (if c ≤ 15 then 74 else (if c ≤ 16 then 70 else (if c ≤ 17 then 76 else (68)))))))))))))
  | _ => 0

def potential9 (b c : Nat) : Nat :=
  match b with
  | 0 => if c ≤ 9 then 88 else (86)
  | 1 | 2 | 3 | 5 | 6 | 7 | 8 => 86
  | 4 => if c ≤ 8 then 86 else (88)
  | 9 => if c ≤ 9 then 86 else (84)
  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 => 84
  | _ => 0

def potential10 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 => 42
  | _ => 0

def potential11 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 9 | 10 => 43
  | 2 | 11 => if c ≤ 6 then 43 else (if c ≤ 7 then 48 else (if c ≤ 15 then 43 else (if c ≤ 16 then 48 else (43))))
  | 3 => if c ≤ 0 then 48 else (if c ≤ 1 then 50 else (if c ≤ 9 then 48 else (if c ≤ 10 then 50 else (48))))
  | 4 => if c ≤ 0 then 50 else (48)
  | 5 => if c ≤ 2 then 48 else (if c ≤ 9 then 46 else (if c ≤ 11 then 48 else (46)))
  | 6 | 15 => 46
  | 7 => if c ≤ 2 then 46 else (if c ≤ 9 then 42 else (if c ≤ 11 then 46 else (42)))
  | 8 | 17 | 18 => 42
  | 12 => if c ≤ 0 then 48 else (if c ≤ 1 then 50 else (if c ≤ 8 then 48 else (if c ≤ 10 then 50 else (48))))
  | 13 => if c ≤ 0 then 50 else (if c ≤ 8 then 48 else (if c ≤ 9 then 50 else (48)))
  | 14 => if c ≤ 2 then 48 else (if c ≤ 8 then 46 else (if c ≤ 11 then 48 else (46)))
  | 16 => if c ≤ 2 then 46 else (if c ≤ 8 then 42 else (if c ≤ 11 then 46 else (42)))
  | _ => 0

def potential12 (b c : Nat) : Nat :=
  match b with
  | 0 | 7 | 8 | 9 | 16 | 17 | 18 => 43
  | 1 | 10 => if c ≤ 7 then 43 else (if c ≤ 8 then 45 else (if c ≤ 16 then 43 else (if c ≤ 17 then 45 else (43))))
  | 2 | 11 => 45
  | 3 => if c ≤ 1 then 45 else (if c ≤ 6 then 50 else (if c ≤ 7 then 52 else (if c ≤ 8 then 50 else (if c ≤ 9 then 52 else (if c ≤ 10 then 45 else (if c ≤ 15 then 50 else (if c ≤ 16 then 52 else (if c ≤ 17 then 50 else (52)))))))))
  | 4 => if c ≤ 0 then 50 else (45)
  | 5 => if c ≤ 3 then 45 else (if c ≤ 6 then 50 else (if c ≤ 7 then 45 else (if c ≤ 8 then 50 else (if c ≤ 9 then 52 else (if c ≤ 12 then 45 else (if c ≤ 15 then 50 else (if c ≤ 16 then 45 else (50))))))))
  | 6 => if c ≤ 0 then 50 else (if c ≤ 1 then 52 else (if c ≤ 3 then 50 else (if c ≤ 7 then 43 else (if c ≤ 9 then 45 else (if c ≤ 10 then 52 else (if c ≤ 12 then 50 else (if c ≤ 16 then 43 else (45))))))))
  | 12 => if c ≤ 1 then 45 else (if c ≤ 6 then 50 else (if c ≤ 7 then 52 else (if c ≤ 8 then 50 else (if c ≤ 10 then 45 else (if c ≤ 15 then 50 else (if c ≤ 16 then 52 else (if c ≤ 17 then 50 else (52))))))))
  | 13 => if c ≤ 0 then 50 else (if c ≤ 8 then 45 else (if c ≤ 9 then 50 else (45)))
  | 14 => if c ≤ 3 then 45 else (if c ≤ 6 then 50 else (if c ≤ 7 then 45 else (if c ≤ 8 then 50 else (if c ≤ 12 then 45 else (if c ≤ 15 then 50 else (if c ≤ 16 then 45 else (50)))))))
  | 15 => if c ≤ 0 then 50 else (if c ≤ 1 then 52 else (if c ≤ 3 then 50 else (if c ≤ 7 then 43 else (if c ≤ 8 then 45 else (if c ≤ 10 then 52 else (if c ≤ 12 then 50 else (if c ≤ 16 then 43 else (45))))))))
  | _ => 0

def potential13 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 4 | 9 | 10 | 11 | 12 | 13 => 83
  | 5 => if c ≤ 3 then 83 else (if c ≤ 9 then 88 else (if c ≤ 12 then 83 else (88)))
  | 6 | 15 => if c ≤ 2 then 88 else (if c ≤ 3 then 90 else (if c ≤ 11 then 88 else (if c ≤ 12 then 90 else (88))))
  | 7 | 16 | 18 => 88
  | 8 => if c ≤ 1 then 90 else (if c ≤ 9 then 88 else (if c ≤ 10 then 90 else (88)))
  | 14 => if c ≤ 3 then 83 else (if c ≤ 8 then 88 else (if c ≤ 12 then 83 else (88)))
  | 17 => if c ≤ 1 then 90 else (if c ≤ 8 then 88 else (if c ≤ 10 then 90 else (88)))
  | _ => 0

def potential14 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 3 | 9 | 10 | 11 | 12 => 44
  | 4 => if c ≤ 4 then 44 else (if c ≤ 9 then 45 else (if c ≤ 13 then 44 else (45)))
  | 5 | 14 | 18 => 45
  | 6 => if c ≤ 0 then 45 else (if c ≤ 1 then 50 else (if c ≤ 2 then 45 else (if c ≤ 3 then 50 else (if c ≤ 4 then 52 else (if c ≤ 7 then 50 else (if c ≤ 8 then 52 else (if c ≤ 10 then 50 else (if c ≤ 11 then 45 else (if c ≤ 12 then 50 else (if c ≤ 13 then 52 else (if c ≤ 16 then 50 else (if c ≤ 17 then 52 else (50)))))))))))))
  | 7 => if c ≤ 3 then 50 else (if c ≤ 6 then 48 else (if c ≤ 8 then 50 else (if c ≤ 9 then 48 else (if c ≤ 12 then 50 else (if c ≤ 15 then 48 else (if c ≤ 17 then 50 else (48)))))))
  | 8 => if c ≤ 2 then 48 else (if c ≤ 5 then 44 else (if c ≤ 7 then 48 else (if c ≤ 9 then 44 else (if c ≤ 11 then 48 else (if c ≤ 14 then 44 else (if c ≤ 16 then 48 else (44)))))))
  | 13 => if c ≤ 4 then 44 else (if c ≤ 8 then 45 else (if c ≤ 13 then 44 else (45)))
  | 15 => if c ≤ 0 then 45 else (if c ≤ 1 then 50 else (if c ≤ 2 then 45 else (if c ≤ 3 then 50 else (if c ≤ 4 then 52 else (if c ≤ 7 then 50 else (if c ≤ 8 then 52 else (if c ≤ 9 then 45 else (if c ≤ 10 then 50 else (if c ≤ 11 then 45 else (if c ≤ 12 then 50 else (if c ≤ 13 then 52 else (if c ≤ 16 then 50 else (if c ≤ 17 then 52 else (50))))))))))))))
  | 16 => if c ≤ 3 then 50 else (if c ≤ 6 then 48 else (if c ≤ 12 then 50 else (if c ≤ 15 then 48 else (if c ≤ 17 then 50 else (48)))))
  | 17 => if c ≤ 2 then 48 else (if c ≤ 5 then 44 else (if c ≤ 7 then 48 else (if c ≤ 8 then 44 else (if c ≤ 11 then 48 else (if c ≤ 14 then 44 else (if c ≤ 16 then 48 else (44)))))))
  | _ => 0

def potential15 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 2 | 9 | 10 | 11 => 83
  | 3 => if c ≤ 5 then 83 else (if c ≤ 9 then 85 else (if c ≤ 14 then 83 else (85)))
  | 4 | 5 | 13 | 14 | 18 => 85
  | 6 => if c ≤ 4 then 85 else (if c ≤ 9 then 90 else (if c ≤ 13 then 85 else (if c ≤ 17 then 90 else (85))))
  | 7 | 16 => 90
  | 8 => if c ≤ 1 then 90 else (if c ≤ 9 then 85 else (if c ≤ 10 then 90 else (85)))
  | 12 => if c ≤ 5 then 83 else (if c ≤ 8 then 85 else (if c ≤ 14 then 83 else (85)))
  | 15 => if c ≤ 4 then 85 else (if c ≤ 8 then 90 else (if c ≤ 13 then 85 else (if c ≤ 17 then 90 else (85))))
  | 17 => if c ≤ 1 then 90 else (if c ≤ 8 then 85 else (if c ≤ 10 then 90 else (85)))
  | _ => 0

def potential16 (b c : Nat) : Nat :=
  match b with
  | 0 | 1 | 9 | 10 => 83
  | 2 => if c ≤ 6 then 83 else (if c ≤ 9 then 85 else (if c ≤ 15 then 83 else (85)))
  | 3 | 8 | 12 | 17 => 85
  | 4 => if c ≤ 7 then 85 else (if c ≤ 9 then 87 else (if c ≤ 16 then 85 else (87)))
  | 5 | 14 | 18 => 87
  | 6 | 15 => 92
  | 7 => if c ≤ 2 then 87 else (if c ≤ 9 then 85 else (if c ≤ 11 then 87 else (85)))
  | 11 => if c ≤ 6 then 83 else (if c ≤ 8 then 85 else (if c ≤ 15 then 83 else (85)))
  | 13 => if c ≤ 7 then 85 else (if c ≤ 8 then 87 else (if c ≤ 16 then 85 else (87)))
  | 16 => if c ≤ 2 then 87 else (if c ≤ 8 then 85 else (if c ≤ 11 then 87 else (85)))
  | _ => 0

def potential17 (b c : Nat) : Nat :=
  match b with
  | 0 => if c ≤ 1 then 89 else (if c ≤ 3 then 87 else (if c ≤ 5 then 89 else (if c ≤ 9 then 87 else (if c ≤ 10 then 89 else (if c ≤ 12 then 87 else (if c ≤ 14 then 89 else (87)))))))
  | 1 => if c ≤ 7 then 89 else (if c ≤ 9 then 96 else (if c ≤ 16 then 89 else (96)))
  | 2 | 11 => if c ≤ 0 then 91 else (if c ≤ 1 then 89 else (if c ≤ 2 then 91 else (if c ≤ 3 then 89 else (if c ≤ 4 then 91 else (if c ≤ 6 then 89 else (if c ≤ 9 then 91 else (if c ≤ 10 then 89 else (if c ≤ 11 then 91 else (if c ≤ 12 then 89 else (if c ≤ 13 then 91 else (if c ≤ 15 then 89 else (91))))))))))))
  | 3 => if c ≤ 5 then 93 else (if c ≤ 8 then 95 else (if c ≤ 9 then 97 else (if c ≤ 14 then 93 else (if c ≤ 17 then 95 else (97)))))
  | 4 => if c ≤ 0 then 114 else (if c ≤ 1 then 112 else (if c ≤ 2 then 110 else (if c ≤ 3 then 102 else (if c ≤ 4 then 104 else (if c ≤ 5 then 108 else (if c ≤ 7 then 100 else (if c ≤ 9 then 102 else (if c ≤ 10 then 112 else (if c ≤ 11 then 110 else (if c ≤ 12 then 102 else (if c ≤ 13 then 104 else (if c ≤ 14 then 108 else (if c ≤ 16 then 100 else (if c ≤ 17 then 102 else (97)))))))))))))))
  | 5 => if c ≤ 0 then 107 else (if c ≤ 3 then 98 else (if c ≤ 4 then 93 else (if c ≤ 5 then 100 else (if c ≤ 8 then 95 else (if c ≤ 9 then 100 else (if c ≤ 12 then 98 else (if c ≤ 13 then 93 else (if c ≤ 14 then 100 else (if c ≤ 17 then 95 else (100))))))))))
  | 6 => if c ≤ 0 then 112 else (if c ≤ 1 then 118 else (if c ≤ 2 then 108 else (if c ≤ 3 then 106 else (if c ≤ 8 then 96 else (if c ≤ 9 then 91 else (if c ≤ 10 then 118 else (if c ≤ 11 then 107 else (if c ≤ 12 then 106 else (if c ≤ 17 then 96 else (89))))))))))
  | 7 => if c ≤ 0 then 91 else (if c ≤ 1 then 98 else (if c ≤ 4 then 93 else (if c ≤ 5 then 91 else (if c ≤ 9 then 93 else (if c ≤ 10 then 98 else (if c ≤ 13 then 93 else (if c ≤ 14 then 91 else (93))))))))
  | 8 => if c ≤ 0 then 99 else (if c ≤ 1 then 116 else (if c ≤ 2 then 114 else (if c ≤ 3 then 106 else (if c ≤ 4 then 110 else (if c ≤ 5 then 104 else (if c ≤ 6 then 116 else (if c ≤ 7 then 112 else (if c ≤ 8 then 108 else (if c ≤ 9 then 104 else (if c ≤ 10 then 116 else (if c ≤ 11 then 114 else (if c ≤ 12 then 106 else (if c ≤ 13 then 110 else (if c ≤ 14 then 104 else (if c ≤ 15 then 116 else (if c ≤ 16 then 112 else (if c ≤ 17 then 107 else (102))))))))))))))))))
  | 9 => if c ≤ 9 then 94 else (if c ≤ 10 then 89 else (if c ≤ 12 then 87 else (if c ≤ 14 then 89 else (87))))
  | 10 => if c ≤ 7 then 89 else (if c ≤ 8 then 96 else (if c ≤ 16 then 89 else (96)))
  | 12 => if c ≤ 5 then 93 else (if c ≤ 8 then 95 else (if c ≤ 14 then 93 else (if c ≤ 17 then 95 else (97))))
  | 13 => if c ≤ 0 then 114 else (if c ≤ 1 then 112 else (if c ≤ 2 then 110 else (if c ≤ 3 then 102 else (if c ≤ 4 then 104 else (if c ≤ 5 then 108 else (if c ≤ 7 then 100 else (if c ≤ 8 then 102 else (if c ≤ 9 then 114 else (if c ≤ 10 then 112 else (if c ≤ 11 then 110 else (if c ≤ 12 then 102 else (if c ≤ 13 then 104 else (if c ≤ 14 then 107 else (if c ≤ 16 then 100 else (if c ≤ 17 then 102 else (97))))))))))))))))
  | 14 => if c ≤ 0 then 108 else (if c ≤ 3 then 98 else (if c ≤ 4 then 93 else (if c ≤ 5 then 100 else (if c ≤ 8 then 95 else (if c ≤ 9 then 120 else (if c ≤ 12 then 98 else (if c ≤ 13 then 93 else (if c ≤ 14 then 100 else (if c ≤ 17 then 95 else (100))))))))))
  | 15 => if c ≤ 0 then 112 else (if c ≤ 1 then 118 else (if c ≤ 2 then 108 else (if c ≤ 3 then 106 else (if c ≤ 8 then 96 else (if c ≤ 9 then 116 else (if c ≤ 10 then 118 else (if c ≤ 11 then 108 else (if c ≤ 12 then 106 else (if c ≤ 17 then 96 else (89))))))))))
  | 16 => if c ≤ 0 then 91 else (if c ≤ 1 then 98 else (if c ≤ 4 then 93 else (if c ≤ 5 then 91 else (if c ≤ 8 then 93 else (if c ≤ 9 then 91 else (if c ≤ 10 then 98 else (if c ≤ 13 then 93 else (if c ≤ 14 then 91 else (93)))))))))
  | 17 => if c ≤ 0 then 99 else (if c ≤ 1 then 116 else (if c ≤ 2 then 114 else (if c ≤ 3 then 106 else (if c ≤ 4 then 110 else (if c ≤ 5 then 104 else (if c ≤ 6 then 116 else (if c ≤ 7 then 112 else (if c ≤ 8 then 108 else (if c ≤ 9 then 99 else (if c ≤ 10 then 116 else (if c ≤ 11 then 114 else (if c ≤ 12 then 106 else (if c ≤ 13 then 110 else (if c ≤ 14 then 104 else (if c ≤ 15 then 116 else (if c ≤ 16 then 112 else (if c ≤ 17 then 108 else (102))))))))))))))))))
  | 18 => if c ≤ 0 then 122 else (if c ≤ 1 then 120 else (if c ≤ 2 then 108 else (if c ≤ 4 then 98 else (if c ≤ 5 then 120 else (if c ≤ 6 then 110 else (if c ≤ 8 then 98 else (if c ≤ 9 then 122 else (if c ≤ 10 then 120 else (if c ≤ 11 then 108 else (if c ≤ 13 then 98 else (if c ≤ 14 then 120 else (if c ≤ 15 then 110 else (98)))))))))))))
  | _ => 0

def potential18 (b c : Nat) : Nat :=
  match b with
  | 0 | 9 => 128
  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 => 126
  | _ => 0

def potential (s : Prefix) : Nat :=
  match s.a with
  | 1 => potential1 s.b s.c
  | 2 => potential2 s.b s.c
  | 3 => potential3 s.b s.c
  | 4 => potential4 s.b s.c
  | 5 => potential5 s.b s.c
  | 6 => potential6 s.b s.c
  | 7 => potential7 s.b s.c
  | 8 => potential8 s.b s.c
  | 9 => potential9 s.b s.c
  | 10 => potential10 s.b s.c
  | 11 => potential11 s.b s.c
  | 12 => potential12 s.b s.c
  | 13 => potential13 s.b s.c
  | 14 => potential14 s.b s.c
  | 15 => potential15 s.b s.c
  | 16 => potential16 s.b s.c
  | 17 => potential17 s.b s.c
  | 18 => potential18 s.b s.c
  | _ => 0

def clock (s : Prefix) : Nat :=
  match s.a, s.b, s.c with
  | 8, 12, 9 => 0
  | 17, 5, 0 => 1
  | 8, 13, 5 => 2
  | 17, 6, 11 => 3
  | 8, 14, 8 => 4
  | 17, 8, 17 => 5
  | 8, 16, 16 => 6
  | 17, 13, 14 => 7
  | _, _, _ => 0

def Check (a b c e : Nat) : Prop :=
  let s : Prefix := ⟨a,b,c⟩
  let out := advance s e
  82*out.2 + potential out.1 ≤ 41 + potential s ∧
    (82*out.2 + potential out.1 = 41 + potential s →
      clock out.1 = (clock s + 1) % 8)

instance (a b c e : Nat) : Decidable (Check a b c e) := inferInstanceAs
  (Decidable (82*(advance ⟨a,b,c⟩ e).2 + potential (advance ⟨a,b,c⟩ e).1 ≤
      41 + potential ⟨a,b,c⟩ ∧
    (82*(advance ⟨a,b,c⟩ e).2 + potential (advance ⟨a,b,c⟩ e).1 =
      41 + potential ⟨a,b,c⟩ →
      clock (advance ⟨a,b,c⟩ e).1 = (clock ⟨a,b,c⟩ + 1) % 8)))

set_option maxRecDepth 100000
set_option maxHeartbeats 50000000


end P196.Agent4.Saturation

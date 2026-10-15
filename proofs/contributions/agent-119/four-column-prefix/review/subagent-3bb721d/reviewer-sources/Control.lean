namespace Ctl
def roots (a : Nat) : List (List Nat) := (List.range 10).map (fun d => [a, d])
def f : Nat → Nat
  | 0 => 0
  | n + 1 => f n + 2
end Ctl

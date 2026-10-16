import OddCounts
open P196.Agent9.InverseFibers
open P196.Agent7.OddFibers

-- Zero half-width has one positive canonical coefficient witness.
example : oddPreimages [] (2 : Fin 10) 0 = [([], 2)] := by decide
example : oddMax 0 = 1 := by decide

-- An incompatible odd middle digit has no zero-carry single-column predecessor.
example : oddPreimages [] (1 : Fin 10) 0 = [] := by decide

-- The positive attaining family counts distinct coefficient words, not centers twice.
example : oddPreimages [11] (0 : Fin 10) 0 = [([5], 10)] := by decide
example : oddPreimages [11] (1 : Fin 10) 0 = [] := by decide

#print axioms odd_count_bound
#print axioms odd_preimages_length
#print axioms odd_preimages_bound
#print axioms leading_eleven_odd_sharp
#print axioms leading_eleven_odd_positive
#print axioms odd_preimages_center_parity

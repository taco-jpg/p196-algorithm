import PrefixInverse

/- Runtime diagnostic only. The accepted inverse theorem is kernel checked
   in PrefixInverse. This executable does not replace that theorem. -/
def showWord (w : List Nat) : String := String.intercalate "," (w.map toString)

def main (args : List String) : IO Unit := do
  let input ← IO.FS.readFile (args[0]!)
  let mut lines : Array String := #[]
  for line in input.splitOn "\n" do
    if !line.isEmpty then
      let p := (line.splitOn ",").map String.toNat!
      let qs := SevenColumn.prefixPredecessors p
      lines := lines.push (showWord p ++ "=" ++ String.intercalate ";" (qs.map showWord))
  IO.FS.writeFile (args[1]!) (String.intercalate "\n" lines.toList ++ "\n")

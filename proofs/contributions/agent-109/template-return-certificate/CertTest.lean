import ReturnCertificate
open Agent109 Agent109.Cert
def demo : Certificate :=
  { states := [⟨2, [1], [3], [4]⟩, ⟨4, [3, 5], [1], [2,2]⟩],
    links := [⟨0,0,0,0,5,5⟩, ⟨0,0,0,0,5,5⟩] }
#eval check demo
#eval (data 2 [1] [3] [4]).γ
#eval Br 2 [1] [3] [4]
#eval decide (StepPal 2 [1] [3] [4])
example : check demo = false := by decide

import ReturnCertificate
open Agent109.Cert

def cert : Certificate :=
  { states := [
    ⟨2, [1], [3], [4]⟩,
    ⟨4, [3, 5], [1], [2, 2]⟩],
    links := [
    ⟨0, 0, 0, 0, 5, 5⟩,
    ⟨0, 0, 0, 0, 5, 5⟩] }

#eval check cert

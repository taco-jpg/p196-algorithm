import Agent102ParameterIntervalCompact

/- 仅用于本地证据的具体规模控制，不增加冻结数学模块的接口。 -/
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000

namespace Agent102.ParameterSets.CompactControls

theorem empty_128 :
    fastComplement (List.replicate 128 Interval.empty) = univ := by
  decide

theorem reversed_128 :
    fastComplement (List.replicate 128 (⟨5, some 3⟩ : Interval)) = univ := by
  decide

theorem mixed_128 :
    fastComplement
      ([⟨1, some 3⟩] ++ List.replicate 128 Interval.empty ++
        [⟨4, some 6⟩] ++ List.replicate 128 (⟨5, some 3⟩ : Interval)) =
      [⟨0, some 1⟩, ⟨3, some 4⟩, ⟨6, none⟩] := by
  decide

end Agent102.ParameterSets.CompactControls

#print axioms Agent102.ParameterSets.CompactControls.empty_128
#print axioms Agent102.ParameterSets.CompactControls.reversed_128
#print axioms Agent102.ParameterSets.CompactControls.mixed_128

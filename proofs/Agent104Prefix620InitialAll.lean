/- Agent #104 finite-list partition of the frozen 620 instance.
Agent #124's original semantic checker and enumerations are unchanged. -/
import Agent104Prefix620InitialCoverage
import Agent104Prefix620Initial000
import Agent104Prefix620Initial001
import Agent104Prefix620Initial002
import Agent104Prefix620Initial003
import Agent104Prefix620Initial004
import Agent104Prefix620Initial005
import Agent104Prefix620Initial006
import Agent104Prefix620Initial007
import Agent104Prefix620Initial008
import Agent104Prefix620Initial009
import Agent104Prefix620Initial010
import Agent104Prefix620Initial011
import Agent104Prefix620Initial012
import Agent104Prefix620Initial013
import Agent104Prefix620Initial014
import Agent104Prefix620Initial015
import Agent104Prefix620Initial016
import Agent104Prefix620Initial017
import Agent104Prefix620Initial018
import Agent104Prefix620Initial019
import Agent104Prefix620Initial020
import Agent104Prefix620Initial021
import Agent104Prefix620Initial022
import Agent104Prefix620Initial023
import Agent104Prefix620Initial024
import Agent104Prefix620Initial025
import Agent104Prefix620Initial026
import Agent104Prefix620Initial027
import Agent104Prefix620Initial028
import Agent104Prefix620Initial029
import Agent104Prefix620Initial030
import Agent104Prefix620Initial031
import Agent104Prefix620Initial032
import Agent104Prefix620Initial033
import Agent104Prefix620Initial034
import Agent104Prefix620Initial035
import Agent104Prefix620Initial036
import Agent104Prefix620Initial037
import Agent104Prefix620Initial038
import Agent104Prefix620Initial039
import Agent104Prefix620Initial040
import Agent104Prefix620Initial041
import Agent104Prefix620Initial042
import Agent104Prefix620Initial043
import Agent104Prefix620Initial044
import Agent104Prefix620Initial045
import Agent104Prefix620Initial046
import Agent104Prefix620Initial047
import Agent104Prefix620Initial048
import Agent104Prefix620Initial049
import Agent104Prefix620Initial050
import Agent104Prefix620Initial051
import Agent104Prefix620Initial052
import Agent104Prefix620Initial053
import Agent104Prefix620Initial054
import Agent104Prefix620Initial055
import Agent104Prefix620Initial056
import Agent104Prefix620Initial057
import Agent104Prefix620Initial058
import Agent104Prefix620Initial059
import Agent104Prefix620Initial060
import Agent104Prefix620Initial061
import Agent104Prefix620Initial062
import Agent104Prefix620Initial063
import Agent104Prefix620Initial064
import Agent104Prefix620Initial065
import Agent104Prefix620Initial066
import Agent104Prefix620Initial067
import Agent104Prefix620Initial068
import Agent104Prefix620Initial069
import Agent104Prefix620Initial070
import Agent104Prefix620Initial071
import Agent104Prefix620Initial072
import Agent104Prefix620Initial073
import Agent104Prefix620Initial074
import Agent104Prefix620Initial075
import Agent104Prefix620Initial076
import Agent104Prefix620Initial077
import Agent104Prefix620Initial078
import Agent104Prefix620Initial079
import Agent104Prefix620Initial080
import Agent104Prefix620Initial081
import Agent104Prefix620Initial082
import Agent104Prefix620Initial083
import Agent104Prefix620Initial084
import Agent104Prefix620Initial085
import Agent104Prefix620Initial086
import Agent104Prefix620Initial087
import Agent104Prefix620Initial088
import Agent104Prefix620Initial089
import Agent104Prefix620Initial090
import Agent104Prefix620Initial091
import Agent104Prefix620Initial092
import Agent104Prefix620Initial093
import Agent104Prefix620Initial094
import Agent104Prefix620Initial095
import Agent104Prefix620Initial096
import Agent104Prefix620Initial097
import Agent104Prefix620Initial098
import Agent104Prefix620Initial099
import Agent104Prefix620Initial100

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem init_620 : (initialWordsK 7 6 2 0).all (initOKC ranks 11) = true := by
  apply initial_all_of_slices (initOKC ranks 11)
  · rw [initial_cover_short]
    exact initial_ok000
  · intro a ha b hb
    have ha10 : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 := by omega
    have hb10 : b = 0 ∨ b = 1 ∨ b = 2 ∨ b = 3 ∨ b = 4 ∨ b = 5 ∨ b = 6 ∨ b = 7 ∨ b = 8 ∨ b = 9 := by omega
    rcases ha10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_0_0]
        exact initial_ok001
      · rw [initial_cover_0_1]
        exact initial_ok002
      · rw [initial_cover_0_2]
        exact initial_ok003
      · rw [initial_cover_0_3]
        exact initial_ok004
      · rw [initial_cover_0_4]
        exact initial_ok005
      · rw [initial_cover_0_5]
        exact initial_ok006
      · rw [initial_cover_0_6]
        exact initial_ok007
      · rw [initial_cover_0_7]
        exact initial_ok008
      · rw [initial_cover_0_8]
        exact initial_ok009
      · rw [initial_cover_0_9]
        exact initial_ok010
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_1_0]
        exact initial_ok011
      · rw [initial_cover_1_1]
        exact initial_ok012
      · rw [initial_cover_1_2]
        exact initial_ok013
      · rw [initial_cover_1_3]
        exact initial_ok014
      · rw [initial_cover_1_4]
        exact initial_ok015
      · rw [initial_cover_1_5]
        exact initial_ok016
      · rw [initial_cover_1_6]
        exact initial_ok017
      · rw [initial_cover_1_7]
        exact initial_ok018
      · rw [initial_cover_1_8]
        exact initial_ok019
      · rw [initial_cover_1_9]
        exact initial_ok020
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_2_0]
        exact initial_ok021
      · rw [initial_cover_2_1]
        exact initial_ok022
      · rw [initial_cover_2_2]
        exact initial_ok023
      · rw [initial_cover_2_3]
        exact initial_ok024
      · rw [initial_cover_2_4]
        exact initial_ok025
      · rw [initial_cover_2_5]
        exact initial_ok026
      · rw [initial_cover_2_6]
        exact initial_ok027
      · rw [initial_cover_2_7]
        exact initial_ok028
      · rw [initial_cover_2_8]
        exact initial_ok029
      · rw [initial_cover_2_9]
        exact initial_ok030
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_3_0]
        exact initial_ok031
      · rw [initial_cover_3_1]
        exact initial_ok032
      · rw [initial_cover_3_2]
        exact initial_ok033
      · rw [initial_cover_3_3]
        exact initial_ok034
      · rw [initial_cover_3_4]
        exact initial_ok035
      · rw [initial_cover_3_5]
        exact initial_ok036
      · rw [initial_cover_3_6]
        exact initial_ok037
      · rw [initial_cover_3_7]
        exact initial_ok038
      · rw [initial_cover_3_8]
        exact initial_ok039
      · rw [initial_cover_3_9]
        exact initial_ok040
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_4_0]
        exact initial_ok041
      · rw [initial_cover_4_1]
        exact initial_ok042
      · rw [initial_cover_4_2]
        exact initial_ok043
      · rw [initial_cover_4_3]
        exact initial_ok044
      · rw [initial_cover_4_4]
        exact initial_ok045
      · rw [initial_cover_4_5]
        exact initial_ok046
      · rw [initial_cover_4_6]
        exact initial_ok047
      · rw [initial_cover_4_7]
        exact initial_ok048
      · rw [initial_cover_4_8]
        exact initial_ok049
      · rw [initial_cover_4_9]
        exact initial_ok050
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_5_0]
        exact initial_ok051
      · rw [initial_cover_5_1]
        exact initial_ok052
      · rw [initial_cover_5_2]
        exact initial_ok053
      · rw [initial_cover_5_3]
        exact initial_ok054
      · rw [initial_cover_5_4]
        exact initial_ok055
      · rw [initial_cover_5_5]
        exact initial_ok056
      · rw [initial_cover_5_6]
        exact initial_ok057
      · rw [initial_cover_5_7]
        exact initial_ok058
      · rw [initial_cover_5_8]
        exact initial_ok059
      · rw [initial_cover_5_9]
        exact initial_ok060
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_6_0]
        exact initial_ok061
      · rw [initial_cover_6_1]
        exact initial_ok062
      · rw [initial_cover_6_2]
        exact initial_ok063
      · rw [initial_cover_6_3]
        exact initial_ok064
      · rw [initial_cover_6_4]
        exact initial_ok065
      · rw [initial_cover_6_5]
        exact initial_ok066
      · rw [initial_cover_6_6]
        exact initial_ok067
      · rw [initial_cover_6_7]
        exact initial_ok068
      · rw [initial_cover_6_8]
        exact initial_ok069
      · rw [initial_cover_6_9]
        exact initial_ok070
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_7_0]
        exact initial_ok071
      · rw [initial_cover_7_1]
        exact initial_ok072
      · rw [initial_cover_7_2]
        exact initial_ok073
      · rw [initial_cover_7_3]
        exact initial_ok074
      · rw [initial_cover_7_4]
        exact initial_ok075
      · rw [initial_cover_7_5]
        exact initial_ok076
      · rw [initial_cover_7_6]
        exact initial_ok077
      · rw [initial_cover_7_7]
        exact initial_ok078
      · rw [initial_cover_7_8]
        exact initial_ok079
      · rw [initial_cover_7_9]
        exact initial_ok080
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_8_0]
        exact initial_ok081
      · rw [initial_cover_8_1]
        exact initial_ok082
      · rw [initial_cover_8_2]
        exact initial_ok083
      · rw [initial_cover_8_3]
        exact initial_ok084
      · rw [initial_cover_8_4]
        exact initial_ok085
      · rw [initial_cover_8_5]
        exact initial_ok086
      · rw [initial_cover_8_6]
        exact initial_ok087
      · rw [initial_cover_8_7]
        exact initial_ok088
      · rw [initial_cover_8_8]
        exact initial_ok089
      · rw [initial_cover_8_9]
        exact initial_ok090
    · rcases hb10 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
      · rw [initial_cover_9_0]
        exact initial_ok091
      · rw [initial_cover_9_1]
        exact initial_ok092
      · rw [initial_cover_9_2]
        exact initial_ok093
      · rw [initial_cover_9_3]
        exact initial_ok094
      · rw [initial_cover_9_4]
        exact initial_ok095
      · rw [initial_cover_9_5]
        exact initial_ok096
      · rw [initial_cover_9_6]
        exact initial_ok097
      · rw [initial_cover_9_7]
        exact initial_ok098
      · rw [initial_cover_9_8]
        exact initial_ok099
      · rw [initial_cover_9_9]
        exact initial_ok100

theorem initialBounded : InitialBounded 7 6 2 0 11 (R ranks) :=
  initialBounded_of_all init_620

#print axioms init_620
#print axioms initialBounded

end Agent104.Prefix620

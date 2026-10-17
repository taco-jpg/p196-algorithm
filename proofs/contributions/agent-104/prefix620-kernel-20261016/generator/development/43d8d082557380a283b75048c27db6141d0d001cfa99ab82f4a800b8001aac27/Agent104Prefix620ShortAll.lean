/- Agent #104 finite-list partition of the frozen 620 instance.
Agent #124's original semantic checker and enumerations are unchanged. -/
import Agent104Prefix620ShortCoverage
import Agent104Prefix620Short000
import Agent104Prefix620Short001
import Agent104Prefix620Short002
import Agent104Prefix620Short003
import Agent104Prefix620Short004
import Agent104Prefix620Short005
import Agent104Prefix620Short006
import Agent104Prefix620Short007
import Agent104Prefix620Short008
import Agent104Prefix620Short009
import Agent104Prefix620Short010
import Agent104Prefix620Short011
import Agent104Prefix620Short012
import Agent104Prefix620Short013
import Agent104Prefix620Short014
import Agent104Prefix620Short015
import Agent104Prefix620Short016
import Agent104Prefix620Short017
import Agent104Prefix620Short018
import Agent104Prefix620Short019
import Agent104Prefix620Short020
import Agent104Prefix620Short021
import Agent104Prefix620Short022
import Agent104Prefix620Short023
import Agent104Prefix620Short024
import Agent104Prefix620Short025
import Agent104Prefix620Short026
import Agent104Prefix620Short027
import Agent104Prefix620Short028
import Agent104Prefix620Short029
import Agent104Prefix620Short030
import Agent104Prefix620Short031
import Agent104Prefix620Short032
import Agent104Prefix620Short033
import Agent104Prefix620Short034
import Agent104Prefix620Short035
import Agent104Prefix620Short036
import Agent104Prefix620Short037
import Agent104Prefix620Short038
import Agent104Prefix620Short039
import Agent104Prefix620Short040
import Agent104Prefix620Short041
import Agent104Prefix620Short042
import Agent104Prefix620Short043
import Agent104Prefix620Short044
import Agent104Prefix620Short045
import Agent104Prefix620Short046
import Agent104Prefix620Short047
import Agent104Prefix620Short048
import Agent104Prefix620Short049
import Agent104Prefix620Short050
import Agent104Prefix620Short051
import Agent104Prefix620Short052
import Agent104Prefix620Short053
import Agent104Prefix620Short054
import Agent104Prefix620Short055
import Agent104Prefix620Short056
import Agent104Prefix620Short057
import Agent104Prefix620Short058
import Agent104Prefix620Short059
import Agent104Prefix620Short060
import Agent104Prefix620Short061
import Agent104Prefix620Short062
import Agent104Prefix620Short063
import Agent104Prefix620Short064
import Agent104Prefix620Short065
import Agent104Prefix620Short066
import Agent104Prefix620Short067
import Agent104Prefix620Short068
import Agent104Prefix620Short069
import Agent104Prefix620Short070
import Agent104Prefix620Short071
import Agent104Prefix620Short072
import Agent104Prefix620Short073
import Agent104Prefix620Short074
import Agent104Prefix620Short075
import Agent104Prefix620Short076
import Agent104Prefix620Short077

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem short_w0 : (symWords 0).all (shortOKC ranks) = true := by
  decide +kernel

theorem short_w1 : (symWords 1).all (shortOKC ranks) = true := by
  rw [short_cover_w1]
  exact short_ok000

theorem short_w2 : (symWords 2).all (shortOKC ranks) = true := by
  rw [short_cover_w2]
  exact short_ok001

theorem short_w3 : (symWords 3).all (shortOKC ranks) = true := by
  apply short_all_of_slices (shortOKC ranks) 3 1 (by decide +kernel)
  intro a ha
  have ha19 : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases ha19 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [short_cover_w3_0]
    exact short_ok002
  · rw [short_cover_w3_1]
    exact short_ok003
  · rw [short_cover_w3_2]
    exact short_ok004
  · rw [short_cover_w3_3]
    exact short_ok005
  · rw [short_cover_w3_4]
    exact short_ok006
  · rw [short_cover_w3_5]
    exact short_ok007
  · rw [short_cover_w3_6]
    exact short_ok008
  · rw [short_cover_w3_7]
    exact short_ok009
  · rw [short_cover_w3_8]
    exact short_ok010
  · rw [short_cover_w3_9]
    exact short_ok011
  · rw [short_cover_w3_10]
    exact short_ok012
  · rw [short_cover_w3_11]
    exact short_ok013
  · rw [short_cover_w3_12]
    exact short_ok014
  · rw [short_cover_w3_13]
    exact short_ok015
  · rw [short_cover_w3_14]
    exact short_ok016
  · rw [short_cover_w3_15]
    exact short_ok017
  · rw [short_cover_w3_16]
    exact short_ok018
  · rw [short_cover_w3_17]
    exact short_ok019
  · rw [short_cover_w3_18]
    exact short_ok020

theorem short_w4 : (symWords 4).all (shortOKC ranks) = true := by
  apply short_all_of_slices (shortOKC ranks) 4 1 (by decide +kernel)
  intro a ha
  have ha19 : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases ha19 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [short_cover_w4_0]
    exact short_ok021
  · rw [short_cover_w4_1]
    exact short_ok022
  · rw [short_cover_w4_2]
    exact short_ok023
  · rw [short_cover_w4_3]
    exact short_ok024
  · rw [short_cover_w4_4]
    exact short_ok025
  · rw [short_cover_w4_5]
    exact short_ok026
  · rw [short_cover_w4_6]
    exact short_ok027
  · rw [short_cover_w4_7]
    exact short_ok028
  · rw [short_cover_w4_8]
    exact short_ok029
  · rw [short_cover_w4_9]
    exact short_ok030
  · rw [short_cover_w4_10]
    exact short_ok031
  · rw [short_cover_w4_11]
    exact short_ok032
  · rw [short_cover_w4_12]
    exact short_ok033
  · rw [short_cover_w4_13]
    exact short_ok034
  · rw [short_cover_w4_14]
    exact short_ok035
  · rw [short_cover_w4_15]
    exact short_ok036
  · rw [short_cover_w4_16]
    exact short_ok037
  · rw [short_cover_w4_17]
    exact short_ok038
  · rw [short_cover_w4_18]
    exact short_ok039

theorem short_w5 : (symWords 5).all (shortOKC ranks) = true := by
  apply short_all_of_slices (shortOKC ranks) 5 2 (by decide +kernel)
  intro a ha
  have ha19 : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases ha19 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [short_cover_w5_0]
    exact short_ok040
  · rw [short_cover_w5_1]
    exact short_ok041
  · rw [short_cover_w5_2]
    exact short_ok042
  · rw [short_cover_w5_3]
    exact short_ok043
  · rw [short_cover_w5_4]
    exact short_ok044
  · rw [short_cover_w5_5]
    exact short_ok045
  · rw [short_cover_w5_6]
    exact short_ok046
  · rw [short_cover_w5_7]
    exact short_ok047
  · rw [short_cover_w5_8]
    exact short_ok048
  · rw [short_cover_w5_9]
    exact short_ok049
  · rw [short_cover_w5_10]
    exact short_ok050
  · rw [short_cover_w5_11]
    exact short_ok051
  · rw [short_cover_w5_12]
    exact short_ok052
  · rw [short_cover_w5_13]
    exact short_ok053
  · rw [short_cover_w5_14]
    exact short_ok054
  · rw [short_cover_w5_15]
    exact short_ok055
  · rw [short_cover_w5_16]
    exact short_ok056
  · rw [short_cover_w5_17]
    exact short_ok057
  · rw [short_cover_w5_18]
    exact short_ok058

theorem short_w6 : (symWords 6).all (shortOKC ranks) = true := by
  apply short_all_of_slices (shortOKC ranks) 6 2 (by decide +kernel)
  intro a ha
  have ha19 : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨ a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨ a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases ha19 with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [short_cover_w6_0]
    exact short_ok059
  · rw [short_cover_w6_1]
    exact short_ok060
  · rw [short_cover_w6_2]
    exact short_ok061
  · rw [short_cover_w6_3]
    exact short_ok062
  · rw [short_cover_w6_4]
    exact short_ok063
  · rw [short_cover_w6_5]
    exact short_ok064
  · rw [short_cover_w6_6]
    exact short_ok065
  · rw [short_cover_w6_7]
    exact short_ok066
  · rw [short_cover_w6_8]
    exact short_ok067
  · rw [short_cover_w6_9]
    exact short_ok068
  · rw [short_cover_w6_10]
    exact short_ok069
  · rw [short_cover_w6_11]
    exact short_ok070
  · rw [short_cover_w6_12]
    exact short_ok071
  · rw [short_cover_w6_13]
    exact short_ok072
  · rw [short_cover_w6_14]
    exact short_ok073
  · rw [short_cover_w6_15]
    exact short_ok074
  · rw [short_cover_w6_16]
    exact short_ok075
  · rw [short_cover_w6_17]
    exact short_ok076
  · rw [short_cover_w6_18]
    exact short_ok077

theorem short : ShortClosed 7 (R ranks) := shortClosed_of_widths fun n hn => by
  have : n = 0 ∨ n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨ n = 6 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact short_w0
  · exact short_w1
  · exact short_w2
  · exact short_w3
  · exact short_w4
  · exact short_w5
  · exact short_w6

#print axioms short

end Agent104.Prefix620

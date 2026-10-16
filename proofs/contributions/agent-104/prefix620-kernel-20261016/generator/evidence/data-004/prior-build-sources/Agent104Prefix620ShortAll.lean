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
import Agent104Prefix620Short078
import Agent104Prefix620Short079
import Agent104Prefix620Short080
import Agent104Prefix620Short081
import Agent104Prefix620Short082
import Agent104Prefix620Short083
import Agent104Prefix620Short084
import Agent104Prefix620Short085
import Agent104Prefix620Short086
import Agent104Prefix620Short087
import Agent104Prefix620Short088
import Agent104Prefix620Short089
import Agent104Prefix620Short090
import Agent104Prefix620Short091
import Agent104Prefix620Short092
import Agent104Prefix620Short093
import Agent104Prefix620Short094
import Agent104Prefix620Short095
import Agent104Prefix620Short096
import Agent104Prefix620Short097
import Agent104Prefix620Short098
import Agent104Prefix620Short099
import Agent104Prefix620Short100
import Agent104Prefix620Short101
import Agent104Prefix620Short102
import Agent104Prefix620Short103
import Agent104Prefix620Short104
import Agent104Prefix620Short105
import Agent104Prefix620Short106
import Agent104Prefix620Short107

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem short_w0 : (symWords 0).all (shortOKC ranks) = true := by
  rw [short_cover_w0]
  rfl

theorem short_w1 : (symWords 1).all (shortOKC ranks) = true := by
  rw [short_cover_w1]
  exact short_ok000

theorem short_w2 : (symWords 2).all (shortOKC ranks) = true := by
  rw [short_cover_w2]
  exact short_ok001

theorem short_w3 : (symWords 3).all (shortOKC ranks) = true := by
  rw [short_cover_w3]
  simp only [List.all_append, short_ok002, short_ok003, Bool.and_self]

theorem short_w4 : (symWords 4).all (shortOKC ranks) = true := by
  rw [short_cover_w4]
  simp only [List.all_append, short_ok004, short_ok005, short_ok006, short_ok007, Bool.and_self]

theorem short_w5 : (symWords 5).all (shortOKC ranks) = true := by
  rw [short_cover_w5]
  simp only [List.all_append, short_ok008, short_ok009, short_ok010, short_ok011, short_ok012, short_ok013, short_ok014, short_ok015, short_ok016, short_ok017, short_ok018, short_ok019, short_ok020, short_ok021, short_ok022, short_ok023, short_ok024, short_ok025, short_ok026, short_ok027, short_ok028, short_ok029, short_ok030, short_ok031, short_ok032, short_ok033, short_ok034, short_ok035, short_ok036, short_ok037, short_ok038, short_ok039, short_ok040, short_ok041, short_ok042, Bool.and_self]

theorem short_w6 : (symWords 6).all (shortOKC ranks) = true := by
  rw [short_cover_w6]
  simp only [List.all_append, short_ok043, short_ok044, short_ok045, short_ok046, short_ok047, short_ok048, short_ok049, short_ok050, short_ok051, short_ok052, short_ok053, short_ok054, short_ok055, short_ok056, short_ok057, short_ok058, short_ok059, short_ok060, short_ok061, short_ok062, short_ok063, short_ok064, short_ok065, short_ok066, short_ok067, short_ok068, short_ok069, short_ok070, short_ok071, short_ok072, short_ok073, short_ok074, short_ok075, short_ok076, short_ok077, short_ok078, short_ok079, short_ok080, short_ok081, short_ok082, short_ok083, short_ok084, short_ok085, short_ok086, short_ok087, short_ok088, short_ok089, short_ok090, short_ok091, short_ok092, short_ok093, short_ok094, short_ok095, short_ok096, short_ok097, short_ok098, short_ok099, short_ok100, short_ok101, short_ok102, short_ok103, short_ok104, short_ok105, short_ok106, short_ok107, Bool.and_self]

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

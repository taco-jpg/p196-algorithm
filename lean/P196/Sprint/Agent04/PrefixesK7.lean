import P196.Sprint.Agent04.Trap

/-!
# Sprint agent 04: width-7 method limits through ONE shared cycle

For each prefix below, an explicit initial word `p0_P ∈ initialWordsL 7 P` reaches the length-7
cycle `Sprint04.cycle7` backward (verified walk `entry_P`).  Hence, for every rank function with
`RowsClosed 7 R` (the interface consumed by `Agent124.PrefixL.entryOK` / `no_196_of_entries`),
`entryOK 7 R (P, bound) = false` for every `bound`: no width-7 certificate of the batch kind exists.

Prefixes: the 13 three-digit prefixes of `Agent117RemainingCycles` other than the lead-one
prefix 112 (138, 164, 198, 248, 275, 398, 626, 710, 716, 790, 911, 936, 952; Agent #117 already proves 275 at width 8, which is
stronger), the 20 four-digit prefixes with the longest delays observed in the sprint's forward scan
(seeds < 10^6, 300 steps) among those with cycles at every width 4..7, and 4456.

Method-limit statements only; nothing here excludes or asserts a palindrome in the orbit of 196.
-/

namespace Sprint04.PrefixesK7

open SevenColumn.Certificate Agent117 Agent124.PrefixR Agent124.PrefixL Sprint04

/-- Prefix 138: initial word `[1, 3, 8, 9, 8, 5, 0]`; 1627 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_138 : List Nat := [9, 8, 5, 0]
def p0_138 : List Nat := [1, 3, 8] ++ tail_138
def entry_138Data : List Nat := [895213673, 1385568292, 608077556, 304038778, 104908547, 993436854, 1390651537, 831675506, 220358484, 192261872, 96137434, 1029353, 894379899, 1363216259, 872645396, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_138 : List (List Nat × Nat) := entry_138Data.map (unpack 7)
theorem entry_138_ok : walkOKk 7 ((p0_138, 0) :: entry_138) = true := by decide +kernel
theorem entry_138_end : (entry_138.getLastD (p0_138, 0)).1 = z7 := by decide +kernel
theorem p0_138_initial : p0_138 ∈ initialWordsL 7 [1, 3, 8] :=
  mem_initialWordsL_of_full 7 [1, 3, 8] tail_138 (by decide) (by decide)
theorem no_certificate_138 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 3, 8], bound) = false :=
  entryOK_false_of_none [1, 3, 8] bound p0_138_initial
    (R_none_of_entry7 rows entry_138 p0_138 0 entry_138_ok entry_138_end)

/-- Prefix 164: initial word `[1, 6, 4, 9, 9, 9, 9]`; 1 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_164 : List Nat := [9, 9, 9, 9]
def p0_164 : List Nat := [1, 6, 4] ++ tail_164
def entry_164Data : List Nat := [893871930, 893868045, 268167510, 89390151, 983260418, 853777906, 1367676252, 604837176, 1196290327, 328099518, 117127341, 950082773, 475164848, 239935042, 950685198, 809671376, 1299873989, 1541339475, 726099595, 1645026518, 797349078, 938443780, 888924443, 864233021, 383904239, 1086989889, 414373946, 1090889046, 325175574, 1103505046, 504836621, 254764430, 1065823736, 768388596, 711175528, 440146854, 1158638410, 1517760744, 1696155844, 804674171, 1378565236, 1588510218, 1777775316, 888887658, 918544786, 879043175, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_164 : List (List Nat × Nat) := entry_164Data.map (unpack 7)
theorem entry_164_ok : walkOKk 7 ((p0_164, 0) :: entry_164) = true := by decide +kernel
theorem entry_164_end : (entry_164.getLastD (p0_164, 0)).1 = z7 := by decide +kernel
theorem p0_164_initial : p0_164 ∈ initialWordsL 7 [1, 6, 4] :=
  mem_initialWordsL_of_full 7 [1, 6, 4] tail_164 (by decide) (by decide)
theorem no_certificate_164 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 6, 4], bound) = false :=
  entryOK_false_of_none [1, 6, 4] bound p0_164_initial
    (R_none_of_entry7 rows entry_164 p0_164 0 entry_164_ok entry_164_end)

/-- Prefix 198: initial word `[1, 9, 8, 6, 6, 0, 0]`; 600 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_198 : List Nat := [6, 6, 0, 0]
def p0_198 : List Nat := [1, 9, 8] ++ tail_198
def entry_198Data : List Nat := [893947855, 892541769, 446745584, 1117244513, 511515005, 1051175974, 478672409, 1180062114, 589969686, 344705886, 1113263704, 559101452, 282019966, 1175886992, 505737078, 923856340, 934863060, 940366438, 893596589, 919733202, 182289412, 982547205, 272595312, 136421460, 905390542, 1393482930, 1408135976, 1597939727, 1737535188, 868767594, 1375301056, 1677603880, 1782236498, 1787468128, 893740904, 919805360, 462248458, 231315920, 905437193, 1383603730, 563155438, 234538337, 1080347874, 518012850, 1175032735, 684461872, 528204844, 252223972, 1019976867, 1448429972, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_198 : List (List Nat × Nat) := entry_198Data.map (unpack 7)
theorem entry_198_ok : walkOKk 7 ((p0_198, 0) :: entry_198) = true := by decide +kernel
theorem entry_198_end : (entry_198.getLastD (p0_198, 0)).1 = z7 := by decide +kernel
theorem p0_198_initial : p0_198 ∈ initialWordsL 7 [1, 9, 8] :=
  mem_initialWordsL_of_full 7 [1, 9, 8] tail_198 (by decide) (by decide)
theorem no_certificate_198 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 9, 8], bound) = false :=
  entryOK_false_of_none [1, 9, 8] bound p0_198_initial
    (R_none_of_entry7 rows entry_198 p0_198 0 entry_198_ok entry_198_end)

/-- Prefix 248: initial word `[2, 4, 8, 6, 0, 0, 0]`; 1336 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_248 : List Nat := [6, 0, 0, 0]
def p0_248 : List Nat := [2, 4, 8] ++ tail_248
def entry_248Data : List Nat := [44120, 893873603, 893876442, 893870319, 400019239, 918564292, 879056177, 1380435618, 1584092779, 1775091360, 893245992, 867566685, 854850475, 1368212536, 1674904018, 790529591, 1333706334, 622283367, 299405668, 283132166, 1129144348, 564572516, 282286618, 1082060910, 1483182334, 702338592, 529098680, 28931032, 908206935, 406992625, 1097433013, 1489695496, 836627704, 978044778, 855856404, 848871531, 377396401, 1082563423, 1457308021, 872645397, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_248 : List (List Nat × Nat) := entry_248Data.map (unpack 7)
theorem entry_248_ok : walkOKk 7 ((p0_248, 0) :: entry_248) = true := by decide +kernel
theorem entry_248_end : (entry_248.getLastD (p0_248, 0)).1 = z7 := by decide +kernel
theorem p0_248_initial : p0_248 ∈ initialWordsL 7 [2, 4, 8] :=
  mem_initialWordsL_of_full 7 [2, 4, 8] tail_248 (by decide) (by decide)
theorem no_certificate_248 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([2, 4, 8], bound) = false :=
  entryOK_false_of_none [2, 4, 8] bound p0_248_initial
    (R_none_of_entry7 rows entry_248 p0_248 0 entry_248_ok entry_248_end)

/-- Prefix 275: initial word `[2, 7, 5, 0, 0, 0, 0]`; 1 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_275 : List Nat := [0, 0, 0, 0]
def p0_275 : List Nat := [2, 7, 5] ++ tail_275
def entry_275Data : List Nat := [893873661, 893871475, 1474881858, 1772093556, 886177080, 445558140, 918378478, 880317779, 848630432, 897126662, 270676236, 135338460, 902867152, 924368484, 272038652, 136026184, 959532537, 479889730, 193028945, 992897346, 1077721172, 634909204, 317461442, 111815161, 947303221, 429143199, 920033144, 982215050, 543086004, 273895278, 1075395676, 1429217283, 1655395940, 882549793, 1384935098, 1767596560, 1777663161, 888831598, 864186581, 1374176940, 868488843, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_275 : List (List Nat × Nat) := entry_275Data.map (unpack 7)
theorem entry_275_ok : walkOKk 7 ((p0_275, 0) :: entry_275) = true := by decide +kernel
theorem entry_275_end : (entry_275.getLastD (p0_275, 0)).1 = z7 := by decide +kernel
theorem p0_275_initial : p0_275 ∈ initialWordsL 7 [2, 7, 5] :=
  mem_initialWordsL_of_full 7 [2, 7, 5] tail_275 (by decide) (by decide)
theorem no_certificate_275 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([2, 7, 5], bound) = false :=
  entryOK_false_of_none [2, 7, 5] bound p0_275_initial
    (R_none_of_entry7 rows entry_275 p0_275 0 entry_275_ok entry_275_end)

/-- Prefix 398: initial word `[3, 9, 8, 9, 7, 0, 0]`; 282 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_398 : List Nat := [9, 7, 0, 0]
def p0_398 : List Nat := [3, 9, 8] ++ tail_398
def entry_398Data : List Nat := [915840, 893917189, 312864240, 907039213, 926324194, 884229419, 1697867690, 804240601, 40218546, 958674274, 1478115824, 690845983, 928530643, 417158241, 163817629, 973434415, 718951738, 1300386648, 652662582, 1264779652, 602037782, 923973629, 1353382473, 676821196, 340886678, 913144580, 892235839, 893926780, 893971260, 423534366, 1176136066, 517570871, 1458418436, 698637998, 933501728, 887694193, 864907407, 1373247842, 642047281, 32102382, 1735440, 893952013, 893839857, 1389003596, 1631777270, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_398 : List (List Nat × Nat) := entry_398Data.map (unpack 7)
theorem entry_398_ok : walkOKk 7 ((p0_398, 0) :: entry_398) = true := by decide +kernel
theorem entry_398_end : (entry_398.getLastD (p0_398, 0)).1 = z7 := by decide +kernel
theorem p0_398_initial : p0_398 ∈ initialWordsL 7 [3, 9, 8] :=
  mem_initialWordsL_of_full 7 [3, 9, 8] tail_398 (by decide) (by decide)
theorem no_certificate_398 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([3, 9, 8], bound) = false :=
  entryOK_false_of_none [3, 9, 8] bound p0_398_initial
    (R_none_of_entry7 rows entry_398 p0_398 0 entry_398_ok entry_398_end)

/-- Prefix 626: initial word `[6, 2, 6, 9, 1, 0, 0]`; 655 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_626 : List Nat := [9, 1, 0, 0]
def p0_626 : List Nat := [6, 2, 6] ++ tail_626
def entry_626Data : List Nat := [894059143, 895327312, 536272702, 270673820, 90575437, 939152599, 893535897, 867704779, 1374770008, 1625836614, 707248990, 331469564, 1057136939, 481522931, 1317837892, 423688200, 23660166, 950395408, 1368939141, 868350415, 387129687, 334557046, 120233003, 97744962, 989790082, 851615261, 898619076, 849428550, 898815574, 923509068, 1403838184, 702049052, 571425514, 1458766058, 1768948828, 884604716, 863246047, 1372410322, 686396852, 1464514282, 873006053, 627012728, 313512862, 109717067, 7936457, 897709647, 313047022, 909524091, 539451456, 272194968, 136097502, 958278343, 1374176941, 868488843, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_626 : List (List Nat × Nat) := entry_626Data.map (unpack 7)
theorem entry_626_ok : walkOKk 7 ((p0_626, 0) :: entry_626) = true := by decide +kernel
theorem entry_626_end : (entry_626.getLastD (p0_626, 0)).1 = z7 := by decide +kernel
theorem p0_626_initial : p0_626 ∈ initialWordsL 7 [6, 2, 6] :=
  mem_initialWordsL_of_full 7 [6, 2, 6] tail_626 (by decide) (by decide)
theorem no_certificate_626 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([6, 2, 6], bound) = false :=
  entryOK_false_of_none [6, 2, 6] bound p0_626_initial
    (R_none_of_entry7 rows entry_626 p0_626 0 entry_626_ok entry_626_end)

/-- Prefix 710: initial word `[7, 1, 0, 1, 9, 3, 0]`; 441 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_710 : List Nat := [1, 9, 3, 0]
def p0_710 : List Nat := [7, 1, 0] ++ tail_710
def entry_710Data : List Nat := [7442040, 502080, 257880, 894000661, 893864541, 893878580, 893803141, 423454068, 1150178644, 236530564, 49057973, 918270423, 1400052812, 653371222, 282109313, 141054674, 986553989, 319965302, 909870005, 1071224026, 488696093, 246824144, 123542374, 1002558486, 320758704, 999296848, 409989636, 204994818, 1040873968, 522978044, 1202468012, 643491982, 32174960, 4078348, 2045672, 1029352, 894379899, 1363216259, 872645396, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_710 : List (List Nat × Nat) := entry_710Data.map (unpack 7)
theorem entry_710_ok : walkOKk 7 ((p0_710, 0) :: entry_710) = true := by decide +kernel
theorem entry_710_end : (entry_710.getLastD (p0_710, 0)).1 = z7 := by decide +kernel
theorem p0_710_initial : p0_710 ∈ initialWordsL 7 [7, 1, 0] :=
  mem_initialWordsL_of_full 7 [7, 1, 0] tail_710 (by decide) (by decide)
theorem no_certificate_710 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([7, 1, 0], bound) = false :=
  entryOK_false_of_none [7, 1, 0] bound p0_710_initial
    (R_none_of_entry7 rows entry_710 p0_710 0 entry_710_ok entry_710_end)

/-- Prefix 716: initial word `[7, 1, 6, 0, 0, 0, 0]`; 1778 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_716 : List Nat := [0, 0, 0, 0]
def p0_716 : List Nat := [7, 1, 6] ++ tail_716
def entry_716Data : List Nat := [893873931, 491636082, 1186729144, 1487112831, 696640855, 660549118, 1271185320, 1526998579, 1657374259, 887477100, 446084328, 1116907063, 1499371132, 1505039534, 1693430870, 799669573, 1362907318, 1677114478, 1690479076, 889021550, 864281215, 385225047, 148042723, 26975481, 895213673, 1385568292, 608077556, 304038778, 104908547, 993436854, 1390651537, 831675506, 220358484, 192261872, 96137434, 1029353, 894379899, 1363216259, 872645396, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_716 : List (List Nat × Nat) := entry_716Data.map (unpack 7)
theorem entry_716_ok : walkOKk 7 ((p0_716, 0) :: entry_716) = true := by decide +kernel
theorem entry_716_end : (entry_716.getLastD (p0_716, 0)).1 = z7 := by decide +kernel
theorem p0_716_initial : p0_716 ∈ initialWordsL 7 [7, 1, 6] :=
  mem_initialWordsL_of_full 7 [7, 1, 6] tail_716 (by decide) (by decide)
theorem no_certificate_716 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([7, 1, 6], bound) = false :=
  entryOK_false_of_none [7, 1, 6] bound p0_716_initial
    (R_none_of_entry7 rows entry_716 p0_716 0 entry_716_ok entry_716_end)

/-- Prefix 790: initial word `[7, 9, 0, 9, 9, 8, 0]`; 580 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_790 : List Nat := [9, 9, 8, 0]
def p0_790 : List Nat := [7, 9, 0] ++ tail_790
def entry_790Data : List Nat := [958251022, 1417505832, 518058428, 296540542, 908686095, 874113487, 388845003, 155991926, 968225573, 1431690158, 1656755858, 1778841820, 889551212, 917580536, 879857401, 1697772534, 848893296, 897251596, 921430386, 1250458762, 862433237, 852153467, 1366864032, 1577303737, 796431836, 712577690, 527141052, 1154966167, 577603314, 1182676627, 591348402, 965903932, 1478489654, 746680580, 375816370, 1128825804, 1455938503, 680923371, 1374853434, 1451891934, 745344196, 1264074237, 634389412, 1211059929, 605529964, 209050864, 993711456, 1658648204, 831793342, 1354338210, 676003056, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_790 : List (List Nat × Nat) := entry_790Data.map (unpack 7)
theorem entry_790_ok : walkOKk 7 ((p0_790, 0) :: entry_790) = true := by decide +kernel
theorem entry_790_end : (entry_790.getLastD (p0_790, 0)).1 = z7 := by decide +kernel
theorem p0_790_initial : p0_790 ∈ initialWordsL 7 [7, 9, 0] :=
  mem_initialWordsL_of_full 7 [7, 9, 0] tail_790 (by decide) (by decide)
theorem no_certificate_790 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([7, 9, 0], bound) = false :=
  entryOK_false_of_none [7, 9, 0] bound p0_790_initial
    (R_none_of_entry7 rows entry_790 p0_790 0 entry_790_ok entry_790_end)

/-- Prefix 911: initial word `[9, 1, 1, 9, 7, 1, 0]`; 62 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_911 : List Nat := [9, 7, 1, 0]
def p0_911 : List Nat := [9, 1, 1] ++ tail_911
def entry_911Data : List Nat := [897192245, 1117375396, 561039992, 1172045939, 1756958600, 878479300, 895571718, 893359875, 762241158, 336543939, 121226089, 1002697036, 722760630, 1302297934, 1584690354, 1730786698, 864159260, 1323414071, 423966666, 202448780, 908686094, 874113487, 388845003, 155991926, 968225573, 1431690158, 1656755858, 1778841820, 889551212, 917580536, 879857401, 1697772534, 848893296, 897251596, 921430386, 1250458762, 862433237, 852153467, 1366864032, 1577303737, 796431836, 712577690, 527141052, 1154966167, 577603314, 1182676627, 591348402, 965903932, 1478489654, 746680580, 375816370, 1128825804, 1455938503, 680923371, 1374853434, 1451891934, 745344196, 1264074237, 634389412, 1211059929, 605529964, 209050864, 993711456, 1658648204, 831793342, 1354338210, 676003056, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_911 : List (List Nat × Nat) := entry_911Data.map (unpack 7)
theorem entry_911_ok : walkOKk 7 ((p0_911, 0) :: entry_911) = true := by decide +kernel
theorem entry_911_end : (entry_911.getLastD (p0_911, 0)).1 = z7 := by decide +kernel
theorem p0_911_initial : p0_911 ∈ initialWordsL 7 [9, 1, 1] :=
  mem_initialWordsL_of_full 7 [9, 1, 1] tail_911 (by decide) (by decide)
theorem no_certificate_911 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([9, 1, 1], bound) = false :=
  entryOK_false_of_none [9, 1, 1] bound p0_911_initial
    (R_none_of_entry7 rows entry_911 p0_911 0 entry_911_ok entry_911_end)

/-- Prefix 936: initial word `[9, 3, 6, 9, 9, 1, 0]`; 496 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_936 : List Nat := [9, 9, 1, 0]
def p0_936 : List Nat := [9, 3, 6] ++ tail_936
def entry_936Data : List Nat := [2546920, 893998743, 424844800, 21242258, 10559758, 896758536, 869446401, 850302664, 1366062624, 613824345, 1269990860, 863409841, 1372499248, 1579997901, 790122412, 622874702, 31144096, 909436947, 407672593, 1097708017, 817021832, 490256562, 160932886, 33550865, 910646829, 1346842859, 628851287, 1146429962, 857108335, 1562430874, 1719663456, 859955208, 902789032, 924322566, 314377668, 284010726, 1176227298, 1552482190, 1671278883, 1725869033, 819530765, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_936 : List (List Nat × Nat) := entry_936Data.map (unpack 7)
theorem entry_936_ok : walkOKk 7 ((p0_936, 0) :: entry_936) = true := by decide +kernel
theorem entry_936_end : (entry_936.getLastD (p0_936, 0)).1 = z7 := by decide +kernel
theorem p0_936_initial : p0_936 ∈ initialWordsL 7 [9, 3, 6] :=
  mem_initialWordsL_of_full 7 [9, 3, 6] tail_936 (by decide) (by decide)
theorem no_certificate_936 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([9, 3, 6], bound) = false :=
  entryOK_false_of_none [9, 3, 6] bound p0_936_initial
    (R_none_of_entry7 rows entry_936 p0_936 0 entry_936_ok entry_936_end)

/-- Prefix 952: initial word `[9, 5, 2, 2, 0, 2, 0]`; 441 of the 10000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_952 : List Nat := [2, 0, 2, 0]
def p0_952 : List Nat := [9, 5, 2] ++ tail_952
def entry_952Data : List Nat := [898838481, 91857844, 939800661, 890960623, 866547633, 1384128474, 608005566, 1192427040, 596213520, 298045560, 14909136, 7578048, 897537283, 181186456, 981995367, 361961392, 1072506315, 771068520, 1323985870, 423865296, 1105674085, 278628194, 1077885938, 1707673978, 809137247, 1202359820, 601186768, 434653914, 1155768838, 819931696, 1348404138, 1763430732, 881722224, 443337192, 221798556, 110899278, 903990988, 1207232810, 551997612, 278351424, 139182570, 985617595, 493000488, 1276070116, 689514084, 260289434, 85451113, 936473491, 1409147848, 704573924, 214003062, 904571893, 628591020, 1208160391, 1542521734, 770094818, 1280085179, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_952 : List (List Nat × Nat) := entry_952Data.map (unpack 7)
theorem entry_952_ok : walkOKk 7 ((p0_952, 0) :: entry_952) = true := by decide +kernel
theorem entry_952_end : (entry_952.getLastD (p0_952, 0)).1 = z7 := by decide +kernel
theorem p0_952_initial : p0_952 ∈ initialWordsL 7 [9, 5, 2] :=
  mem_initialWordsL_of_full 7 [9, 5, 2] tail_952 (by decide) (by decide)
theorem no_certificate_952 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([9, 5, 2], bound) = false :=
  entryOK_false_of_none [9, 5, 2] bound p0_952_initial
    (R_none_of_entry7 rows entry_952 p0_952 0 entry_952_ok entry_952_end)

/-- Prefix 1337: initial word `[1, 3, 3, 7, 9, 3, 0]`; 241 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1337 : List Nat := [9, 3, 0]
def p0_1337 : List Nat := [1, 3, 3, 7] ++ tail_1337
def entry_1337Data : List Nat := [894613311, 400384579, 1138757632, 1463126733, 1503227314, 611484770, 522080250, 213994587, 62427511, 31152366, 909509293, 628837548, 1193475138, 866634420, 854254041, 378843289, 146089713, 1014023846, 1212734110, 418185762, 1004161702, 457387247, 184000037, 983519463, 447059629, 1362912998, 1677114780, 886105317, 915980708, 878927203, 1329693193, 621442845, 1056672366, 142468402, 945806052, 472903026, 240093660, 1057322302, 532303280, 26615182]
def entry_1337 : List (List Nat × Nat) := entry_1337Data.map (unpack 7)
theorem entry_1337_ok : walkOKk 7 ((p0_1337, 0) :: entry_1337) = true := by decide +kernel
theorem entry_1337_end : (entry_1337.getLastD (p0_1337, 0)).1 = z7 := by decide +kernel
theorem p0_1337_initial : p0_1337 ∈ initialWordsL 7 [1, 3, 3, 7] :=
  mem_initialWordsL_of_full 7 [1, 3, 3, 7] tail_1337 (by decide) (by decide)
theorem no_certificate_1337 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 3, 3, 7], bound) = false :=
  entryOK_false_of_none [1, 3, 3, 7] bound p0_1337_initial
    (R_none_of_entry7 rows entry_1337 p0_1337 0 entry_1337_ok entry_1337_end)

/-- Prefix 1475: initial word `[1, 4, 7, 5, 4, 4, 0]`; 429 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1475 : List Nat := [4, 4, 0]
def p0_1475 : List Nat := [1, 4, 7, 5] ++ tail_1475
def entry_1475Data : List Nat := [897146504, 983546456, 766744314, 1321943980, 660978506, 1271406854, 1551729737, 795029674, 623120408, 391180472, 195590578, 96629258, 989225390, 1457694974, 701064224, 973612382, 48928228, 918212373, 880173337, 861153459, 383530849, 1270596634, 1493594654, 700513772, 352609162, 129265217, 67102190, 971992616, 808266822, 42889440, 896009713, 450474096, 225237066, 111452484, 997809892, 1433039414, 518835450, 1322173100, 661086550, 334185422, 1057322303, 532303280, 26615182]
def entry_1475 : List (List Nat × Nat) := entry_1475Data.map (unpack 7)
theorem entry_1475_ok : walkOKk 7 ((p0_1475, 0) :: entry_1475) = true := by decide +kernel
theorem entry_1475_end : (entry_1475.getLastD (p0_1475, 0)).1 = z7 := by decide +kernel
theorem p0_1475_initial : p0_1475 ∈ initialWordsL 7 [1, 4, 7, 5] :=
  mem_initialWordsL_of_full 7 [1, 4, 7, 5] tail_1475 (by decide) (by decide)
theorem no_certificate_1475 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 4, 7, 5], bound) = false :=
  entryOK_false_of_none [1, 4, 7, 5] bound p0_1475_initial
    (R_none_of_entry7 rows entry_1475 p0_1475 0 entry_1475_ok entry_1475_end)

/-- Prefix 2288: initial word `[2, 2, 8, 8, 0, 0, 0]`; 413 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_2288 : List Nat := [0, 0, 0]
def p0_2288 : List Nat := [2, 2, 8, 8] ++ tail_2288
def entry_2288Data : List Nat := [893877519, 893946818, 424818838, 1150850940, 857329041, 849697156, 897653184, 921631180, 933750480, 940429303, 423175269, 142380343, 987223321, 47145366, 987941566, 1458339342, 1645196323, 884515875, 1474420576, 1635774598, 770971379, 340915907, 123542375, 1002558486, 320758704, 999296848, 409989636, 204994818, 1040873968, 522978044, 1202468012, 643491982, 32174960, 4078348, 2045672, 1029352, 894379899, 1363216259, 872645396, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_2288 : List (List Nat × Nat) := entry_2288Data.map (unpack 7)
theorem entry_2288_ok : walkOKk 7 ((p0_2288, 0) :: entry_2288) = true := by decide +kernel
theorem entry_2288_end : (entry_2288.getLastD (p0_2288, 0)).1 = z7 := by decide +kernel
theorem p0_2288_initial : p0_2288 ∈ initialWordsL 7 [2, 2, 8, 8] :=
  mem_initialWordsL_of_full 7 [2, 2, 8, 8] tail_2288 (by decide) (by decide)
theorem no_certificate_2288 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([2, 2, 8, 8], bound) = false :=
  entryOK_false_of_none [2, 2, 8, 8] bound p0_2288_initial
    (R_none_of_entry7 rows entry_2288 p0_2288 0 entry_2288_ok entry_2288_end)

/-- Prefix 6820: initial word `[6, 8, 2, 0, 0, 0, 0]`; 438 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_6820 : List Nat := [0, 0, 0]
def p0_6820 : List Nat := [6, 8, 2, 0] ++ tail_6820
def entry_6820Data : List Nat := [448, 893871963, 180996350, 1031291972, 515645986, 235661564, 1080903314, 590368210, 478930396, 1180253028, 1483998235, 1682916376, 799243228, 310593284, 196780110, 53813757, 920778617, 881456099, 393682169, 1271104200, 868040136, 805538780, 1296640769, 1539846003, 725223241, 1254007261, 862480359, 805267290, 534238616, 1158638411, 1517760744, 1696155844, 804674171, 1378565236, 1588510218, 1777775316, 888887658, 918544786, 879043175, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_6820 : List (List Nat × Nat) := entry_6820Data.map (unpack 7)
theorem entry_6820_ok : walkOKk 7 ((p0_6820, 0) :: entry_6820) = true := by decide +kernel
theorem entry_6820_end : (entry_6820.getLastD (p0_6820, 0)).1 = z7 := by decide +kernel
theorem p0_6820_initial : p0_6820 ∈ initialWordsL 7 [6, 8, 2, 0] :=
  mem_initialWordsL_of_full 7 [6, 8, 2, 0] tail_6820 (by decide) (by decide)
theorem no_certificate_6820 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([6, 8, 2, 0], bound) = false :=
  entryOK_false_of_none [6, 8, 2, 0] bound p0_6820_initial
    (R_none_of_entry7 rows entry_6820 p0_6820 0 entry_6820_ok entry_6820_end)

/-- Prefix 8834: initial word `[8, 8, 3, 4, 7, 7, 3]`; 428 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_8834 : List Nat := [7, 7, 3]
def p0_8834 : List Nat := [8, 8, 3, 4] ++ tail_8834
def entry_8834Data : List Nat := [1086117630, 1483976092, 1502041310, 1691931776, 1693558878, 1787697058, 893869778, 893866987, 893873134, 893868647, 919930602, 984685318, 808901800, 42921188, 915332315, 1398453816, 1593091789, 796675854, 712583050, 527134840, 73396124, 930562943, 1406192250, 658526325, 329263162, 997245990, 1301282734, 1584639594, 1730761318, 1760418447, 879043174, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_8834 : List (List Nat × Nat) := entry_8834Data.map (unpack 7)
theorem entry_8834_ok : walkOKk 7 ((p0_8834, 0) :: entry_8834) = true := by decide +kernel
theorem entry_8834_end : (entry_8834.getLastD (p0_8834, 0)).1 = z7 := by decide +kernel
theorem p0_8834_initial : p0_8834 ∈ initialWordsL 7 [8, 8, 3, 4] :=
  mem_initialWordsL_of_full 7 [8, 8, 3, 4] tail_8834 (by decide) (by decide)
theorem no_certificate_8834 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([8, 8, 3, 4], bound) = false :=
  entryOK_false_of_none [8, 8, 3, 4] bound p0_8834_initial
    (R_none_of_entry7 rows entry_8834 p0_8834 0 entry_8834_ok entry_8834_end)

/-- Prefix 8935: initial word `[8, 9, 3, 5, 3, 0, 0]`; 371 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_8935 : List Nat := [3, 0, 0]
def p0_8935 : List Nat := [8, 9, 3, 5] ++ tail_8935
def entry_8935Data : List Nat := [166132, 893954805, 893841253, 1474756542, 690339249, 439105040, 219552880, 11107964, 899425361, 452058800, 226159360, 13784066, 900763943, 403336451, 1140109746, 236027102, 903203855, 404686025, 1096084431, 1488959816, 1680941040, 1779927618, 1787352684, 893683182, 892415607, 891775645, 866831151, 582140032, 1367568832, 1587960072, 1687851415, 1784713024, 892363352, 919109726, 358686808, 1269237486, 329401440, 1082023381, 1483095358, 1631777271, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_8935 : List (List Nat × Nat) := entry_8935Data.map (unpack 7)
theorem entry_8935_ok : walkOKk 7 ((p0_8935, 0) :: entry_8935) = true := by decide +kernel
theorem entry_8935_end : (entry_8935.getLastD (p0_8935, 0)).1 = z7 := by decide +kernel
theorem p0_8935_initial : p0_8935 ∈ initialWordsL 7 [8, 9, 3, 5] :=
  mem_initialWordsL_of_full 7 [8, 9, 3, 5] tail_8935 (by decide) (by decide)
theorem no_certificate_8935 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([8, 9, 3, 5], bound) = false :=
  entryOK_false_of_none [8, 9, 3, 5] bound p0_8935_initial
    (R_none_of_entry7 rows entry_8935 p0_8935 0 entry_8935_ok entry_8935_end)

/-- Prefix 8846: initial word `[8, 8, 4, 6, 4, 2, 0]`; 636 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_8846 : List Nat := [4, 2, 0]
def p0_8846 : List Nat := [8, 8, 4, 6] ++ tail_8846
def entry_8846Data : List Nat := [894416523, 895512158, 896059958, 893597821, 893994862, 893858051, 449395034, 1118572487, 1170922520, 1712209186, 811534469, 405890696, 1096693607, 322996220, 912250400, 92658400, 46336040, 916915955, 411412439, 1144154238, 859463121, 847464580, 894144786, 892646391, 399400795, 155007135, 1018414328, 408469430, 378102488, 1270319060, 1552482191, 1671278883, 1725869033, 819530765, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_8846 : List (List Nat × Nat) := entry_8846Data.map (unpack 7)
theorem entry_8846_ok : walkOKk 7 ((p0_8846, 0) :: entry_8846) = true := by decide +kernel
theorem entry_8846_end : (entry_8846.getLastD (p0_8846, 0)).1 = z7 := by decide +kernel
theorem p0_8846_initial : p0_8846 ∈ initialWordsL 7 [8, 8, 4, 6] :=
  mem_initialWordsL_of_full 7 [8, 8, 4, 6] tail_8846 (by decide) (by decide)
theorem no_certificate_8846 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([8, 8, 4, 6], bound) = false :=
  entryOK_false_of_none [8, 8, 4, 6] bound p0_8846_initial
    (R_none_of_entry7 rows entry_8846 p0_8846 0 entry_8846_ok entry_8846_end)

/-- Prefix 4668: initial word `[4, 6, 6, 8, 4, 1, 0]`; 469 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_4668 : List Nat := [4, 1, 0]
def p0_4668 : List Nat := [4, 6, 6, 8] ++ tail_4668
def entry_4668Data : List Nat := [896535660, 869328141, 895120658, 893134687, 357518358, 1119546478, 1451178969, 1666510334, 785046487, 309759300, 914064634, 929967396, 886044333, 863965495, 715824070, 393463722, 153760462, 29834693, 908789085, 875461333, 858667497, 1651902162, 882375447, 359319676, 182135576, 93543544, 46772114, 961827578, 852575962, 894406854, 1564295800, 782271362, 1329577220, 1602064082, 804674170, 1378565236, 1588510218, 1777775316, 888887658, 918544786, 879043175, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_4668 : List (List Nat × Nat) := entry_4668Data.map (unpack 7)
theorem entry_4668_ok : walkOKk 7 ((p0_4668, 0) :: entry_4668) = true := by decide +kernel
theorem entry_4668_end : (entry_4668.getLastD (p0_4668, 0)).1 = z7 := by decide +kernel
theorem p0_4668_initial : p0_4668 ∈ initialWordsL 7 [4, 6, 6, 8] :=
  mem_initialWordsL_of_full 7 [4, 6, 6, 8] tail_4668 (by decide) (by decide)
theorem no_certificate_4668 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([4, 6, 6, 8], bound) = false :=
  entryOK_false_of_none [4, 6, 6, 8] bound p0_4668_initial
    (R_none_of_entry7 rows entry_4668 p0_4668 0 entry_4668_ok entry_4668_end)

/-- Prefix 1386: initial word `[1, 3, 8, 6, 0, 0, 0]`; 429 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1386 : List Nat := [0, 0, 0]
def p0_1386 : List Nat := [1, 3, 8, 6] ++ tail_1386
def entry_1386Data : List Nat := [893875807, 893869983, 893874650, 893869405, 1070300192, 1349746338, 1718927718, 814887561, 407443798, 916472436, 879303369, 1292909522, 599415739, 923842201, 882858273, 535648566, 220908723, 949611104, 474929374, 1178375790, 1527629416, 1701089838, 800269190, 1291433894, 1537238090, 1707190868, 853602292, 847737977, 1364847978, 1766598360, 892814844, 270454472, 135233734, 20577503, 948854076, 1368168457, 783505832, 533157042, 163084408, 84011444, 42005740, 958278342, 1374176941, 868488843, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_1386 : List (List Nat × Nat) := entry_1386Data.map (unpack 7)
theorem entry_1386_ok : walkOKk 7 ((p0_1386, 0) :: entry_1386) = true := by decide +kernel
theorem entry_1386_end : (entry_1386.getLastD (p0_1386, 0)).1 = z7 := by decide +kernel
theorem p0_1386_initial : p0_1386 ∈ initialWordsL 7 [1, 3, 8, 6] :=
  mem_initialWordsL_of_full 7 [1, 3, 8, 6] tail_1386 (by decide) (by decide)
theorem no_certificate_1386 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 3, 8, 6], bound) = false :=
  entryOK_false_of_none [1, 3, 8, 6] bound p0_1386_initial
    (R_none_of_entry7 rows entry_1386 p0_1386 0 entry_1386_ok entry_1386_end)

/-- Prefix 3657: initial word `[3, 6, 5, 7, 6, 1, 0]`; 242 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_3657 : List Nat := [6, 1, 0]
def p0_3657 : List Nat := [3, 6, 5, 7] ++ tail_3657
def entry_3657Data : List Nat := [331156, 894030459, 1742934364, 1765215459, 892745698, 399456929, 1271262978, 1551657817, 1738907596, 869577602, 895256918, 868562059, 907082386, 874611575, 669447312, 480415094, 1181124824, 547158661, 225367401, 902664029, 313295084, 1088310840, 546508038, 1214047834, 1545465780, 772739388, 488048270, 1273477070, 1493868310, 1687851414, 1784713024, 892363352, 919109726, 358686808, 1269237486, 329401440, 1082023381, 1483095358, 1631777271, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_3657 : List (List Nat × Nat) := entry_3657Data.map (unpack 7)
theorem entry_3657_ok : walkOKk 7 ((p0_3657, 0) :: entry_3657) = true := by decide +kernel
theorem entry_3657_end : (entry_3657.getLastD (p0_3657, 0)).1 = z7 := by decide +kernel
theorem p0_3657_initial : p0_3657 ∈ initialWordsL 7 [3, 6, 5, 7] :=
  mem_initialWordsL_of_full 7 [3, 6, 5, 7] tail_3657 (by decide) (by decide)
theorem no_certificate_3657 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([3, 6, 5, 7], bound) = false :=
  entryOK_false_of_none [3, 6, 5, 7] bound p0_3657_initial
    (R_none_of_entry7 rows entry_3657 p0_3657 0 entry_3657_ok entry_3657_end)

/-- Prefix 4965: initial word `[4, 9, 6, 5, 4, 0, 0]`; 330 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_4965 : List Nat := [4, 0, 0]
def p0_4965 : List Nat := [4, 9, 6, 5] ++ tail_4965
def entry_4965Data : List Nat := [62308, 893902893, 1430319802, 1655947218, 1781030202, 845945301, 940866734, 423387847, 289461234, 97808559, 989821880, 495034402, 1188434460, 859201719, 1651929216, 797824172, 399042388, 1093392933, 1438092107, 721583522, 1019337746, 1076567454, 682008190, 293964713, 149334650, 27745249, 907614043, 981593752, 543061438, 925722900, 935789500, 888831599, 864186581, 1374176940, 868488843, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_4965 : List (List Nat × Nat) := entry_4965Data.map (unpack 7)
theorem entry_4965_ok : walkOKk 7 ((p0_4965, 0) :: entry_4965) = true := by decide +kernel
theorem entry_4965_end : (entry_4965.getLastD (p0_4965, 0)).1 = z7 := by decide +kernel
theorem p0_4965_initial : p0_4965 ∈ initialWordsL 7 [4, 9, 6, 5] :=
  mem_initialWordsL_of_full 7 [4, 9, 6, 5] tail_4965 (by decide) (by decide)
theorem no_certificate_4965 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([4, 9, 6, 5], bound) = false :=
  entryOK_false_of_none [4, 9, 6, 5] bound p0_4965_initial
    (R_none_of_entry7 rows entry_4965 p0_4965 0 entry_4965_ok entry_4965_end)

/-- Prefix 8835: initial word `[8, 8, 3, 5, 9, 7, 0]`; 398 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_8835 : List Nat := [9, 7, 0]
def p0_8835 : List Nat := [8, 8, 3, 5] ++ tail_8835
def entry_8835Data : List Nat := [895602047, 1363833849, 423524930, 1150210844, 236531832, 1081344964, 279887476, 1033808637, 516904660, 924421542, 883144371, 1382495244, 691377600, 928427623, 883984593, 535704882, 220936881, 904795121, 873341249, 857607797, 431149676, 215704798, 909231264, 984150694, 719617854, 312769887, 1097302562, 501605401, 1191781690, 509000710, 1274394732, 647082162, 278847477, 139430254, 47554040, 986849210, 496278348, 340021320, 64040448, 925885105, 1354338211, 676003056, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_8835 : List (List Nat × Nat) := entry_8835Data.map (unpack 7)
theorem entry_8835_ok : walkOKk 7 ((p0_8835, 0) :: entry_8835) = true := by decide +kernel
theorem entry_8835_end : (entry_8835.getLastD (p0_8835, 0)).1 = z7 := by decide +kernel
theorem p0_8835_initial : p0_8835 ∈ initialWordsL 7 [8, 8, 3, 5] :=
  mem_initialWordsL_of_full 7 [8, 8, 3, 5] tail_8835 (by decide) (by decide)
theorem no_certificate_8835 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([8, 8, 3, 5], bound) = false :=
  entryOK_false_of_none [8, 8, 3, 5] bound p0_8835_initial
    (R_none_of_entry7 rows entry_8835 p0_8835 0 entry_8835_ok entry_8835_end)

/-- Prefix 1114: initial word `[1, 1, 1, 4, 4, 4, 2]`; 237 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1114 : List Nat := [4, 4, 2]
def p0_1114 : List Nat := [1, 1, 1, 4] ++ tail_1114
def entry_1114Data : List Nat := [908900550, 403124044, 198937408, 99475202, 2822041, 895282399, 895938580, 893845103, 1387710192, 693855456, 349403466, 1268649514, 1446581738, 876814012, 911211936, 928540876, 1354431801, 1572321899, 885569918, 806421768, 1247171740, 625931648, 312900862, 1097433012, 1489695496, 836627704, 978044778, 855856404, 848871531, 377396401, 1082563423, 1457308021, 872645397, 716388368, 440407496, 1114068629, 1448429973, 676003057, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_1114 : List (List Nat × Nat) := entry_1114Data.map (unpack 7)
theorem entry_1114_ok : walkOKk 7 ((p0_1114, 0) :: entry_1114) = true := by decide +kernel
theorem entry_1114_end : (entry_1114.getLastD (p0_1114, 0)).1 = z7 := by decide +kernel
theorem p0_1114_initial : p0_1114 ∈ initialWordsL 7 [1, 1, 1, 4] :=
  mem_initialWordsL_of_full 7 [1, 1, 1, 4] tail_1114 (by decide) (by decide)
theorem no_certificate_1114 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 1, 1, 4], bound) = false :=
  entryOK_false_of_none [1, 1, 1, 4] bound p0_1114_initial
    (R_none_of_entry7 rows entry_1114 p0_1114 0 entry_1114_ok entry_1114_end)

/-- Prefix 4345: initial word `[4, 3, 4, 5, 0, 0, 0]`; 424 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_4345 : List Nat := [0, 0, 0]
def p0_4345 : List Nat := [4, 3, 4, 5] ++ tail_4345
def entry_4345Data : List Nat := [36142, 1808, 893872643, 134211126, 1008016324, 229182022, 69891251, 973510950, 442055373, 1159479296, 773071032, 532635644, 268673878, 89643677, 938686719, 893636065, 983240974, 1566274764, 783144222, 1330137454, 1603640208, 804165882, 1023466864, 140560878, 905604028, 1393527924, 1635144112, 820041296, 1348472258, 874377436, 716345010, 485229218, 1183532210, 547072861, 276012168, 1031747503, 1077200270, 1305150488, 422930042, 1149913040, 574963036, 1181346741, 590673370, 1367865196, 1587975216, 796965752, 1292347757, 1537569537, 1706060240, 809626369, 1244855890, 330651926, 1133989576, 566994788, 240093661, 1057322302, 532303280, 26615182]
def entry_4345 : List (List Nat × Nat) := entry_4345Data.map (unpack 7)
theorem entry_4345_ok : walkOKk 7 ((p0_4345, 0) :: entry_4345) = true := by decide +kernel
theorem entry_4345_end : (entry_4345.getLastD (p0_4345, 0)).1 = z7 := by decide +kernel
theorem p0_4345_initial : p0_4345 ∈ initialWordsL 7 [4, 3, 4, 5] :=
  mem_initialWordsL_of_full 7 [4, 3, 4, 5] tail_4345 (by decide) (by decide)
theorem no_certificate_4345 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([4, 3, 4, 5], bound) = false :=
  entryOK_false_of_none [4, 3, 4, 5] bound p0_4345_initial
    (R_none_of_entry7 rows entry_4345 p0_4345 0 entry_4345_ok entry_4345_end)

/-- Prefix 3654: initial word `[3, 6, 5, 4, 2, 0, 0]`; 395 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_3654 : List Nat := [2, 0, 0]
def p0_3654 : List Nat := [3, 6, 5, 4] ++ tail_3654
def entry_3654Data : List Nat := [29360, 14680, 7592, 893875535, 672750132, 338727342, 195716906, 992896241, 1433723250, 720504096, 1644877028, 800273854, 1363205886, 612405723, 966839834, 587141134, 248876981, 124438490, 1003136846, 1165144240, 1754137778, 1786063192, 1786903317, 893458174, 892296929, 867091793, 1562935878, 793374506, 399693194, 1138418078, 1507650578, 709132027, 1295476774, 735053856, 1645604534, 705768488, 1270206905, 1577187120, 1725869032, 819530765, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_3654 : List (List Nat × Nat) := entry_3654Data.map (unpack 7)
theorem entry_3654_ok : walkOKk 7 ((p0_3654, 0) :: entry_3654) = true := by decide +kernel
theorem entry_3654_end : (entry_3654.getLastD (p0_3654, 0)).1 = z7 := by decide +kernel
theorem p0_3654_initial : p0_3654 ∈ initialWordsL 7 [3, 6, 5, 4] :=
  mem_initialWordsL_of_full 7 [3, 6, 5, 4] tail_3654 (by decide) (by decide)
theorem no_certificate_3654 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([3, 6, 5, 4], bound) = false :=
  entryOK_false_of_none [3, 6, 5, 4] bound p0_3654_initial
    (R_none_of_entry7 rows entry_3654 p0_3654 0 entry_3654_ok entry_3654_end)

/-- Prefix 6787: initial word `[6, 7, 8, 7, 0, 0, 0]`; 415 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_6787 : List Nat := [0, 0, 0]
def p0_6787 : List Nat := [6, 7, 8, 7] ++ tail_6787
def entry_6787Data : List Nat := [893876843, 893870519, 893872056, 867879699, 386893969, 1270764790, 637919882, 121283528, 1002725774, 678322604, 341637040, 173294600, 978042941, 851151383, 1366492968, 614045691, 1245464708, 330682024, 108273912, 945656077, 1366699417, 1646428738, 889151798, 804125124, 219110924, 1003427183, 1440285090, 1660930186, 783425711, 622539542, 31257298, 895434279, 896021018, 893578027, 1362822163, 636834441, 923237381, 892870439, 893952012, 893839857, 1389003596, 1631777270, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_6787 : List (List Nat × Nat) := entry_6787Data.map (unpack 7)
theorem entry_6787_ok : walkOKk 7 ((p0_6787, 0) :: entry_6787) = true := by decide +kernel
theorem entry_6787_end : (entry_6787.getLastD (p0_6787, 0)).1 = z7 := by decide +kernel
theorem p0_6787_initial : p0_6787 ∈ initialWordsL 7 [6, 7, 8, 7] :=
  mem_initialWordsL_of_full 7 [6, 7, 8, 7] tail_6787 (by decide) (by decide)
theorem no_certificate_6787 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([6, 7, 8, 7], bound) = false :=
  entryOK_false_of_none [6, 7, 8, 7] bound p0_6787_initial
    (R_none_of_entry7 rows entry_6787 p0_6787 0 entry_6787_ok entry_6787_end)

/-- Prefix 1299: initial word `[1, 2, 9, 9, 5, 4, 0]`; 420 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1299 : List Nat := [5, 4, 0]
def p0_1299 : List Nat := [1, 2, 9, 9] ++ tail_1299
def entry_1299Data : List Nat := [1185582, 59640, 9840, 893876641, 893946208, 893980632, 893854167, 359899768, 1269168174, 691638226, 1286736372, 1534893805, 1661188663, 783548451, 486113310, 428900242, 157871568, 970454887, 1423668982, 1602064083, 804674170, 1378565236, 1588510218, 1777775316, 888887658, 918544786, 879043175, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_1299 : List (List Nat × Nat) := entry_1299Data.map (unpack 7)
theorem entry_1299_ok : walkOKk 7 ((p0_1299, 0) :: entry_1299) = true := by decide +kernel
theorem entry_1299_end : (entry_1299.getLastD (p0_1299, 0)).1 = z7 := by decide +kernel
theorem p0_1299_initial : p0_1299 ∈ initialWordsL 7 [1, 2, 9, 9] :=
  mem_initialWordsL_of_full 7 [1, 2, 9, 9] tail_1299 (by decide) (by decide)
theorem no_certificate_1299 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 2, 9, 9], bound) = false :=
  entryOK_false_of_none [1, 2, 9, 9] bound p0_1299_initial
    (R_none_of_entry7 rows entry_1299 p0_1299 0 entry_1299_ok entry_1299_end)

/-- Prefix 4439: initial word `[4, 4, 3, 9, 1, 0, 0]`; 496 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_4439 : List Nat := [1, 0, 0]
def p0_4439 : List Nat := [4, 4, 3, 9] ++ tail_4439
def entry_4439Data : List Nat := [894126325, 223487522, 111867754, 996721536, 498490728, 382479748, 1134235190, 522547471, 1151502985, 532348083, 962953916, 1567723154, 1687225002, 1735018231, 867505884, 854820075, 1368197336, 785976516, 712054924, 214507072, 107383838, 994609538, 452604667, 226435884, 1083961040, 858682978, 1741290452, 801444757, 331521927, 143606032, 963198657, 1657128720, 887341362, 1027619482, 1452257760, 728481174, 1305151690, 605529965, 209050864, 993711456, 1658648204, 831793342, 1354338210, 676003056, 1280085178, 868488842, 895202498, 1698540148, 849270074, 428277184, 1151414064, 532303281, 26615182]
def entry_4439 : List (List Nat × Nat) := entry_4439Data.map (unpack 7)
theorem entry_4439_ok : walkOKk 7 ((p0_4439, 0) :: entry_4439) = true := by decide +kernel
theorem entry_4439_end : (entry_4439.getLastD (p0_4439, 0)).1 = z7 := by decide +kernel
theorem p0_4439_initial : p0_4439 ∈ initialWordsL 7 [4, 4, 3, 9] :=
  mem_initialWordsL_of_full 7 [4, 4, 3, 9] tail_4439 (by decide) (by decide)
theorem no_certificate_4439 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([4, 4, 3, 9], bound) = false :=
  entryOK_false_of_none [4, 4, 3, 9] bound p0_4439_initial
    (R_none_of_entry7 rows entry_4439 p0_4439 0 entry_4439_ok entry_4439_end)

/-- Prefix 1452: initial word `[1, 4, 5, 2, 2, 2, 0]`; 405 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_1452 : List Nat := [2, 2, 0]
def p0_1452 : List Nat := [1, 4, 5, 2] ++ tail_1452
def entry_1452Data : List Nat := [894394241, 1698506234, 804559873, 1296151315, 1588986418, 883940402, 895968578, 849283354, 898742958, 923472436, 882679889, 862276775, 668824074, 616810128, 432965500, 216606554, 63733495, 970431730, 1378967373, 607740670, 1279331730, 557948336, 281450248, 140731982, 48211060, 917846949, 492840906, 1097158172, 591304774, 1234100406, 570010839, 240429121, 120214560, 897406387, 1117516406, 326506942, 1104164232, 1443477775, 1611968479, 809626368, 1244855890, 330651926, 1133989576, 566994788, 240093661, 1057322302, 532303280, 26615182]
def entry_1452 : List (List Nat × Nat) := entry_1452Data.map (unpack 7)
theorem entry_1452_ok : walkOKk 7 ((p0_1452, 0) :: entry_1452) = true := by decide +kernel
theorem entry_1452_end : (entry_1452.getLastD (p0_1452, 0)).1 = z7 := by decide +kernel
theorem p0_1452_initial : p0_1452 ∈ initialWordsL 7 [1, 4, 5, 2] :=
  mem_initialWordsL_of_full 7 [1, 4, 5, 2] tail_1452 (by decide) (by decide)
theorem no_certificate_1452 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([1, 4, 5, 2], bound) = false :=
  entryOK_false_of_none [1, 4, 5, 2] bound p0_1452_initial
    (R_none_of_entry7 rows entry_1452 p0_1452 0 entry_1452_ok entry_1452_end)

/-- Prefix 8802: initial word `[8, 8, 0, 2, 2, 0, 0]`; 557 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_8802 : List Nat := [2, 0, 0]
def p0_8802 : List Nat := [8, 8, 0, 2] ++ tail_8802
def entry_8802Data : List Nat := [893899191, 893957654, 892546669, 919207882, 1026743226, 468801489, 234400762, 72630581, 986649348, 317624310, 111889755, 9028957, 4644780, 898795552, 536445790, 1456899782, 681534313, 1232292775, 1556934028, 778473512, 711679106, 1061314482, 142700182, 49195160, 987669788, 1456913924, 730926202, 170503284, 1081053962, 141217916, 987931619, 1389003597, 1631777270, 819530764, 219750904, 994246458, 856666488, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_8802 : List (List Nat × Nat) := entry_8802Data.map (unpack 7)
theorem entry_8802_ok : walkOKk 7 ((p0_8802, 0) :: entry_8802) = true := by decide +kernel
theorem entry_8802_end : (entry_8802.getLastD (p0_8802, 0)).1 = z7 := by decide +kernel
theorem p0_8802_initial : p0_8802 ∈ initialWordsL 7 [8, 8, 0, 2] :=
  mem_initialWordsL_of_full 7 [8, 8, 0, 2] tail_8802 (by decide) (by decide)
theorem no_certificate_8802 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([8, 8, 0, 2], bound) = false :=
  entryOK_false_of_none [8, 8, 0, 2] bound p0_8802_initial
    (R_none_of_entry7 rows entry_8802 p0_8802 0 entry_8802_ok entry_8802_end)

/-- Prefix 4456: initial word `[4, 4, 5, 6, 5, 5, 0]`; 536 of the 1000 long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_4456 : List Nat := [5, 5, 0]
def p0_4456 : List Nat := [4, 4, 5, 6] ++ tail_4456
def entry_4456Data : List Nat := [897538062, 1389686650, 516426718, 1174239687, 327003826, 141340484, 1081935084, 517516278, 921976402, 414072641, 912099291, 409134085, 246146630, 1061521694, 725831840, 1254311579, 869676242, 1375749242, 643297981, 1215390409, 607818666, 253735406, 1174596244, 235288702, 47147531, 987942666, 449394693, 1118568725, 281741824, 1175872778, 1757143444, 1772436603, 841641679, 376251039, 141079639, 903154228, 1207190972, 1490547832, 1636669557, 1760418446, 879043174, 913622526, 313842666, 1088338220, 856666489, 849270075, 428277184, 1151414064, 532303281, 26615182]
def entry_4456 : List (List Nat × Nat) := entry_4456Data.map (unpack 7)
theorem entry_4456_ok : walkOKk 7 ((p0_4456, 0) :: entry_4456) = true := by decide +kernel
theorem entry_4456_end : (entry_4456.getLastD (p0_4456, 0)).1 = z7 := by decide +kernel
theorem p0_4456_initial : p0_4456 ∈ initialWordsL 7 [4, 4, 5, 6] :=
  mem_initialWordsL_of_full 7 [4, 4, 5, 6] tail_4456 (by decide) (by decide)
theorem no_certificate_4456 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ([4, 4, 5, 6], bound) = false :=
  entryOK_false_of_none [4, 4, 5, 6] bound p0_4456_initial
    (R_none_of_entry7 rows entry_4456 p0_4456 0 entry_4456_ok entry_4456_end)

/-- All 34 prefixes at once. -/
def prefixes : List (List Nat) := [[1, 3, 8], [1, 6, 4], [1, 9, 8], [2, 4, 8], [2, 7, 5], [3, 9, 8], [6, 2, 6], [7, 1, 0], [7, 1, 6], [7, 9, 0], [9, 1, 1], [9, 3, 6], [9, 5, 2], [1, 3, 3, 7], [1, 4, 7, 5], [2, 2, 8, 8], [6, 8, 2, 0], [8, 8, 3, 4], [8, 9, 3, 5], [8, 8, 4, 6], [4, 6, 6, 8], [1, 3, 8, 6], [3, 6, 5, 7], [4, 9, 6, 5], [8, 8, 3, 5], [1, 1, 1, 4], [4, 3, 4, 5], [3, 6, 5, 4], [6, 7, 8, 7], [1, 2, 9, 9], [4, 4, 3, 9], [1, 4, 5, 2], [8, 8, 0, 2], [4, 4, 5, 6]]

theorem no_certificate_all {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (bound : Nat) :
    ∀ pre ∈ prefixes, entryOK 7 R (pre, bound) = false := by
  intro pre hpre
  simp only [prefixes, List.mem_cons, List.mem_nil_iff, or_false] at hpre
  rcases hpre with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact no_certificate_138 rows bound
  · exact no_certificate_164 rows bound
  · exact no_certificate_198 rows bound
  · exact no_certificate_248 rows bound
  · exact no_certificate_275 rows bound
  · exact no_certificate_398 rows bound
  · exact no_certificate_626 rows bound
  · exact no_certificate_710 rows bound
  · exact no_certificate_716 rows bound
  · exact no_certificate_790 rows bound
  · exact no_certificate_911 rows bound
  · exact no_certificate_936 rows bound
  · exact no_certificate_952 rows bound
  · exact no_certificate_1337 rows bound
  · exact no_certificate_1475 rows bound
  · exact no_certificate_2288 rows bound
  · exact no_certificate_6820 rows bound
  · exact no_certificate_8834 rows bound
  · exact no_certificate_8935 rows bound
  · exact no_certificate_8846 rows bound
  · exact no_certificate_4668 rows bound
  · exact no_certificate_1386 rows bound
  · exact no_certificate_3657 rows bound
  · exact no_certificate_4965 rows bound
  · exact no_certificate_8835 rows bound
  · exact no_certificate_1114 rows bound
  · exact no_certificate_4345 rows bound
  · exact no_certificate_3654 rows bound
  · exact no_certificate_6787 rows bound
  · exact no_certificate_1299 rows bound
  · exact no_certificate_4439 rows bound
  · exact no_certificate_1452 rows bound
  · exact no_certificate_8802 rows bound
  · exact no_certificate_4456 rows bound

end Sprint04.PrefixesK7

#print axioms Sprint04.PrefixesK7.no_certificate_138
#print axioms Sprint04.PrefixesK7.no_certificate_164
#print axioms Sprint04.PrefixesK7.no_certificate_198
#print axioms Sprint04.PrefixesK7.no_certificate_248
#print axioms Sprint04.PrefixesK7.no_certificate_275
#print axioms Sprint04.PrefixesK7.no_certificate_398
#print axioms Sprint04.PrefixesK7.no_certificate_626
#print axioms Sprint04.PrefixesK7.no_certificate_710
#print axioms Sprint04.PrefixesK7.no_certificate_716
#print axioms Sprint04.PrefixesK7.no_certificate_790
#print axioms Sprint04.PrefixesK7.no_certificate_911
#print axioms Sprint04.PrefixesK7.no_certificate_936
#print axioms Sprint04.PrefixesK7.no_certificate_952
#print axioms Sprint04.PrefixesK7.no_certificate_1337
#print axioms Sprint04.PrefixesK7.no_certificate_1475
#print axioms Sprint04.PrefixesK7.no_certificate_2288
#print axioms Sprint04.PrefixesK7.no_certificate_6820
#print axioms Sprint04.PrefixesK7.no_certificate_8834
#print axioms Sprint04.PrefixesK7.no_certificate_8935
#print axioms Sprint04.PrefixesK7.no_certificate_8846
#print axioms Sprint04.PrefixesK7.no_certificate_4668
#print axioms Sprint04.PrefixesK7.no_certificate_1386
#print axioms Sprint04.PrefixesK7.no_certificate_3657
#print axioms Sprint04.PrefixesK7.no_certificate_4965
#print axioms Sprint04.PrefixesK7.no_certificate_8835
#print axioms Sprint04.PrefixesK7.no_certificate_1114
#print axioms Sprint04.PrefixesK7.no_certificate_4345
#print axioms Sprint04.PrefixesK7.no_certificate_3654
#print axioms Sprint04.PrefixesK7.no_certificate_6787
#print axioms Sprint04.PrefixesK7.no_certificate_1299
#print axioms Sprint04.PrefixesK7.no_certificate_4439
#print axioms Sprint04.PrefixesK7.no_certificate_1452
#print axioms Sprint04.PrefixesK7.no_certificate_8802
#print axioms Sprint04.PrefixesK7.no_certificate_4456
#print axioms Sprint04.PrefixesK7.no_certificate_all

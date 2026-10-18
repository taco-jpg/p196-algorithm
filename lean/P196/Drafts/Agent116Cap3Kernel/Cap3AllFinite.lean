import P196.Drafts.Agent116Integration.Cap3AllBatch000
import P196.Drafts.Agent116Integration.Cap3AllBatch001
import P196.Drafts.Agent116Integration.Cap3AllBatch002
import P196.Drafts.Agent116Integration.Cap3AllBatch003
import P196.Drafts.Agent116Integration.Cap3AllBatch004
import P196.Drafts.Agent116Integration.Cap3AllBatch005
import P196.Drafts.Agent116Integration.Cap3AllBatch006
import P196.Drafts.Agent116Integration.Cap3AllBatch007
import P196.Drafts.Agent116Integration.Cap3AllBatch008
import P196.Drafts.Agent116Integration.Cap3AllBatch009
import P196.Drafts.Agent116Integration.Cap3AllBatch010
import P196.Drafts.Agent116Integration.Cap3AllBatch011
import P196.Drafts.Agent116Integration.Cap3AllBatch012
import P196.Drafts.Agent116Integration.Cap3AllBatch013
import P196.Drafts.Agent116Integration.Cap3AllBatch014
import P196.Drafts.Agent116Integration.Cap3AllBatch015
import P196.Drafts.Agent116Integration.Cap3AllBatch016
import P196.Drafts.Agent116Integration.Cap3AllBatch017
import P196.Drafts.Agent116Integration.Cap3AllBatch018
import P196.Drafts.Agent116Integration.Cap3AllBatch019
import P196.Drafts.Agent116Integration.Cap3AllBatch020
import P196.Drafts.Agent116Integration.Cap3AllBatch021
import P196.Drafts.Agent116Integration.Cap3AllBatch022
import P196.Drafts.Agent116Integration.Cap3AllBatch023
import P196.Drafts.Agent116Integration.Cap3AllBatch024
import P196.Drafts.Agent116Integration.Cap3AllBatch025
import P196.Drafts.Agent116Integration.Cap3AllBatch026
import P196.Drafts.Agent116Integration.Cap3AllBatch027
import P196.Drafts.Agent116Integration.Cap3AllBatch028
import P196.Drafts.Agent116Integration.Cap3AllBatch029
import P196.Drafts.Agent116Integration.Cap3AllBatch030
import P196.Drafts.Agent116Integration.Cap3AllBatch031
import P196.Drafts.Agent116Integration.Cap3AllBatch032
import P196.Drafts.Agent116Integration.Cap3AllBatch033
import P196.Drafts.Agent116Integration.Cap3AllBatch034
import P196.Drafts.Agent116Integration.Cap3AllBatch035
import P196.Drafts.Agent116Integration.Cap3AllBatch036
import P196.Drafts.Agent116Integration.Cap3AllBatch037
import P196.Drafts.Agent116Integration.Cap3AllBatch038
import P196.Drafts.Agent116Integration.Cap3AllBatch039
import P196.Drafts.Agent116Integration.Cap3AllBatch040
import P196.Drafts.Agent116Integration.Cap3AllBatch041
import P196.Drafts.Agent116Integration.Cap3AllBatch042
import P196.Drafts.Agent116Integration.Cap3AllBatch043
import P196.Drafts.Agent116Integration.Cap3AllBatch044
import P196.Drafts.Agent116Integration.Cap3AllBatch045
import P196.Drafts.Agent116Integration.Cap3AllBatch046
import P196.Drafts.Agent116Integration.Cap3AllBatch047
import P196.Drafts.Agent116Integration.Cap3AllBatch048
import P196.Drafts.Agent116Integration.Cap3AllBatch049
import P196.Drafts.Agent116Integration.Cap3AllBatch050
import P196.Drafts.Agent116Integration.Cap3AllBatch051
import P196.Drafts.Agent116Integration.Cap3AllBatch052
import P196.Drafts.Agent116Integration.Cap3AllBatch053
import P196.Drafts.Agent116Integration.Cap3AllBatch054
import P196.Drafts.Agent116Integration.Cap3AllBatch055
import P196.Drafts.Agent116Integration.Cap3AllBatch056

namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxHeartbeats 0

theorem cap3_all_exits_by_ten :
    ∀ (p : Fin 8) (k : Fin 7240),
      staysWithin 3 10 (encoded3 p k) = false := by
  intro p k
  change AllExitCheck p k.val
  by_cases h0 : k.val < 128
  · exact of_all_batch allBatch000 p (by omega) (by omega)
  by_cases h1 : k.val < 256
  · exact of_all_batch allBatch001 p (by omega) (by omega)
  by_cases h2 : k.val < 384
  · exact of_all_batch allBatch002 p (by omega) (by omega)
  by_cases h3 : k.val < 512
  · exact of_all_batch allBatch003 p (by omega) (by omega)
  by_cases h4 : k.val < 640
  · exact of_all_batch allBatch004 p (by omega) (by omega)
  by_cases h5 : k.val < 768
  · exact of_all_batch allBatch005 p (by omega) (by omega)
  by_cases h6 : k.val < 896
  · exact of_all_batch allBatch006 p (by omega) (by omega)
  by_cases h7 : k.val < 1024
  · exact of_all_batch allBatch007 p (by omega) (by omega)
  by_cases h8 : k.val < 1152
  · exact of_all_batch allBatch008 p (by omega) (by omega)
  by_cases h9 : k.val < 1280
  · exact of_all_batch allBatch009 p (by omega) (by omega)
  by_cases h10 : k.val < 1408
  · exact of_all_batch allBatch010 p (by omega) (by omega)
  by_cases h11 : k.val < 1536
  · exact of_all_batch allBatch011 p (by omega) (by omega)
  by_cases h12 : k.val < 1664
  · exact of_all_batch allBatch012 p (by omega) (by omega)
  by_cases h13 : k.val < 1792
  · exact of_all_batch allBatch013 p (by omega) (by omega)
  by_cases h14 : k.val < 1920
  · exact of_all_batch allBatch014 p (by omega) (by omega)
  by_cases h15 : k.val < 2048
  · exact of_all_batch allBatch015 p (by omega) (by omega)
  by_cases h16 : k.val < 2176
  · exact of_all_batch allBatch016 p (by omega) (by omega)
  by_cases h17 : k.val < 2304
  · exact of_all_batch allBatch017 p (by omega) (by omega)
  by_cases h18 : k.val < 2432
  · exact of_all_batch allBatch018 p (by omega) (by omega)
  by_cases h19 : k.val < 2560
  · exact of_all_batch allBatch019 p (by omega) (by omega)
  by_cases h20 : k.val < 2688
  · exact of_all_batch allBatch020 p (by omega) (by omega)
  by_cases h21 : k.val < 2816
  · exact of_all_batch allBatch021 p (by omega) (by omega)
  by_cases h22 : k.val < 2944
  · exact of_all_batch allBatch022 p (by omega) (by omega)
  by_cases h23 : k.val < 3072
  · exact of_all_batch allBatch023 p (by omega) (by omega)
  by_cases h24 : k.val < 3200
  · exact of_all_batch allBatch024 p (by omega) (by omega)
  by_cases h25 : k.val < 3328
  · exact of_all_batch allBatch025 p (by omega) (by omega)
  by_cases h26 : k.val < 3456
  · exact of_all_batch allBatch026 p (by omega) (by omega)
  by_cases h27 : k.val < 3584
  · exact of_all_batch allBatch027 p (by omega) (by omega)
  by_cases h28 : k.val < 3712
  · exact of_all_batch allBatch028 p (by omega) (by omega)
  by_cases h29 : k.val < 3840
  · exact of_all_batch allBatch029 p (by omega) (by omega)
  by_cases h30 : k.val < 3968
  · exact of_all_batch allBatch030 p (by omega) (by omega)
  by_cases h31 : k.val < 4096
  · exact of_all_batch allBatch031 p (by omega) (by omega)
  by_cases h32 : k.val < 4224
  · exact of_all_batch allBatch032 p (by omega) (by omega)
  by_cases h33 : k.val < 4352
  · exact of_all_batch allBatch033 p (by omega) (by omega)
  by_cases h34 : k.val < 4480
  · exact of_all_batch allBatch034 p (by omega) (by omega)
  by_cases h35 : k.val < 4608
  · exact of_all_batch allBatch035 p (by omega) (by omega)
  by_cases h36 : k.val < 4736
  · exact of_all_batch allBatch036 p (by omega) (by omega)
  by_cases h37 : k.val < 4864
  · exact of_all_batch allBatch037 p (by omega) (by omega)
  by_cases h38 : k.val < 4992
  · exact of_all_batch allBatch038 p (by omega) (by omega)
  by_cases h39 : k.val < 5120
  · exact of_all_batch allBatch039 p (by omega) (by omega)
  by_cases h40 : k.val < 5248
  · exact of_all_batch allBatch040 p (by omega) (by omega)
  by_cases h41 : k.val < 5376
  · exact of_all_batch allBatch041 p (by omega) (by omega)
  by_cases h42 : k.val < 5504
  · exact of_all_batch allBatch042 p (by omega) (by omega)
  by_cases h43 : k.val < 5632
  · exact of_all_batch allBatch043 p (by omega) (by omega)
  by_cases h44 : k.val < 5760
  · exact of_all_batch allBatch044 p (by omega) (by omega)
  by_cases h45 : k.val < 5888
  · exact of_all_batch allBatch045 p (by omega) (by omega)
  by_cases h46 : k.val < 6016
  · exact of_all_batch allBatch046 p (by omega) (by omega)
  by_cases h47 : k.val < 6144
  · exact of_all_batch allBatch047 p (by omega) (by omega)
  by_cases h48 : k.val < 6272
  · exact of_all_batch allBatch048 p (by omega) (by omega)
  by_cases h49 : k.val < 6400
  · exact of_all_batch allBatch049 p (by omega) (by omega)
  by_cases h50 : k.val < 6528
  · exact of_all_batch allBatch050 p (by omega) (by omega)
  by_cases h51 : k.val < 6656
  · exact of_all_batch allBatch051 p (by omega) (by omega)
  by_cases h52 : k.val < 6784
  · exact of_all_batch allBatch052 p (by omega) (by omega)
  by_cases h53 : k.val < 6912
  · exact of_all_batch allBatch053 p (by omega) (by omega)
  by_cases h54 : k.val < 7040
  · exact of_all_batch allBatch054 p (by omega) (by omega)
  by_cases h55 : k.val < 7168
  · exact of_all_batch allBatch055 p (by omega) (by omega)
  exact of_all_batch allBatch056 p (by omega) (by omega)

#print axioms cap3_all_exits_by_ten
end P196.Agent116.Cap3

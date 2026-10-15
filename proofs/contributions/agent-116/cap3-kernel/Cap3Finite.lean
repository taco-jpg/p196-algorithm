import Cap3Batch000
import Cap3Batch001
import Cap3Batch002
import Cap3Batch003
import Cap3Batch004
import Cap3Batch005
import Cap3Batch006
import Cap3Batch007
import Cap3Batch008
import Cap3Batch009
import Cap3Batch010
import Cap3Batch011
import Cap3Batch012
import Cap3Batch013
import Cap3Batch014
import Cap3Batch015
import Cap3Batch016
import Cap3Batch017
import Cap3Batch018
import Cap3Batch019
import Cap3Batch020
import Cap3Batch021
import Cap3Batch022
import Cap3Batch023
import Cap3Batch024
import Cap3Batch025
import Cap3Batch026
import Cap3Batch027
import Cap3Batch028
import Cap3Batch029
import Cap3Batch030
import Cap3Batch031
import Cap3Batch032
import Cap3Batch033
import Cap3Batch034
import Cap3Batch035
import Cap3Batch036
import Cap3Batch037
import Cap3Batch038
import Cap3Batch039
import Cap3Batch040
import Cap3Batch041
import Cap3Batch042
import Cap3Batch043
import Cap3Batch044
import Cap3Batch045
import Cap3Batch046
import Cap3Batch047
import Cap3Batch048
import Cap3Batch049
import Cap3Batch050
import Cap3Batch051
import Cap3Batch052
import Cap3Batch053
import Cap3Batch054
import Cap3Batch055
import Cap3Batch056

namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxHeartbeats 0

theorem cap3_exits_by_nine :
    ∀ (p : Fin 8) (k : Fin 7240),
      validOuter (encoded3 p k) = true →
      staysWithin 3 9 (encoded3 p k) = false := by
  intro p k
  change ExitCheck p k.val
  by_cases h0 : k.val < 128
  · exact of_batch batch000 p (by omega) (by omega)
  by_cases h1 : k.val < 256
  · exact of_batch batch001 p (by omega) (by omega)
  by_cases h2 : k.val < 384
  · exact of_batch batch002 p (by omega) (by omega)
  by_cases h3 : k.val < 512
  · exact of_batch batch003 p (by omega) (by omega)
  by_cases h4 : k.val < 640
  · exact of_batch batch004 p (by omega) (by omega)
  by_cases h5 : k.val < 768
  · exact of_batch batch005 p (by omega) (by omega)
  by_cases h6 : k.val < 896
  · exact of_batch batch006 p (by omega) (by omega)
  by_cases h7 : k.val < 1024
  · exact of_batch batch007 p (by omega) (by omega)
  by_cases h8 : k.val < 1152
  · exact of_batch batch008 p (by omega) (by omega)
  by_cases h9 : k.val < 1280
  · exact of_batch batch009 p (by omega) (by omega)
  by_cases h10 : k.val < 1408
  · exact of_batch batch010 p (by omega) (by omega)
  by_cases h11 : k.val < 1536
  · exact of_batch batch011 p (by omega) (by omega)
  by_cases h12 : k.val < 1664
  · exact of_batch batch012 p (by omega) (by omega)
  by_cases h13 : k.val < 1792
  · exact of_batch batch013 p (by omega) (by omega)
  by_cases h14 : k.val < 1920
  · exact of_batch batch014 p (by omega) (by omega)
  by_cases h15 : k.val < 2048
  · exact of_batch batch015 p (by omega) (by omega)
  by_cases h16 : k.val < 2176
  · exact of_batch batch016 p (by omega) (by omega)
  by_cases h17 : k.val < 2304
  · exact of_batch batch017 p (by omega) (by omega)
  by_cases h18 : k.val < 2432
  · exact of_batch batch018 p (by omega) (by omega)
  by_cases h19 : k.val < 2560
  · exact of_batch batch019 p (by omega) (by omega)
  by_cases h20 : k.val < 2688
  · exact of_batch batch020 p (by omega) (by omega)
  by_cases h21 : k.val < 2816
  · exact of_batch batch021 p (by omega) (by omega)
  by_cases h22 : k.val < 2944
  · exact of_batch batch022 p (by omega) (by omega)
  by_cases h23 : k.val < 3072
  · exact of_batch batch023 p (by omega) (by omega)
  by_cases h24 : k.val < 3200
  · exact of_batch batch024 p (by omega) (by omega)
  by_cases h25 : k.val < 3328
  · exact of_batch batch025 p (by omega) (by omega)
  by_cases h26 : k.val < 3456
  · exact of_batch batch026 p (by omega) (by omega)
  by_cases h27 : k.val < 3584
  · exact of_batch batch027 p (by omega) (by omega)
  by_cases h28 : k.val < 3712
  · exact of_batch batch028 p (by omega) (by omega)
  by_cases h29 : k.val < 3840
  · exact of_batch batch029 p (by omega) (by omega)
  by_cases h30 : k.val < 3968
  · exact of_batch batch030 p (by omega) (by omega)
  by_cases h31 : k.val < 4096
  · exact of_batch batch031 p (by omega) (by omega)
  by_cases h32 : k.val < 4224
  · exact of_batch batch032 p (by omega) (by omega)
  by_cases h33 : k.val < 4352
  · exact of_batch batch033 p (by omega) (by omega)
  by_cases h34 : k.val < 4480
  · exact of_batch batch034 p (by omega) (by omega)
  by_cases h35 : k.val < 4608
  · exact of_batch batch035 p (by omega) (by omega)
  by_cases h36 : k.val < 4736
  · exact of_batch batch036 p (by omega) (by omega)
  by_cases h37 : k.val < 4864
  · exact of_batch batch037 p (by omega) (by omega)
  by_cases h38 : k.val < 4992
  · exact of_batch batch038 p (by omega) (by omega)
  by_cases h39 : k.val < 5120
  · exact of_batch batch039 p (by omega) (by omega)
  by_cases h40 : k.val < 5248
  · exact of_batch batch040 p (by omega) (by omega)
  by_cases h41 : k.val < 5376
  · exact of_batch batch041 p (by omega) (by omega)
  by_cases h42 : k.val < 5504
  · exact of_batch batch042 p (by omega) (by omega)
  by_cases h43 : k.val < 5632
  · exact of_batch batch043 p (by omega) (by omega)
  by_cases h44 : k.val < 5760
  · exact of_batch batch044 p (by omega) (by omega)
  by_cases h45 : k.val < 5888
  · exact of_batch batch045 p (by omega) (by omega)
  by_cases h46 : k.val < 6016
  · exact of_batch batch046 p (by omega) (by omega)
  by_cases h47 : k.val < 6144
  · exact of_batch batch047 p (by omega) (by omega)
  by_cases h48 : k.val < 6272
  · exact of_batch batch048 p (by omega) (by omega)
  by_cases h49 : k.val < 6400
  · exact of_batch batch049 p (by omega) (by omega)
  by_cases h50 : k.val < 6528
  · exact of_batch batch050 p (by omega) (by omega)
  by_cases h51 : k.val < 6656
  · exact of_batch batch051 p (by omega) (by omega)
  by_cases h52 : k.val < 6784
  · exact of_batch batch052 p (by omega) (by omega)
  by_cases h53 : k.val < 6912
  · exact of_batch batch053 p (by omega) (by omega)
  by_cases h54 : k.val < 7040
  · exact of_batch batch054 p (by omega) (by omega)
  by_cases h55 : k.val < 7168
  · exact of_batch batch055 p (by omega) (by omega)
  exact of_batch batch056 p (by omega) (by omega)

#print axioms cap3_exits_by_nine
end P196.Agent116.Cap3

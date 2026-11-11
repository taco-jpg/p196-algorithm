#!/bin/bash
# r12b khx controls. POSITIVE (known exteriors / band templates: must SURVIVE to the cap) and NEGATIVE (must DIE).
cd ~/p196_run/r12b
K=${KHX:-bin/khx}; A="-kmax 60 -nodecap 30000000 -sec 120 ${XA:-}"
run(){ echo "== $1 :: $(nice -n 10 $K "${@:2}" $A | tr "\n" " ")"; }
echo "# positive (must SURVIVE)"
run "p11 wire"            10 -g 00001110001
run "p12 N12 wire"        10 -g 000100010001
run "p22 = p11^2"         10 -g 0000111000100001110001
run "p11^3 (L=33)"        10 -g 00001110001 -L 33
run "N12^2 (0001)^6"      10 -g 0001 -L 24
run "(01)^4 (bx saturates, no stream; khx expected to survive)" 10 -g 01 -L 8
run "base13 band {8,16}"  13 -g 1010010000
run "base4 wire+band"     4 -g 011001
run "base11 001"          11 -g 001
run "base11 001001"       11 -g 001001
run "base17 100001"       17 -g 100001
run "base26 01"           26 -g 01
run "base20 00010001"     20 -g 00010001
run "base2 10"            2 -g 10
run "base4 100"           4 -g 100
run "base8 1000"          8 -g 1000
run "base16 10000"        16 -g 10000
run "base32 100000"       32 -g 100000
run "base3 11100"         3 -g 11100
echo "# negative (must DIE)"
run "01 L=36 (8|p thm: K=3)"   10 -g 01 -L 36
run "0001 L=40 (Thm A)"        10 -g 0001 -L 40
run "0001 L=16 (bx dies d13)"  10 -g 0001 -L 16
run "0001 L=20 (bx dies d6)"   10 -g 0001 -L 20
run "0001 L=28 (bx dies d10)"  10 -g 0001 -L 28
echo CTRL_DONE

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
bash reproduce_20k.sh
python3 test_exterior.py
c++ -std=c++17 -O3 exterior_pump.cpp -o /tmp/n23_exterior_pump
for Q in 6016 7000 7001 8000; do
    output=$(/tmp/n23_exterior_pump "$Q" 20000)
    echo "$output"
    hash=$(echo "$output" | sed -n 's/.*checksum=\([0-9]*\).*/\1/p')
    expect=$(awk -F '\t' -v q="$Q" 'NR>1 && $1==q {print $10}' parametric20k.tsv)
    [[ -n "$hash" && "$hash" == "$expect" ]]
done
sed 's/core<1000/core<2/' protected_20k.cpp > /tmp/n23_digit_min2.cpp
sed 's/core<1000/core<2/' protected_bigint.cpp > /tmp/n23_limb_min2.cpp
c++ -std=c++17 -O3 /tmp/n23_digit_min2.cpp -o /tmp/n23_digit_min2
c++ -std=c++17 -O3 /tmp/n23_limb_min2.cpp -o /tmp/n23_limb_min2
x=$(/tmp/n23_digit_min2 6016 20000)
y=$(/tmp/n23_limb_min2 6016 20000)
echo "$x"
echo "$y"
[[ "$x" == *'checksum_mod1000000007=788241103'* ]]
[[ "$y" == *'checksum_mod1000000007=788241103'* ]]

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 exterior_pump.cpp -o /tmp/n23_pump_100k
c++ -std=c++17 -O3 protected_thousands.cpp -o /tmp/n23_thousands_100k
sed 's/core<1000/core<2/' protected_20k.cpp > /tmp/n23_digits100k.cpp
c++ -std=c++17 -O3 /tmp/n23_digits100k.cpp -o /tmp/n23_digits_100k
while IFS="$(printf '\t')" read -r horizon q width gam0 gam1 trims minband digits checksum; do
  [[ "$horizon" == "horizon" ]] && continue
  output=$(/tmp/n23_pump_100k "$q" "$horizon")
  echo "$output"
  [[ "$output" == *"minL=$minband"* ]]
  [[ "$output" == *"finalDigits=$digits"* ]]
  [[ "$output" == *"exteriorWidth=$width"* ]]
  [[ "$output" == *"gamma0=$gam0"* ]]
  [[ "$output" == *"gamma1=$gam1"* ]]
  [[ "$output" == *"trim=$trims"* ]]
  [[ "$output" == *"checksum=$checksum"* ]]
  # At Q-1 the same protected-9 transducer is no longer valid throughout
  # this horizon. This is NOT evidence that the decimal number palindromes.
  if /tmp/n23_pump_100k "$((q-1))" "$horizon" >/tmp/n23_under_threshold.out 2>&1; then
    echo "ERROR: nonsharp threshold at $horizon" >&2; exit 4
  fi
done < threshold_100k.tsv
digits=$(/tmp/n23_digits_100k 30037 100000)
thousands=$(/tmp/n23_thousands_100k 30037 100000)
echo "$digits"
echo "$thousands"
[[ "$digits" == *"final_len=101386"* && "$digits" == *"min_center18=2"* && "$digits" == *"checksum_mod1000000007=886568206"* ]]
[[ "$thousands" == *"lastdigits=101386"* && "$thousands" == *"central_min=2"* && "$thousands" == *"hash=886568206"* ]]

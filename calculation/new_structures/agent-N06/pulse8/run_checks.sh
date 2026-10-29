#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
c++ -std=c++17 -O3 pulse8_digit.cpp -o /tmp/n06p_digit
c++ -std=c++17 -O3 pulse8_gmp.cpp -lgmpxx -lgmp -o /tmp/n06p_gmp
c++ -std=c++17 -O3 pulse8_front.cpp -o /tmp/n06p_front
for L in 1 2 10 221 222; do
  T=$((476 + 88*L))
  /tmp/n06p_digit scan "$L" "$T" > /tmp/n06p_sample.txt
  cat /tmp/n06p_sample.txt
  grep -q "first8_failure=$T palindrome=-1 gamma_failure=-1" /tmp/n06p_sample.txt
done
/tmp/n06p_digit scan 1 800 1 | grep -q 'first8_failure=310'
/tmp/n06p_digit scan 1 800 2 | grep -q 'first8_failure=348'
/tmp/n06p_digit seed 222 > /tmp/n06p_seed.txt
echo '27422d16426c85d5c74498fc382958d8ff6bd78335dac425a805ec99ad4d95e8  /tmp/n06p_seed.txt' | sha256sum -c -
/tmp/n06p_digit scan 222 20000 | tee /tmp/n06p_digit_result.txt
/tmp/n06p_gmp 20000 < /tmp/n06p_seed.txt | tee /tmp/n06p_gmp_result.txt
expected='first8_failure=-1 palindrome=-1 gamma_failure=-1 modulo1000000007=383594414 fnv64=746813162037088509'
grep -q "$expected" /tmp/n06p_digit_result.txt
grep -q "$expected" /tmp/n06p_gmp_result.txt
/tmp/n06p_front 222 20012 | grep -q 't=20012 len=18980 frontier=7'
echo N06_PULSE8_CHECKS_PASSED
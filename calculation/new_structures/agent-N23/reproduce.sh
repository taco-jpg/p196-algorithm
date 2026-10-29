#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 make_control.py /tmp/n23_control.json /tmp/n23_control.txt
printf '%s  %s\n' \
  '1b643c058c5ae26d1a1851a69f513988f9b5e27727be0e8b5a6e7f45a5c243d7' /tmp/n23_control.json \
  '57b40746c09f824a7e1c1a44bf2cf7eee035417b71ffad6d52ece04925bef3b3' /tmp/n23_control.txt | sha256sum -c -
python3 poly_certificate.py /tmp/n23_control.json
python3 poly_certificate.py decimal_b100_twisted_path.json
python3 check_decimal.py
c++ -std=c++17 -O3 replay.cpp -o /tmp/n23_digit_replay
/tmp/n23_digit_replay /tmp/n23_control.txt 20000

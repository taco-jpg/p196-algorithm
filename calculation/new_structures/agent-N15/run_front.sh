#!/bin/sh
set -eu
cd "$(dirname "$0")"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
g++ -O3 -std=c++17 -Wall -Wextra front_profile.cpp -o "$tmp/profile"
g++ -O3 -std=c++17 -Wall -Wextra front_verify.cpp -o "$tmp/verify"
"$tmp/profile" > "$tmp/profile.csv"
"$tmp/verify" > "$tmp/verify.csv"
python3 - "$tmp/profile.csv" "$tmp/verify.csv" <<'PY'
import csv,sys,math
expected=list(csv.reader(open('front_profile.csv')))
a=list(csv.reader(open(sys.argv[1])))
b=list(csv.reader(open(sys.argv[2])))
assert expected==a,(len(expected),len(a))
assert len(a)==len(b)==66
for x,y in zip(a,b):assert x[:3]==y
for h in range(7,13):
    pts=[(int(row[1])/2**h,int(row[2])/2**h) for row in a if int(row[0])==h]
    n=len(pts); sx=sum(x for x,y in pts); sy=sum(y for x,y in pts)
    slope=(n*sum(x*y for x,y in pts)-sx*sy)/(n*sum(x*x for x,y in pts)-sx*sx)
    intercept=(sy-slope*sx)/n
    print('FRONT_FIT',h,'slope',format(slope,'.5f'),'intercept',format(intercept,'.5f'))
print('N15_66_POINT_DYADIC_FRONT_PROFILE_PASS')
PY

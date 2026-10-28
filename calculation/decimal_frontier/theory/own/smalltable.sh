#!/bin/bash
# exterior cycles (G, p, count of e-streams) for p<=PM, all bases in list
PM=$1; shift
for b in "$@"; do
  ./gamlist $b 1 $PM emit > /tmp/gl_$b.txt 2>/dev/null
  ( ulimit -v 1500000; timeout 25 ./bauto4 $b /tmp/gl_$b.txt -cap 300000 2> /tmp/gl_$b.err ) | awk -v b=$b '{split($3,a,"=");split($4,c,"="); key=$4" "$3; g=c[2]; n=gsub(/1/,"1",g); cnt[ "p"substr($3,3)" g="c[2]" G="n ]++} END{for(k in cnt) print "b="b" "k" nE="cnt[k]}' | sort -t= -k3 -n | head -12
  echo "b=$b: $(tail -1 /tmp/gl_$b.err)"
done

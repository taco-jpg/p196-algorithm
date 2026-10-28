#!/bin/bash
# B-level uniqueness: number of distinct B-cycles (position-choice histories) per accepted e, no symmetry quotient
cd /home/claude/research/w5_exterior
bin/bxl 10 -g 0000111000100001110001 -count 130 -sec 1200 -nosym 2>&1 | awk '/COUNT/{print} /ACCEPTPATHS/{split($2,a,"=");split($3,d,"=");split($4,h,"="); if(!(a[2] in first)) first[a[2]]=d[2]; last[a[2]]=h[2]; ld[a[2]]=d[2]} END{for(k in first) print "e="k" first_depth="first[k]" last_depth="ld[k]" histories_at_last="last[k]}'

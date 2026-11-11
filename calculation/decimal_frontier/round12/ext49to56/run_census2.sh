#!/bin/bash
# r12e census pass 1, variant with shard CLAIMS (atomic mkdir lock out/census/T{T}_s{ii}.lock): several drivers may run at the same
# time on the same T list without duplicating a shard; a shard is skipped if it is done or claimed.  Otherwise identical to
# run_census.sh (fc_enum2 | khxc, r12b pass-1 options).   usage: run_census2.sh "54" N JOBS
cd ~/p196_run/r12e
TL=${1:-"54"}; N=${2:-20}; JOBS=${3:-4}
ARGS="-kmax 400 -nodecap 20000000 -sec 4 -summary -krep 40"
mkdir -p out/census logs/census
for T in $TL; do
  case $T in 49) TOT=94598340;; 50) TOT=146010697;; 51) TOT=225446789;; 52) TOT=348243213;; 53) TOT=538112178;;
             54) TOT=831810647;; 55) TOT=1286235064;; 56) TOT=1989587605;; *) TOT=100000000;; esac
  SAMP=$(( TOT / (N * 25) ))
  for ((i=0;i<N;i++)); do s=$(printf %02d $i); echo "$T $i $N $SAMP $s"; done
done | xargs -P $JOBS -L 1 bash -c '
  T=$0; i=$1; N=$2; SAMP=$3; s=$4
  [ -f out/census/T${T}_s$s.done ] && exit 0
  mkdir out/census/T${T}_s$s.lock 2>/dev/null || exit 0
  nice -n 10 ~/p196_run/r12e/bin/fc_enum2 10 $T -shard $i $N 2> logs/census/fce_T${T}_s$s.log \
   | nice -n 10 ~/p196_run/r12e/bin/khxc 10 -f /dev/stdin '"$ARGS"' -samp $SAMP > out/census/T${T}_s$s.out 2> logs/census/khxc_T${T}_s$s.err
  if grep -q KHXC_SUMMARY out/census/T${T}_s$s.out && grep -q "^FCE" logs/census/fce_T${T}_s$s.log; then touch out/census/T${T}_s$s.done; fi
  echo "$(date -u +%FT%TZ) T=$T shard $s finished"
'
echo "$(date -u +%FT%TZ) CENSUS_DONE $TL"

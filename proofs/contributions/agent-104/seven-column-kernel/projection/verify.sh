#!/usr/bin/env bash
set -euo pipefail
: "${P196_LEAN:=lean}"
: "${P196_BUILD:=/tmp/p196-agent104-projection-build}"
mkdir -p "$P196_BUILD"
"$P196_LEAN" --version
"$P196_LEAN" -o "$P196_BUILD/LychrelDigitSums.olean" proofs/research/continuation/LychrelDigitSums.lean
LEAN_PATH="$P196_BUILD" "$P196_LEAN" -o "$P196_BUILD/PrefixInverse.olean" proofs/contributions/agent-104/seven-column-kernel/PrefixInverse.lean
LEAN_PATH="$P196_BUILD" "$P196_LEAN" -o "$P196_BUILD/ActualPrefix.olean" proofs/contributions/agent-104/seven-column-kernel/ActualPrefix.lean

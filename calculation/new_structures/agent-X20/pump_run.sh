#!/bin/sh
set -eu
c++ -O3 -std=c++17 calculation/new_structures/agent-X20/pump_guard20k.cpp -o /tmp/x20pump
/tmp/x20pump 427 509 10000 0
/tmp/x20pump 427 509 20001 10000
/tmp/x20pump 509 427 10000 0
/tmp/x20pump 509 427 20001 10000
c++ -O3 -std=c++17 calculation/new_structures/agent-X20/asymmetric20k.cpp -o /tmp/x20big
/tmp/x20big 427 509 20000
/tmp/x20big 509 427 20000

#!/bin/bash
# r12b: start a command fully detached (macOS has no setsid): bg.sh LOGFILE cmd args...
LOG=$1; shift
( nohup "$@" > "$LOG" 2>&1 < /dev/null & )

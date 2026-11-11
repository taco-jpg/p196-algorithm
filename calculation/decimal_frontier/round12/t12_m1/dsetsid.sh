#!/bin/bash
# detach: new session (perl POSIX::setsid, macOS has no setsid binary) + nohup
exec nohup perl -MPOSIX -e "POSIX::setsid(); exec @ARGV or die" -- "$@"

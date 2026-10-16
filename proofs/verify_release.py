#!/usr/bin/env python3
from replay_original_layout import main
import sys
if __name__ == '__main__':
    main(['--',sys.executable,'proofs/verify_release.py',*sys.argv[1:]])

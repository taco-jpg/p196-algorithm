#!/usr/bin/env python3
"""R30 exact two-parameter decimal return checker."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'calculation'/'new_structures'/'R30'))
from parametric import main
if __name__=='__main__':main()

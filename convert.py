#!/usr/bin/env python

import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from collada_povray import ColladaPovray

model = ColladaPovray(sys.argv[1])
model.convert()
import os, sys

thisdir = os.path.dirname(__file__)

for d in ['../src']:
    libdir = os.path.join(thisdir, d)
    if libdir not in sys.path:
        sys.path.insert(0, libdir)

import os
import sys
from importlib.machinery import SourceFileLoader

sys.path.insert(0, os.path.dirname(__file__))

wsgi = SourceFileLoader("wsgi", "src/passenger_wsgi.py").load_module()
application = wsgi.application
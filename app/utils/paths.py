import os
import sys

def addProjectRoot():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

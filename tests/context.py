"""
Module to
"""


import os
import sys
# sys.path.insert(0, os.path.abspath('..'))
file_path = os.path.realpath(__file__)
path = os.path.dirname(file_path) + os.sep + '..'
sys.path.append(path)

import hyppocratic
import hyppocratic.CommentaryToEpidoc as CommentaryToEpidoc

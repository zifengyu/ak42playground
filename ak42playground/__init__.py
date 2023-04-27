from .lib import *
import sys


def parse_log():
    filename = sys.argv[1]
    parse_file(filename)

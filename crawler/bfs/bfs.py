import sys
sys.path.append('../shared')

from pre_processing import PreProcessing

if (__name__ == "__main__"):
    p = PreProcessing("../../site.txt")
    p.print_info()
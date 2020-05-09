import numpy as np
import pandas as pd
import sys
import csv


if __name__ == "__main__":
    print("hi")
    input_args = sys.argv
    data = np.loadtxt(input_args[1], delimiter=',', dtype=float)

    print(data)

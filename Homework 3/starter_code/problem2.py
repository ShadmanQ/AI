import numpy as np
import pandas as pd
import sys
import csv


def normalize_and_prep(raw_data):
    intercepts = np.zeros((raw_data.shape[0], 1))

    for i in range(raw_data.shape[1]):
        col = raw_data[:, i]
        mu = np.mean(col)
        dev = np.std(col)
        for i in range(len(col)):
            col[i] = (col[i] - mu) / dev
        intercepts = np.append(intercepts, col[:, None], 1)

    return intercepts


def regression(data_set, alphas):
    reg_function = alphas[8] * data_set[1][2]
    print(reg_function)


if __name__ == "__main__":
    betas = np.zeros(3)
    input_args = sys.argv
    data = np.loadtxt(input_args[1], delimiter=',', dtype=float)
    data2 = pd.read_csv(input_args[1], header=None)
    scaled_data = normalize_and_prep(data)
    learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1,
                      0.5, 1, 5, 10]

    regression(scaled_data, learning_rates)

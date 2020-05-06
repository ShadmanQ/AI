import numpy as np
import sys
import csv


class Perceptron():
    training_data = None
    weights = None

    def __init__(self, training_data, weights):
        self.training_data = training_data
        self.weights = weights

    def predict(self):
        for line in self.training_data:
            print(line)


def main():
    input_args = sys.argv
    data = np.loadtxt(input_args[1], delimiter=',', dtype=float)
    weights = np.zeros(3)
    Pete = Perceptron(data, weights)
    print(Pete.training_data)
    Pete.predict()


main()

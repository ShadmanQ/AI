import numpy as np
import sys
import csv


class Perceptron():
    training_data = None
    weights = None

    def __init__(self, training_data, weights):
        self.training_data = training_data
        self.weights = weights
        self.bias = np.ones(self.training_data.shape[0])

    def train(self):
        for i in range(len(self.training_data)):
            eval = self.bias[i] * self.weights[0] + self.training_data[i][0] * \
                self.weights[1] + self.training_data[i][1] + \
                self.weights[2] * self.training_data[i][2]
            print(eval, np.sign(eval) == 1)


def main():
    input_args = sys.argv
    data = np.loadtxt(input_args[1], delimiter=',', dtype=float)
    print(data.shape)
    weights = np.zeros(3)
    Pete = Perceptron(data, weights)
    # print(Pete.training_data)
    Pete.train()


main()

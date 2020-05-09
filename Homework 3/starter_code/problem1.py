import numpy as np
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def visualize_scatter(df,
                      feat1=0, feat2=1, labels=2,
                      weights=[-1, -1, 1], title=''):
    """
    Scatter plot feat1 vs feat2.
    Assumes +/- binary labels.
    Plots first and second columns by default.
    Args:
      - df: dataframe with feat1, feat2, and labels
      - feat1: column name of first feature
      - feat2: column name of second feature
      - labels: column name of labels
      - weights: [w1, w2, b]
    """

    # Draw color-coded scatter plot
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[labels]])
    ax = df.plot(x=feat1, y=feat2, kind='scatter', c=colors)

    # Get scatter plot boundaries to define line boundaries
    xmin, xmax = ax.get_xlim()

    # Compute and draw line. ax + by + c = 0  =>  y = -a/b*x - c/b
    a = weights[0]
    b = weights[1]
    c = weights[2]

    def y(x):
        return (-a / b) * x - c / b

    line_start = (xmin, xmax)
    line_end = (y(xmin), y(xmax))
    line = mlines.Line2D(line_start, line_end, color='red')
    ax.add_line(line)

    ax.set_title(title or f"Scatter of feature {feat1} vs {feat2}")
    plt.show()


class Perceptron():
    training_data = None
    weights = None

    def __init__(self, training_data, weights):
        self.training_data = training_data
        self.weights = weights
        self.bias = np.ones(self.training_data.shape[0])

    def validate(self):
        correct = 0
        incorrect = 0
        for i in range(len(self.training_data)):
            hi = self.predict(self.training_data[i], self.bias[i])
            if (hi == self.training_data[i][2]):
                correct += 1
            else:
                incorrect += 1
        return correct, incorrect

    def predict(self, data_point, bias):
        eval = (bias * self.weights[0]) + (self.weights[1] *
                                           data_point[0]) + (self.weights[2] * data_point[1])
        if eval > 0:
            return 1
        else:
            return -1

    def train(self):
        for i in range(len(self.training_data)):
            value = self.predict(self.training_data[i], self.bias[i])
            if value < self.training_data[i][2]:
                self.weights += [1, self.training_data[i][0], self.training_data[i][1]]
            if value > self.training_data[i][2]:
                self.weights -= [1, self.training_data[i][0], self.training_data[i][1]]


if __name__ == "__main__":
    np.set_printoptions(suppress=True)
    input_args = sys.argv
    data = np.loadtxt(input_args[1], delimiter=',', dtype=float)

    weights = np.zeros(3)
    output_weights = np.empty(data[0].shape, data[0].dtype)

    Pete = Perceptron(data, weights)
    running = True
    while(running):
        Pete.train()
        right, wrong = Pete.validate()
        add = Pete.weights.copy()
        output_weights = np.append(output_weights, add)
        if (wrong == 0):
            break

    # reformatting columns to fit specifications.
    rows = int(output_weights.shape[0]) / 3
    rows = int(rows)
    output_weights = output_weights.reshape(rows, 3)
    output_weights[:, [0, 1]] = output_weights[:, [1, 0]]
    output_weights[:, [1, 2]] = output_weights[:, [2, 1]]
    output_weights = output_weights.astype('int')

    pd_data = pd.read_csv(input_args[1], header=None)
    visualize_scatter(pd_data, weights=output_weights[output_weights.shape[0] - 1])
    np.savetxt(input_args[2], output_weights, delimiter=',', fmt='%i')

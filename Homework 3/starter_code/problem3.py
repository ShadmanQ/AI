import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from time import time
import sys

if __name__ == "__main__":
    input_args = sys.argv

    trees = plt.imread("trees.png")
    trees = np.array(trees, dtype=np.float64) / 255

    kmean = KMeans(n_clusters=3, random_state=0).fit(trees)

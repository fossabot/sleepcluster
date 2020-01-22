import numpy as np
from tqdm import tqdm
from sklearn.cluster import KMeans

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the K-Means Cluster 'Elkan' Algorithm
class KMeansCluster(cluster.Cluster):

	def __init__(self, k=3, init='kmeans++', n_init=10, max_iter=100, tol=1e-4, seed=None):
		self.kmeans = KMeans(n_clusters=k, init=init, n_init=n_init, max_iter=max_iterm tol=tol, seed=seed)

	def fit(self, data, weights=None):
		return self.kmeans.fit(data, weights=weights)

	def predict(self, data, weights=None):
		return self.kmeans.predict(data, weights=weights)

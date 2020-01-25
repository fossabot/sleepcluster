import numpy as np
from tqdm import tqdm
from sklearn.cluster import KMeans

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the K-Means Cluster 'Elkan' Algorithm
class KMeansCluster(cluster.Cluster):

	def __init__(self, k=3, init='k-means++', n_init=10, max_iter=100, tol=1e-4, seed=None):
		self.cluster = KMeans(n_clusters=k, init=init, n_init=n_init,
								max_iter=max_iter, tol=tol, random_state=seed)

	def fit(self, data, weights=None):
		return self.cluster.fit(data, sample_weight=weights)

	def predict(self, data, weights=None):
		return self.cluster.predict(data, sample_weight=weights)

	def load(self, model):
		if model['model'] == 'kmeans':
			self.cluster = KMeans(n_clusters=len(model['centers']))
			self.cluster.cluster_centers_ = model['centers']
			self.cluster.inertia_ = model['inertia']
			self.cluster.n_iter_ = model['n_iter']
		return	self

	def model(self):
		model = {
					'model': 'kmeans',
					'centers': self.cluster.cluster_centers_,
					'inertia': self.cluster.inertia_,
					'n_iter': self.cluster.n_iter_
				}
		return model

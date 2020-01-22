import numpy as np
from tqdm import tqdm
from sklearn.cluster import DBSCAN

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the DBSCAN Cluster Algorithm
class DBSCANCluster(cluster.Cluster):

	def __init__(self, eps=0.5, min_samples=5):
		self.cluster = DBSCAN(eps, min_samples)

	def fit(self, data, weights=None):
		return self.cluster.fit(data, weights=weights)

	def predict(self, data, weights=None):
		raise NotImplementedError( "No predict function implemented" )

import numpy as np
from tqdm import tqdm
from sklearn.cluster import OPTICS

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the OPTICS Cluster Algorithm
class OPTICSCluster(cluster.Cluster):

	def __init__(self, min_samples=5, max_eps=np.inf, method='xi', eps=None, xi=0.5):
		self.cluster = OPTICS(min_samples=min_samples, max_eps=max_eps, clustr_method=method,
								eps=eps, xi=xi)

	def fit(self, data, weights=None):
		return self.cluster.fit(data)

	def predict(self, data, weights=None):
		raise NotImplementedError( "No predict function implemented" )

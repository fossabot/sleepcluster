import numpy as np
from tqdm import tqdm

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the DBSCAN Cluster Algorithm
class DBSCANCluster(cluster.Cluster):

	def __init__(self):
		pass

	def cluster(self, *args, **kwargs):
		raise NotImplementedError( "No cluster function implemented" )
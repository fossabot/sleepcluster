import numpy as np
from tqdm import tqdm

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


# A Cluster plugin that runs the Density Sensitive
#	Irregular Guassian (DSIG) Clustering Algorithm
class DSIGCluster(cluster.Cluster):

	class CoreCluster:

		def __init__(self, mu, sigma, epsilon, delta):
			self.mu = mu
			self.sigma = sigma
			self.epsilon = epsilon
			self.delta = delta
			self.cores = []

	class CorePoint:

		def __init__(self, point, cluster):
			self.point = point
			self.cluster = cluster


	def __init__(self, n_clusters=None, max_e=np.inf, n_init=10, max_iter=200,
					tol=1e-4, noise=False, seed=None):
		self.n_clusters = n_clusters
		self.max_e = max_e
		self.n_init = n_init
		self.max_iter = max_iter
		self.tol = tol
		self.noise = noise
		self.seed = seed
		self.clusters = None

	def addCluster(self, core_point, mu, sigma, epsilon, delta):
		cluster = CoreCluster(mu, sigma, epsilon, delta)
		cluster.cores.append(core_point)
		core_point.cluster = cluster
		self.clusters.append(cluster)
		return cluster

	def distance(self, p1, p2):
		return np.linalg.norm(p1 - p2)

	def inertia(self):
		'''
		KMEANS uses Within Cluster Sum of Squares
		'''
		pass

	def calculateDissociation(self, core_point):
		'''
		Core points may dissociate if:
			The pull to remain with its associated points exceeds
				the pull to remain with the cluster.
		'''
		pass

	def calculateAbsorption(self, core_point):
		'''
		Core points may be absorbed if:
			They are sufficiently overlapped to imply the same cluster
				This includes similar delta levels to avoid
					wrongfully merging overlapping clusters
		'''
		pass

	def calculateTransfer(self, core_point):
		'''
		Core points may be transferred if:
			The pull to dissociate from old cluster or the pull to be absorbed to a new cluster
				exceeds pull to remain in the same cluster
		'''
		pass

	def calculateDeconstruct(self, core_point):
		'''
		Core points may be deconstructed if:
			They are too close to another core point of the same cluster,
				implying redundancy
		'''
		pass

	def calculateConstruct(self, core_point):
		'''
		Core points may be created if:
			There are data points (claimed or not) that exist just around the epsilon boundary
				Example: 0.9*epsilon to 1.5*epsilon range
				If they are unclaimed, this allows for the expansion of clusters
				If they are claimed, it begins a struggle of dominance (see absorption)
		'''
		pass

	def fit(self, data, weights=None):
		'''
		If k is None - Fluid clustering
		If k is int - Rigid clustering

		Basic principle:
			Each cluster contains a collection of "core points"
			These core points are gaussian models
			A cluster defines the following properties of all core points:
				mu - centroid point
				gamma - falloff point (when the normal distribution begins)
				sigma - standard deviation (sharpness of the falloff)
				epsilon - outer cutoff limit
				delta - peak density (within gamma range)
			A cluster is considered to be overall some gaussian mixture
			This results in clusters that can be irregularly shaped,
				vary in density between each other, and thus overlap
		Finer details:
			The goal is to minimize inertia in an EM Algorithm
			Core points are initialized anywhere and are not actual data points
				as in OPTICS
			Core points may freely dissociate and reassociate with different clusters,
				whichever provides the overall model with the lowest inertia
			When clustering is fluid, this allows the creation and absorption of clusters
			Clusters can spawn or deconstruct core points as needed to lower inertia
		Details around core points:
			Core points strive to include as many points as it can (and as close as it can)
			In fluid clustering, core points can dissociate and form a new cluster
				It may subsequently be absorbed into another cluster, or draw yet more
				points to it
			In rigid clustering, core points must fully transition to a different cluster
				They cannot dissociate unless there is also an adequate pull to join a cluster

		TO DO:
			Define Cost Function to optimize
			Define Algorithm
		'''
		pass

	def predict(self, data, weights=None):
		'''
		Points are classified into cluster by determining probability of belonging
			to each cluster
		Probability is determined by proximity to cluster weighted by the distribution
			model of that cluster (mu, gamma, sigma, epsilon, delta)
		'''
		pass

	def load(self, model):
		return	self

	def model(self):
		pass

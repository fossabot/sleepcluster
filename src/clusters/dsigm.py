import numpy as np
from tqdm import tqdm
from sklearn.datasets import make_spd_matrix
import math

from lib import data as dataLib
from clusters import abstract_cluster as cluster
from dataobjects import dataobject as dataObject


def array(*args):
	'''
	Returns a numpy array of each argument
	'''
	if len(args) == 0:
		raise ValueError("Must contain at least one argument")
	np_args = []
	for i in range(len(args)):
		np_args.append(np.asarray(args[i]))
	return np_args

def checkDimensionality(*args):
	'''
	Check that all arguments are the same dimension
	Return that dimension
	'''
	if len(args) == 0:
		raise ValueError("Must contain at least one argument")
	np_args = array(args)
	ndim = np_args[0].ndim
	for v in np_args[1:]:
		if v.ndim != ndim:
			raise ValueError("Arguments must be the same dimensions")
	return ndim - 1

def ellipsoid(n, components):
	'''
	Compute the volume of an n-dimensional ellipsoid
	n: number of dimensions
	components: vectors defining axes of ellipsoid
	'''
	dim = checkDimensionality(components)
	if dim != n:
		raise ValueError("Arguments must have correct relative dimensions")
	ellipsoid_num = 2 * np.power(np.pi, n / 2) * np.prod(np.linalg.norm(components, axis=-1))
	ellipsoid_denom = n * math.gamma(n / 2)
	return ellipsoid_num / ellipsoid_denom

def withinEllipsoid(center, components, points):
	'''
	Computes whether points lie within the ellipsoid
	n: dimensions
	ellipse: vectors definig aces of ellipsoid
	points: ndarray of points
	'''
	dim = checkDimensionality(center, points)
	param_dim = checkDimensionality(components)
	if param_dim - dim != 1:
		raise ValueError("Arguments must have correct relative dimensions")
	components_norm = np.linalg.norm(components, axis=-1)
	if np.any(components_norm <= 0):
		ellipse = np.inf
	else:
		ellipse = np.square((points - center) / components_norm)
	if dim == 0:
		mask = ellipse <= 1
	else:
		mask = np.sum(ellipse, axis=-1) <= 1
	return mask

def pdf(x, mu=0, sigma=[1], gamma=[0], epsilon=[np.inf]):
	'''
	Calculate probability density function of
		a modified multivariate normal distribution
	x: quantiles, with the last axis of 'x' denoting components
	mu: mean of the distribution (default 0)
	sigma: (co)variance of the distribution (default 1)
	gamma: distribution falloff (default 0)
	epsilon: distribution cutoff (default np.inf)
	'''
	x, mu, sigma, gamma, epsilon = array(x, mu, sigma, gamma, epsilon)
	dim = checkDimensionality(x, mu)
	param_dim = checkDimensionality(sigma, gamma, epsilon)
	if param_dim - dim != 1:
		raise ValueError("Arguments must have correct relative dimensions")
	gamma_norm = np.linalg.norm(gamma, axis=-1)
	sigma = sigma.reshape((param_dim, param_dim))
	k_gauss = np.sqrt(2 * np.pi * np.linalg.det(sigma))
	h = 1 / (1 + 2 * gamma_norm / k_gauss)
	k = h / k_gauss
	g = np.exp(-0.5 * np.linalg.norm(sigma, axis=-1) * np.square((x - mu - gamma_norm)))
	out = np.zeros(len(x))
	mask = withinEllipsoid(mu, gamma, x)
	inverted_mask = np.invert(mask)
	cutoff_mask = np.invert(withinEllipsoid(mu, epsilon, x))
	out[mask] = k
	out[inverted_mask] = k * g
	out[cutoff_mask] = 0
	return out


# A Cluster plugin that runs the Density Sensitive
#	Irregular Gaussian Mixture (DSIGM) Clustering Algorithm
class DSIGCluster(cluster.Cluster):

	class CoreCluster:

		def __init__(self, gamma, sigma, epsilon, delta):
			self.cores = []

	class CorePoint:

		def __init__(self, mu, cluster):
			self.mu = mu
			self.gamma = gamma
			self.sigma = sigma
			self.epsilon = epsilon
			self.delta = delta
			self.points = []
			self.cluster = cluster


	def __init__(self, n_clusters=None, n_cores=50, max_e=np.inf, n_init=10, max_iter=200,
					tol=1e-4, noise=False, seed=None):
		self.fluid = False if n_clusters is None else True
		self.n_clusters = n_cores if n_clusters is None else n_clusters
		self.n_cores = n_cores
		self.max_e = max_e
		self.n_init = n_init
		self.max_iter = max_iter
		self.tol = tol
		self.noise = noise
		self.seed = seed
		self.clusters = []
		self.cores = []

	def initializeCores(self):
		'''
		Create n_clusters core_points and clusters
		Add one core_point to each cluster
		'''
		pass

	def expectation(self, x):
		post = []
		for core in self.cores:
			m, s, g, e = core.mu, core.sigma, core.gamma, core.epsilon
			likelihoods.append(pdf(x=x, mu=m, sigma=s, gamma=g, epsilon=e))
		post = np.array(post)
		if post.shape != (len(self.cores), len(x)):
			raise RuntimeError("Expectation Step found erroneous shape")
		return post

	def maximization(self, post, x):
		for p, c in zip(post, self.cores):
			b = (p * delta) / (np.sum([p * c.delta for i in range(self.n_cores)], axis=0) + 1e-8)
			c.mu = np.sum(b.reshape(len(x), 1) * x, axis=0) / np.sum(b + 1e-8)
			c.sigma = np.dot((b.reshape(len(x), 1) * (x - c.cluster.mu)).T,
										(x - c.cluster.mu)) / np.sum(b + 1e-8)
			c.delta = np.mean(b)

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
			These core points are gaussian models and have the following property:
				mu - centroid point
			A cluster defines the following properties of all core points:
				gamma - falloff point (when the normal distribution begins)
				sigma - variance (sharpness of the falloff)
				epsilon - outer cutoff limit
				delta - peak density (within gamma range) (this is weight in GMM)
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
			The pull to actual data points is always stronger than the pull to any cluster

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

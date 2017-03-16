#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from  tools import logger
import numpy as np
from cluster import *
from sklearn import manifold
from view.plot_utils import *
log=logger.getLogger()


def plot_cluster(cluster):
	'''
	Plot scatter diagram for final points that using multi-dimensional scaling for data

	Args:
		cluster : DensityPeakCluster object
	'''
	log.info("PLOT: cluster result, start multi-dimensional scaling")
	dp = np.zeros((cluster.max_id, cluster.max_id), dtype = np.float32)
	cls = []
	for i in range(1, cluster.max_id):
		for j in range(i + 1, cluster.max_id + 1):
			dp[i - 1, j - 1] = cluster.distances[(i, j)]
			dp[j - 1, i - 1] = cluster.distances[(i, j)]
		cls.append(cluster.cluster[i])
	cls.append(cluster.cluster[cluster.max_id])
	cls = np.array(cls, dtype = np.float32)
	fo = open(r'./tmp.txt', 'w')
	fo.write('\n'.join(map(str, cls)))
	fo.close()
	seed = np.random.RandomState(seed=3)
	mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1,dissimilarity='precomputed')
	dp_mds = mds.fit_transform(dp)
	logger.info("PLOT: end mds, start plot")
	plot_scatter_diagram(1, dp_mds[:, 0], dp_mds[:, 1], title='cluster', style_list = cls)

if __name__ == '__main__':
	"""
	log.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	dpcluster = DensityPeakCluster()
	# dpcluster.local_density(load_paperdata, './example_distances.dat')
	# plot_rho_delta(rho, delta)   #plot to choose the threthold
	rho, delta, nneigh = dpcluster.cluster(load_paperdata, '../data/data_in_paper/example_distances.dat', 20, 0.1)
	logger.info(str(len(dpcluster.ccenter)) + ' center as below')
	for idx, center in dpcluster.ccenter.items():
		logger.info('%d %f %f' %(idx, rho[center], delta[center]))
	plot_cluster(dpcluster)

	"""

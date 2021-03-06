#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tools import logger
import numpy as np
from cluster import *
from sklearn import manifold
from sklearn import __version__ as sklearn_version
from view.plot_utils import *
from cluster.cluster_dpc import *
log = logger.getLogger()


def plot_rho_delta(rho, delta):
    '''
    Plot scatter diagram for rho-delta points

    Args:
            rho   : rho list
            delta : delta list
    '''
    log.info("PLOT: rho-delta plot")
    plot_scatter_diagram(
        0, rho[1:], delta[1:], x_label='rho', y_label='delta', title='rho-delta')


def plot_cluster(cluster):
    '''
    Plot scatter diagram for final points that using multi-dimensional scaling for data

    Args:
            cluster : DensityPeakCluster object
    '''
    log.info("PLOT: cluster result, start multi-dimensional scaling")
    dp = np.zeros((cluster.max_id, cluster.max_id), dtype=np.float32)
    cls = []
    for i in range(1, cluster.max_id):
        for j in range(i + 1, cluster.max_id + 1):
            dp[i - 1, j - 1] = cluster.distances[(i, j)]
            dp[j - 1, i - 1] = cluster.distances[(i, j)]
        cls.append(cluster.cluster[i])
    cls.append(cluster.cluster[cluster.max_id])
    cls = np.array(cls, dtype=np.float32)
    fo = open(r'./tmp.txt', 'w')
    fo.write('\n'.join(map(str, cls)))
    fo.close()
    if (sklearn_version) > "0.14":
        mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1,
                           dissimilarity='precomputed')
    else:
        mds = manifold.MDS(max_iter=200, eps=1e-4, n_init=1)
    dp_mds = mds.fit_transform(dp)
    log.info("PLOT: end mds, start plot")
    print(cls)
    print(dp_mds[:,0])
    print(dp_mds[:,1])
    plot_scatter_diagram(1, dp_mds[:, 0], dp_mds[
                                          :, 1], title='cluster', label=cls)


if __name__ == '__main__':

    dpcluster = DensityPeakCluster()
    # dpcluster.local_density(load_paperdata, './example_distances.dat')
    # plot_rho_delta(rho, delta)   #plot to choose the threthold
    rho, delta, nneigh = dpcluster.cluster(
        load_paperdata, './data/data_in_paper/example_distances.dat', 20, 0.1)
    log.info(str(len(dpcluster.ccenter)) + ' center as below')
    for idx, center in dpcluster.ccenter.items():
        log.info('%d %f %f' % (idx, rho[center], delta[center]))
    plot_cluster(dpcluster)

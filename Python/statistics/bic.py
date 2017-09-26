'''
Module for testing bic (Bayesian Information criterion)
Date:2017/9/20
'''
from sklearn import cluster, datasets
from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt


def compute_bic(kmeans, data):
    """
    Computes the BIC metric for a given clusters

    Parameters:
    -----------------------------------------
    kmeans:  List of clustering object from scikit learn

    data     :  multidimension np array of data points

    Returns:
    -----------------------------------------
    bic value
    """
    # assign centers and labels
    centers = [kmeans.cluster_centers_]
    labels = kmeans.labels_
    # number of clusters
    num_clu = kmeans.n_clusters
    # size of the clusters
    size_clu = np.bincount(labels)
    # size of data set
    data_size, dim = data.shape
    # compute variance for all clusters beforehand
    cl_var = (1.0 / (data_size - num_clu) / dim) * sum(
        [sum(distance.cdist(data[np.where(labels == i)], [centers[0][i]], 'euclidean')**2)
         for i in range(num_clu)])

    const_term = 0.5 * num_clu * np.log(data_size) * (dim + 1)

    bic = np.sum([-(size_clu[i] * np.log(size_clu[i])) +
                  size_clu[i] * np.log(data_size) +
                  ((size_clu[i] * dim) / 2) * np.log(2 * np.pi * cl_var) +
                  ((size_clu[i] - 1) * dim / 2) for i in range(num_clu)]) + const_term

    return bic


def ori_bic(kmeans, data):
    '''
    Method of computing bic using original form
    Input: sklearn.KMeans, np.array
    Output: float (scalar)
    '''
    centers = [kmeans.cluster_centers_]
    labels = kmeans.labels_
    size_clu = np.bincount(labels)
    num_clu = kmeans.n_clusters
    data_size, dim = data.shape
    bic = 0

    for k in range(num_clu):
        sse = sum(distance.cdist(data[np.where(labels == k)], [
                  centers[0][k]], 'euclidean')**2)[0]
        if sse == 0 or size_clu[k] == 0:
            continue
        bic += -size_clu[k] * np.log(sse / size_clu[k]) + \
            (dim + 1) * np.log(size_clu[k])
        print(k, bic)
    return bic


def graph(bic, size_clu):
    '''
    Method to plot the graph of bic result
    Input: bic(array), size_clu(int)
    Output: None
    '''
    plt.plot(size_clu, bic, 'r-o')
    plt.title("iris data  (cluster vs BIC)")
    plt.xlabel("# clusters")
    plt.ylabel("# BIC")
    plt.show()


if __name__ == '__main__':
    # IRIS DATA
    IRIS = datasets.load_iris()
    X = IRIS.data[:, :4]  # extract only the features
    # Xs = StandardScaler().fit_transform(X)
    Y = IRIS.target

    KS = range(1, 40)

    # run 9 times kmeans and save each result in the KMeans object
    KMEANS = [cluster.KMeans(n_clusters=i, init="k-means++").fit(X)
              for i in KS]

    # now run for each cluster the BIC computation
    BIC = [compute_bic(kmeansi, X) for kmeansi in KMEANS]
    #NEW_BIC = [ori_bic(kmeansi, X) for kmeansi in KMEANS]
    print(BIC)
    graph(BIC, KS)

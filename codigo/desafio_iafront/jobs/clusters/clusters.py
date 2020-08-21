import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MiniBatchKMeans, Birch, OPTICS


def kmeans(vector: np.array, n: int):
    k = KMeans(n_clusters=n, random_state=0)
    cluster_coordinate = k.fit_transform(vector)
    cluster_label = k.fit(vector)

    return cluster_coordinate, cluster_label.labels_


def agg_clustering(vector: np.array, n: int):
    k = AgglomerativeClustering(linkage='ward', n_clusters=n)
   
    cluster_label = k.fit(vector)

    return None, cluster_label.labels_

def dbscan(vector: np.array, n: int):
    k = OPTICS(eps=2)
    cluster_label = k.fit(vector)

    return None, cluster_label.labels_
    

def opitcs(vector: np.array, n: int):
    k = Birch()
    cluster_label = k.fit(vector)

    return None, cluster_label.labels_


def minbatchkmeans(vector: np.array, n: int):
    k = MiniBatchKMeans(n_clusters=n, random_state=0)
    cluster_coordinate = k.fit_transform(vector)
    cluster_label = k.fit(vector)

    return cluster_coordinate, cluster_label.labels_
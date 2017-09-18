import numpy as np
# from sklearn.metrics.pairwise import euclidean_distances

D = 2
S = 1000
K = 3
max_iterations = 10

# 1000x2
data = np.random.rand(S, D)

# 3x2
centroids = np.random.rand(K, D)

def euclidean_distances(data, centroids):
    return np.array([np.sum((d - centroids)**2, 1)
        for d in data])

def calc_error(data, centroids, labels):
    total = 0
    for c in range(centroids.shape[0]):
        assigned = data[np.where(labels == c)]
        if assigned.shape[0] > 0:
            total += np.sum(euclidean_distances(assigned, centroids[c].reshape((1, D))))
    return total

# # 1000x3
for iterations in range(max_iterations):
    # result = np.dot(data, centroids.T)
    distances = euclidean_distances(data, centroids)

    # distances is: [SxK], per S_i find min K
    labels = np.argmin(distances, 1)

    print calc_error(data, centroids, labels)
    print centroids

    for c in range(centroids.shape[0]):
        assigned = data[np.where(labels == c)]
        if assigned.shape[0] > 0:
            centroids[c] = np.mean(assigned)

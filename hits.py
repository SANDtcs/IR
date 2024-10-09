import numpy as np
import numpy.linalg as la

def hits(adjMat):
    mat1 = adjMat.dot(adjMat.T)
    mat2 = adjMat.T.dot(adjMat)
    eVals1, eVecs1 = la.eig(mat1)
    eVals2, eVecs2 = la.eig(mat2)
    order1 = np.absolute(eVals1).argsort()[::-1]
    order2 = np.absolute(eVals2).argsort()[::-1]
    eVals1 = eVals1[order1]
    eVals2 = eVals2[order2]
    eVecs1 = eVecs1[:, order1]
    eVecs2 = eVecs2[:, order2]
    auths = eVecs1[:, 0]
    hubs = eVecs2[:, 0]

    return np.real(hubs / np.sum(hubs)), np.real(auths / np.sum(auths))

adjMat = np.array([
    [0, 1, 1, 1],
    [0, 0, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 1]
])
hubs, auths = hits(adjMat)
print("Hub Scores:", hubs)
print("Authority Scores:", auths)


import networkx as nx

G = nx.DiGraph()
for i in range(hits.shape[1]):
    for j in range(hits.shape[0]):
        if hits[j, i] == 1:
            G.add_edge(i, j)
nx.draw(G, with_labels = True)
nx.hits(G, max_iter = 10, normalized = True)

import numpy as np
import numpy.linalg as la

def powerIteration(adjMat, maxIters = 100):
    n = adjMat.shape[0]
    pageRanks = np.ones(n) / n

    for i in range(maxIters):
        newRanks = adjMat.dot(pageRanks)
        if np.allclose(pageRanks, newRanks):
            print("Convergence in step:", i)
            break
        pageRanks = newRanks

    return pageRanks

adjMat = np.array([[0, 1/3, 1/3, 1/3],
                  [1, 0, 1/3, 1/3],
                  [0, 1/3, 0, 1/3],
                  [0, 1/3, 1/3, 0]])
print(powerIteration(adjMat))


def eigenRank(adjMat):
    eVals, eVecs = la.eig(adjMat)
    order = np.absolute(eVals).argsort()[::-1]
    eVals = eVals[order]
    eVecs = eVecs[:, order]
    pageRanks = eVecs[:, 0]
    return np.real(pageRanks / np.sum(pageRanks))

adjMat = np.array([[0, 1/3, 1/3, 1/3],
                  [1, 0, 1/3, 1/3],
                  [0, 1/3, 0, 1/3],
                  [0, 1/3, 1/3, 0]])
print(eigenRank(adjMat))

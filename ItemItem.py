import numpy as np
from tqdm import tqdm

def similarity(data):
    similar = data.T.dot(data)+1e-9
    norms = np.array([np.sqrt(np.diagonal(similar))])
    return similar/norms/norms.T


def SingletopKPredictions(userVector, ratings, similarity, k):
    pred = np.zeros(userVector.shape)
    for i, j in tqdm(enumerate(pred[0])):
        if (userVector[0, i] == 0):
            top_k_users = np.argsort(similarity[i, :])[-k - 1:-1]

            #             print(ratings[i,:][top_k_users].T)
            pred[0, i] = similarity[i, :][top_k_users].dot(userVector[0][top_k_users].T)
            pred[0, i] /= np.mean(np.abs(similarity[i, :][top_k_users]))
    return pred

def giveItemPredictions(ratings, userVector):
    userVector = userVector.reshape(1, -1)
    k = ratings.shape
    ratings = np.append(ratings, userVector, axis=0)
    similarityMatrix = similarity(ratings)
    predictions = SingletopKPredictions(userVector, ratings,similarityMatrix, 40)
    return predictions

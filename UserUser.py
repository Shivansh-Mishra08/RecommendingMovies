import numpy as np
from pymongo import MongoClient
from tqdm import tqdm

def cosSimilarity(ratings, epsilon=1e-9):
    sim = ratings.dot(ratings.T) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)

def cosine_predict_topk(userVector, ratings, similarity, k=40):
    pred = np.zeros(userVector.shape)
    for i, j in tqdm(enumerate(pred[0])):
        if (userVector[0, i] == 0):
            top_k_users = [np.argsort(similarity[-1, :])[-k - 1:-1]]
            pred[0, i] = similarity[-1, :][top_k_users].dot(ratings[:, i][top_k_users])
            pred[0, i] /= np.sum(np.abs(similarity[-1, :][top_k_users]))
    return pred


def giveUserPredictions(ratings,userVector):
    userVector = userVector.reshape(1, -1)

    ratings = np.append(ratings, userVector, axis=0)
    cosine_similarity = cosSimilarity(ratings)
    pred = cosine_predict_topk(userVector, ratings, cosine_similarity)

    # db.permanentRatings.insert_one({
    #     "email": email,
    #     "ratings": list(userVector)
    # })

    return pred

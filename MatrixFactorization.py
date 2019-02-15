import numpy as np


def predict(global_bias, item_bias, user_bias, user_vectors, item_vectors, i, u):
    prediction = global_bias + item_bias[i] + user_bias[u]
    prediction += user_vectors[u, :].dot(item_vectors[i, :].T)
    return prediction


def predictAll(global_bias, item_bias, user_bias, user_vectors, item_vectors):
    predictions = np.zeros((user_vectors.shape[0], item_vectors.shape[0]))
    for u in range(user_vectors.shape[0]):
        for i in range(item_vectors.shape[0]):
            predictions[u, i] = predict(global_bias, item_bias, user_bias, user_vectors, item_vectors, i, u)

    return predictions


def scd(ratings, learning_rate, item_bias_reg, user_bias_reg, item_fact_reg, user_fact_reg, iter_no, n_factors=40):
    number_users, number_items = ratings.shape
    user_vectors = np.random.normal(scale=1. / n_factors, size=(number_users, n_factors))
    item_vectors = np.random.normal(scale=1. / n_factors, size=(number_items, n_factors))
    row, column = np.nonzero(ratings)
    numberOfItems = len(row)
    indexes = np.arange(numberOfItems)
    np.random.shuffle(indexes)
    user_bias = np.zeros(number_users)
    item_bias = np.zeros(number_items)
    global_bias = np.mean(ratings[np.where(ratings != 0)])
    for i in range(iter_no):
        for idx in indexes:
            u = row[idx]
            i = column[idx]
            prediction = predict(global_bias, item_bias, user_bias, user_vectors, item_vectors, i, u)

            e = ratings[u, i] - prediction
            user_bias[u] += learning_rate * (e - user_bias_reg * user_bias[u])
            item_bias[i] += learning_rate * (e - item_bias_reg * item_bias[i])

            user_vectors[u, :] += learning_rate * (e - user_fact_reg * user_vectors[u, :])
            item_vectors[i, :] += learning_rate * (e - item_fact_reg * item_vectors[i, :])

    return global_bias, item_bias, user_bias, user_vectors, item_vectors


def giveMatrixFactorization(ratings, userRating):
    newUserRating = userRating.reshape(1,-1)
    newRatings = np.append(ratings,newUserRating,axis=0)

    global_bias, item_bias, user_bias, user_vectors, item_vectors = scd(newRatings, 0.001, 0.0, 0.0, 0.0, 0.0, 1)
    prediction = predictAll(global_bias, item_bias, user_bias, user_vectors, item_vectors)

    prediction = np.where(np.isnan(prediction), 0, prediction)

    prediction = np.where(np.isinf(prediction), 0, prediction)

    return prediction[-1]


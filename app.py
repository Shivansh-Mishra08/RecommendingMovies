from flask import Flask, render_template, request, redirect, url_for, session
import pickle
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json
import os
import numpy as np
import UserUser, ItemItem, MatrixFactorization
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.secret_key = "1234"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['MONGO_DBNAME'] = "Movie_User_db"
app.config['MONGO_URI'] = "mongodb://localhost:27017/Movie_User_db"
mongo = PyMongo(app)
client = MongoClient('localhost:27017')
db = client.Movie_User_db

@app.route('/likedMovies')
def likedMovies():
    likedUsers1 = db.liked
    moviesC = db.movies
    a = request.cookies
    imagesDictionary = {}
    user = likedUsers1.find_one({"email": a['email']})
    if user is not None:
        movieLocation = user["liked"]
        movieLocation = [f'{i}.jpg' for i in movieLocation]

        for i in movieLocation:
            t = i
            a = moviesC.find_one({"location": i})
            imagesDictionary[i] = a["name"]

    else:
        return "you haven't rated movies yet :("
    synopsis = db.synopsis

    return render_template("likedMovies.html", images=imagesDictionary, synopsis=synopsis)

@app.route('/')
def signIn():
    return render_template("signIn.html")

@app.route('/Movies')
def movies():
    # with open("dictionary_name.pickle", "rb") as f:
    #     images = pickle.load(f)
    #
    # imagesToSend0 = {k: images[k] for k in list(images)[:100]}
    # imagesToSend1 = {k: images[k] for k in list(images)[-100:]}
    # imagesToSend2 = {k: images[k] for k in list(images)[4871:4971]}
    Fantasy = {}
    Romance = {}
    Animation = {}
    Mystery = {}
    Horror = {}
    Thriller = {}
    Comedy = {}
    Film_Noir = {}
    Crime = {}
    Western = {}
    Sci_Fi = {}
    Children = {}
    War = {}
    Musical = {}
    Action = {}
    Documentary = {}
    Drama = {}
    Adventure = {}



    for document in db.movies.find():
        # imagesToSend[document["location"]] = document["name"]
        if document["genre"] == "Fantasy":
            Fantasy[document["location"]] = document["name"]

        if document["genre"] == "Romance":
            Romance[document["location"]] = document["name"]

        if document["genre"] == "Animation":
            Animation[document["location"]] = document["name"]

        if document["genre"] == "Horror":
            Horror[document["location"]] = document["name"]

        if document["genre"] == "Thriller":
            Thriller[document["location"]] = document["name"]

        if document["genre"] == "Comedy":
            Comedy[document["location"]] = document["name"]

        if document["genre"] == "Film-Noir":
            Film_Noir[document["location"]] = document["name"]

        if document["genre"] == "Crime":
            Crime[document["location"]] = document["name"]

        if document["genre"] == "Western":
            Western[document["location"]] = document["name"]

        if document["genre"] == "Sci-Fi":
            Sci_Fi[document["location"]] = document["name"]

        if document["genre"] == "Children":
            Children[document["location"]] = document["name"]

        if document["genre"] == "War":
            War[document["location"]] = document["name"]

        if document["genre"] == "Musical":
            Musical[document["location"]] = document["name"]

        if document["genre"] == "Action":
            Action[document["location"]] = document["name"]

        if document["genre"] == "Documentary":
            Documentary[document["location"]] = document["name"]

        if document["genre"] == "Drama":
            Drama[document["location"]] = document["name"]

        if document["genre"] == "Adventure":
            Adventure[document["location"]] = document["name"]

        if document["genre"] == "Mystery":
            Mystery[document["location"]] = document["name"]

    synopsis = db.synopsis



    # arr = [imagesToSend0, imagesToSend1, imagesToSend2]
    # for i in arr:
    #     for j in list(i):
    #         imagesToSend[j] = i[j]
    #images = os.listdir("static/images")

    return render_template("BulmaTesting.html", Fantasy=Fantasy, Romance=Romance, Animation=Animation, Mystery=Mystery, Horror=Horror, Thriller=Thriller, Comedy=Comedy, Film_Noir=Film_Noir, Crime=Crime, Western=Western, Sci_Fi=Sci_Fi, Children=Children, War=War, Musical=Musical, Action=Action, Documentary=Documentary, Drama=Drama, Adventure=Adventure, synopsis=synopsis)

@app.route('/signInForm', methods=['POST'])
def checkSignIn():
    email = request.form['email']
    password = request.form['password']
    post = {'email': email, 'password': password}
    user = mongo.db.users
    check = user.find_one({'email': email})
    if check is None:
        return "user does not exist"
    elif sha256_crypt.verify(password, check["password"]):
        session["logIn"] = True
        return redirect(url_for('movies'))
    return "password incorrect"



@app.route('/signUp')
def signUp():
    return render_template("SignUp.html")



@app.route('/signUpForm', methods=['POST'])
def checkSignUp():
    email = request.form['email']
    password = sha256_crypt.encrypt(str(request.form['password']))
    post = {'email': email, 'password': password}
    user = mongo.db.users
    find = user.find_one({'email': email})
    if find is not None:
        return "sorry user name already exists :("
    session["logIn"] = True
    user.insert(post)
    return redirect(url_for('movies'))


@app.route("/pred")
def dataGot():
    json1 = request.args.get("js")

    # matrixT = matrix.split("\\")
    # matrixJ = ",".join(matrixT)
    # json1 = json.loads(json1)

    data = json.loads(json1)
    newData = {}

    for i, j in data.items():
        newData[int(i)] = int(j)

    userVector = np.zeros(9742)

    for key in newData.keys():
        t = db.movies.find_one({"location": "{}.jpg".format(key)})
        checkT = t["index"]
        userVector[t["index"] - 1] = newData[key]

    checkUserVector = userVector.nonzero()

    ratings = []

    for document in db.permanentRatings.find():
        ratings.append(document["ratings"])

    ratings = np.array(ratings)
    # userVector = userVector.reshape(1,-1)

    predictionItemItem = ItemItem.giveItemPredictions(ratings, userVector)
    predictionUserUser = UserUser.giveUserPredictions(ratings, userVector)
    predictionMatrix = MatrixFactorization.giveMatrixFactorization(ratings, userVector)
    predictionMatrix = predictionMatrix.reshape(1, -1)

    ItemItemSort = np.argsort(predictionItemItem)
    ItemItemDict = {}

    counterItem = 0
    movies = db.movies
    for i in (ItemItemSort[0])[::-1]:
        checkValueI = i
        result = movies.find_one({"index": int(i + 1)})
        k = result
        if result is not None:
            print("result item item not none")
            if userVector[i] == 0:
                counterItem += 1
                ItemItemDict[result["location"]] = result["name"]
            if counterItem >= 10:
                break

    UserUserSort = np.argsort(predictionUserUser)
    UserUserDict = {}

    counterUser = 0

    for i in (UserUserSort[0])[::-1]:

        result = movies.find_one({"index": int(i + 1)})
        if result is not None:
            print("result user user not none")
            if userVector[i] == 0:
                counterUser += 1
                UserUserDict[result["location"]] = result["name"]
            if counterUser >= 10:
                break

    MatrixSort = np.argsort(predictionMatrix)
    print("hi i am going to print the matrixSort")
    print()
    print(MatrixSort)
    print(type(MatrixSort))
    print(MatrixSort.shape)
    print()
    print()

    MatrixDict = {}
    counterMatrix = 0
    for i in (MatrixSort[0])[::-1]:
        result = movies.find_one({"index": int(i + 1)})

        if result is not None:
            print("result matrix is not none")
            if userVector[i] == 0:
                counterMatrix += 1
                MatrixDict[result["location"]] = result["name"]
            if counterMatrix >= 10:
                break

    print("hi i am going to print the predictions")
    print()
    print(len(list(MatrixDict.keys())), len(list(UserUserDict.keys())), len(list(ItemItemDict.keys())))
    print(MatrixDict)
    print(UserUserDict)
    print(ItemItemDict)
    print()
    print()
    print()

    a = request.cookies
    email = a['email']

    permanentRatings1 = db.permanentRatings.find_one({"email": str(email)})
    if permanentRatings1 is None:
        db.permanentRatings.insert_one({
            "email": str(email),
            "ratings": list((userVector.reshape(1, -1))[0])
        })
    else:

        arrPermanentRatings = permanentRatings1["ratings"]

        for i, j in enumerate(list((userVector.reshape(1, -1))[0])):
            if arrPermanentRatings[i] == 0:
                arrPermanentRatings[i] = j
        checkt = (np.array(arrPermanentRatings).nonzero()[0]).shape
        db.permanentRatings.remove({"email": email})
        db.permanentRatings.insert_one({"email": email, "ratings": list(arrPermanentRatings)})

        retrievet1 = db.permanentRatings.find_one({"email": str(email)})
        checktt = retrievet1["ratings"]
        checkt1 = (np.array(checktt).nonzero()[0]).shape

    like = db.liked.find_one({"email": email})
    if like is None:
        db.liked.insert_one({
            "email": email,
            "liked": list(data)
        })
    else:
        arr = like["liked"]
        # previous = len(arr)
        for i in list(data):
            if i not in arr:
                arr.append(i)
        # after = len(arr)
        db.liked.remove({
            "email": email})

        db.liked.insert_one({"email": email, "liked": arr})
        # fromdb = db.liked.find_one({"email": email})
        # checkliking = len(fromdb["liked"])

    synopsis = db.synopsis

    return render_template("predictions.html", matrix=MatrixDict, user=UserUserDict, item=ItemItemDict, synopsis=synopsis)


@app.route("/signOut")
def signingOut():
    session.clear()
    return redirect(url_for('signIn'))

@app.route("/getmethod", methods=['GET', 'POST'])
def get_data():
        try:
            b = request.cookies
            json1 = b["liked"]
            if(len(json1) >= 10):
                return redirect(url_for('dataGot', js=json1))
        except:
            return redirect(url_for("movies"))











if __name__ == '__main__':
    app.run(debug=True)

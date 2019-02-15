# Movie Recommendation Web Application

## How To Use The Web Application
can be accessed atf [139.59.1.152](http://139.59.1.152)

When you first visit the webapp you will be welcomed with the login page where you can also select to signup if you do not have an account already. The homepage is next presents you with the movies where you can rate them according to your preference, you can also select the movies according to the genre from the tab bar given below the nav bar in the website ,you need to star the movies between 1-5. The user is required to rate **atleast 10** movies. After pressing the **Done** button the recommendations will be generated according to your rating, these recommendations are generated with the help of 3 different algorithms namely **User-User Collaborative Filtering, Item-Item collaborative filtering, Matrix Factorization**, *(note that this will take some time since the existin database is large so that we can give better predictions)* once the processing is done you can also choose the recommendations from the different algorithms by pressing the tab bar present in the website.
You can even see the movies that you have liked previously by pressing the **Movies You Liked** button on the navbar.

![Page After Login](https://github.com/Shivansh-Mishra08/RecommendingMovies/blob/master/moviePage.png)
![Page After Liking the Movies](https://github.com/Shivansh-Mishra08/RecommendingMovies/blob/master/likedMovies.png)

## Approach Followed

1. In general Item-Item collaborative filtering worked better than the User-User collaborative filtering, irrespective of the similarity function used. This is possibly because Item-Item Collaborative filtering is more resistant to user bias than User-User Collaborative filtering. It was also observed that the plain, cosine similarity tends to work better than pearson correlation, for sparse matrices. I also tried to use centered cosine but it tends to fail in the case when user gives same rating to all the movies. The value of nearest neighbors was chosen 40 because at that value the mse loss was minimized.

2.Matrix factorization outperforms both User-User and Item-Item collaborative filtering methods.Using appropriate random initialization, a single iteration of stochastic gradient descent was able to give the best results. K=40 was chosen for latent features for the embeddings. When a new user comes, the algorithm is trained for a single iteration, and the user and item embeddings are multiplied to get the predictions.

## Codebbase and Directory Structure

### Jupyter Notebooks
* **userAndItemCollaborativeFiltering.ipynb** - This notebook was used to explore the User-User and Item-Item Collaborative filtering. The root mean squared error was used to test the model and was also used in the decision to pick the best value of the nearest neighbours.

* **matrix.ipynb** - This notebook was used to explore the matrix factorization method. This notebook contains pure numpy vectorized code for faster results. The root mean squared error was used to test the model and was also used in the decision to pick the best value of the latent features for the embeddings.

* **ScrapeTheSynopsis.ipynb** - This notebook was used to scrape the synopsis as well as the duration of the movie from the IMDb website. This notebook was also used to store these values in MONGODB-DATABASE.

* **scrapingTheUrl.ipynb** - This notebook contains the code to extract the url of the thumbnail images, The code is threaded so that the results come out faster.

* **DownloadingImages.ipynb** - This notebook contains the code to download all the thumbnail images from the IMDb website from the links provided by the scrapingTheUrl.ipynb file.

### Web Application

* **dump floder** - Consists of mongodb database dump, with 5 collections in total. Namely - liked, movies, permanentRatings, synopsis, users.

* **Static folder** - Consists of the images folder.

* **Templates folder** - 
1. BulmaTesting - This is the the html file which shows the movies which users have to Rate.
2. likedMovies - This is the html file which shows the movies liked by the user that has signed In.
3. predictions - This is the html file which shows the predicted movies to the user.
4. signIn - This is the html file which shows the Sign In page.
5. signUp - This is the html file which shows the Sign Up page.

* **app.py** - Uses flask framework as the backend for the webapp.

* **UserUser.py** - This file provides the useruser_predict function to the main app.py module.

* **ItemItem.py** - This file provides the itemitem_predict function to the main app.py module.

* **MatrixFactorization.py** - This file provides the matrixFactorization_predict function to the main app.py module.

### Data Set
* **ml-latest-small** - MovieLens development dataset,  small in size.
* **moviesWithIndex.csv** - This consists of movies with indexes assigned to it.

## Dependencies Used
1. Flask - for backend
2. Jinja2 - for HTML templating
3. passlib - for hashing user password
4. numpy - for fast numerical computation
5. Sklearn - for loss metrics
6. Pandas - for manipulation of CSV'S
7. Pymongo - for communicating with mongodb
8. Flask-PyMongo - for communicating with mongodb
9. tqdm - for monitoring the time taken by the algorithms.

## Citations
 1. C.C. Aggarwal, Recommender Systems: The Textbook, DOI 10.1007/978-3-319-29659-3 2 - Used this book to understand User-User collaborative filtering.
 2. https://www.ethanrosenthal.com/2016/01/09/explicit-matrix-factorization-sgd-als/ - Used this blog to Understand the Matrix Factorization method.



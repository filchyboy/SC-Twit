
from flask import Blueprint, request, jsonify, render_template

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from web_app.models import User, Tweet
from web_app.basilica_service import connection as basilica_api_client

stats_routes = Blueprint("stats_routes", __name__)

#breakpoint()
@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'elonmusk', 'screen_name_b': 'chrisalbon', 'tweet_text': 'Example tweet text here'}
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("FETCHING TWEETS FROM THE DATABASE...")
    # todo: wrap in a try block in case the user's don't exist in the database
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    #user_a_embeddings = [tweet.embedding for tweet in user_a_tweets]
    #user_b_embeddings = [tweet.embedding for tweet in user_b_tweets]

    print("TRAINING THE MODEL...")
    embeddings = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    classifier = LogisticRegression()
    classifier.fit(embeddings, labels)

    print("MAKING A PREDICTION...")
    #result_a = classifier.predict([user_a_tweets[0].embedding])
    #result_b = classifier.predict([user_b_tweets[0].embedding])

    example_embedding = basilica_api_client.embed_sentence(tweet_text)
    result = classifier.predict([example_embedding])
  

    #return jsonify({"message": "RESULTS", "most_likely": result[0]})
    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely= result[0]
    )

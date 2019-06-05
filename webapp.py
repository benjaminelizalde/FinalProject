from flask import Flask, redirect, url_for, session, request, jsonify, Markup
from flask_oauthlib.client import OAuth
from flask import render_template
from time import localtime, strftime
from bson.objectid import ObjectId

import pprint
import os
import json
import pymongo
import dns
import sys

app = Flask(__name__)


url = 'mongodb+srv://{}:{}@{}/{}'.format(
    os.environ["MONGO_USERNAME"],
    os.environ["MONGO_PASSWORD"],
    os.environ["MONGO_HOST"],
    os.environ["MONGO_DBNAME"]
)
client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client[os.environ["MONGO_DBNAME"]]
collection = db['cookieStats']

app.debug = True #Change this to False for production
app.secret_key = os.environ['SECRET_KEY'] #used to sign session cookies
oauth = OAuth(app)



github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'], #your web app's "username" for github's OAuth
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],#your web app's "password" for github's OAuth
    request_token_params={'scope': 'user:email'}, #request read-only access to the user's email.  For a list of possible scopes, see developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize' #URL for github's OAuth login
)

@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}



@app.route("/")
def render_main():

    if 'user_data' in session:
        if collection.find_one({"Github Name": session['user_data']['login']}) is not None:
            docs=collection.find_one({"Github Name": session['user_data']['login']})
            pprint.pprint(docs)
            return render_template('game.html', cookies=docs["cookies"], cookiesPerClick=docs["cookiesPerClick"], cookiesPerSecond=docs["cookiesPerSecond"], cursorsOwned=docs["cursorsOwned"], grandmasOwned=docs["grandmasOwned"], costOfCursors=docs["costOfCursors"], costOfGrandmas=docs["costOfGrandmas"],lifetimeClicks = docs["lifetimeClicks"],lifetimeCookies = docs["lifetimeCookies"])
            print(collection.count_documents({}))
    return render_template('game.html', cookies=0, cookiesPerClick=1, cookiesPerSecond=0,  cursorsOwned = 0, costOfCursors = 10, grandmasOwned = 0, costOfGrandmas = 20, lifetimeClicks = 0, lifetimeCookies = 0)

@app.route("/stats")
def render_stats():
    if 'user_data' in session:
        if collection.find_one({"Github Name": session['user_data']['login']}) is not None:
            docs=collection.find_one({"Github Name": session['user_data']['login']})
            return render_template('game.html', cookies=docs["cookies"], cookiesPerClick=docs["cookiesPerClick"], cookiesPerSecond=docs["cookiesPerSecond"], cursorsOwned=docs["cursorsOwned"], grandmasOwned=docs["grandmasOwned"], costOfCursors=docs["costOfCursors"], costOfGrandmas=docs["costOfGrandmas"],lifetimeClicks = docs["lifetimeClicks"],lifetimeCookies = docs["lifetimeCookies"])

    return render_template('stats.html', cookies=0, cookiesPerClick=1, cookiesPerSecond=0,  cursorsOwned = 0, costOfCursors = 10, grandmasOwned = 0, costOfGrandmas = 20, lifetimeClicks = 0, lifetimeCookies = 0)




@app.route("/save", methods=["POST"])
def render_save():

    pprint.pprint(request.form)
    post = {"Github Name": session['user_data']['login'] ,  "cookies": request.form['cookies'] , "cookiesPerClick": request.form['cookiesPerClick'], "cookiesPerSecond": request.form['cookiesPerSecond'], "cursorsOwned": request.form['cursorsOwned'], "grandmasOwned": request.form['grandmasOwned'], "costOfGrandmas": request.form['costOfGrandmas'], "costOfCursors": request.form['costOfCursors'], "lifetimeClicks": request.form['lifetimeClicks'],
     "lifetimeCookies": request.form['lifetimeCookies'] }
    pprint.pprint(post)
    if collection.find_one({"Github Name": session['user_data']['login']}) is not None:
        print("here")
        print(request.form)
        collection.update_one({"Github Name": session['user_data']['login']}, {'$set':{'cookies' : request.form['cookies'], 'cookiesPerClick' : request.form['cookiesPerClick'] ,'cookiesPerSecond' : request.form['cookiesPerSecond'], "cursorsOwned": request.form['cursorsOwned'], "grandmasOwned": request.form['grandmasOwned'], "costOfGrandmas": request.form['costOfGrandmas'], "costOfCursors": request.form['costOfCursors'], "lifetimeClicks": request.form['lifetimeClicks'],
         "lifetimeCookies": request.form['lifetimeCookies']}})
    else:
        collection.insert_one(post)

    return redirect("/game")



@app.route('/login')
def login():

    return github.authorize(callback=url_for('authorized', _external=True, _scheme='https')) #callback URL must match the pre-configured callback URL


@app.route('/logout')
def logout():
    session.clear()
    return render_template('game.html', message='You were logged out',cookies=0, cookiesPerClick=1, cookiesPerSecond=0,  cursorsOwned = 0, costOfCursors = 10, grandmasOwned = 0, costOfGrandmas = 20, lifetimeClicks = 0, lifetimeCookies = 0)

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    print("here")
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + ' error=' + request.args['error_description'] + ' full=' + pprint.pformat(request.args)
        print("here1")
    else:
        print("here2")
        try:
            print("here3")
            session['github_token'] = (resp['access_token'], '') #save the token to prove that the user logged in
            print("here3.25")
            session['user_data']=github.get('user').data
            print("here3.5")
            message='You were successfully logged in as ' + session['user_data']['login']
            if collection.find_one({"Github Name": session['user_data']['login']}) is not None:
                print("here4")
                docs=collection.find_one({"Github Name": session['user_data']['login']})
                pprint.pprint(docs)
                print("here4.5")
                return render_template('game.html', cookies=docs["cookies"], cookiesPerClick=docs["cookiesPerClick"], cookiesPerSecond=docs["cookiesPerSecond"], cursorsOwned=docs["cursorsOwned"], grandmasOwned=docs["grandmasOwned"], costOfCursors=docs["costOfCursors"], costOfGrandmas=docs["costOfGrandmas"],lifetimeClicks = docs["lifetimeClicks"],lifetimeCookies = docs["lifetimeCookies"])

        except Exception as inst:
            print("here5")
            session.clear()
            print(inst)
            message='Unable to login, please try again.'


    return render_template('game.html',cookies=0, cookiesPerClick=1, cookiesPerSecond=0,  cursorsOwned = 0, costOfCursors = 10, grandmasOwned = 0, costOfGrandmas = 20 , lifetimeClicks = 0, lifetimeCookies = 0)

#the tokengetter is automatically called to check who is logged in.
@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


if __name__ == '__main__':
    os.system("echo json(array) > file")
    app.run()

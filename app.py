from flask import Flask, render_template, request, flash, render_template_string, redirect, Response, make_response
import psycopg2
import json
import random
import string
import requests
import os
from pml import app



port = int(os.getenv('PORT'))




app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    data = {
        '/lonig': 'вход (/login?login=user1&password=123',
        '/register': 'регистрация (register?login=user1&password=123&nickname=nicknnname)',
        '/logout': 'выход (/logout)',
        '/books': 'список всех книг (/books)',
        '/show': 'показать рецензии по id книги (/show/3)',
        '/write': 'написать рецензию text по id книги, поставить оценку mark  (/write/3?mark=4&text=четкая книга)',
        '/delete': 'удалить рецензию по id рецензии (/delete/3)'
    }
    return data, 200


@app.route("/login", methods=["POST", "GET"])
def lonig():

    login = request.args.get('login')
    password = request.args.get('password')

    try:
        req = requests.get(f'http://localhost:5003/login?login={login}&password={password}', cookies=request.cookies)
    except:
        return {'main': 'auth service is not available'}, 504

    if req.status_code == 200:
        data = json.loads(req.text)

        ans = make_response({'auth': 'success'})
        ans.set_cookie('token', data['cookie']['token'])
        ans.set_cookie('username', data['cookie']['username'])
        return ans, 200

    else:
        return req.text, req.status_code





@app.route("/logout", methods=["POST", "GET"])
def logout():
    try:
        req = requests.get(f'http://localhost:5003/logout', cookies=request.cookies)
    except:
        return {'main': 'auth service is not available'}, 504

    ans = make_response(req.text)
    ans.set_cookie('token', '', expires=0)
    ans.set_cookie('username', '', expires=0)
    return ans, req.status_code





@app.route("/register", methods=["POST", "GET"])
def register():

    login = request.args.get('login')
    password = request.args.get('password')
    nickname = request.args.get('nickname')

    try:
        req = requests.get(f'http://localhost:5003/register?login={login}&password={password}&nickname={nickname}')
    except:
        return {'main': 'auth service is not available'}, 504

    return req.text, req.status_code









@app.route("/show/<id>", methods=["POST", "GET"])
def showReviews(id):
    try:
        req = requests.get(f'http://localhost:5002/getReview/{id}')
    except:
        return {'main': 'reviews service is not available'}, 504

    return req.text, req.status_code



@app.route("/write/<id>", methods=["POST", "GET"])
def writeReview(id):
    mark = request.args.get('mark')
    text = request.args.get('text')
    token = request.cookies.get('token')
    data = {
        'text': text,
        'token': token,
        'mark': mark
    }

    try:
        req = requests.post(f'http://localhost:5002/saveReview/{id}', json=data)
    except:
        return {'main': 'reviews service is not available'}, 504

    return req.text, req.status_code




@app.route("/delete/<id>", methods=["POST", "GET"])
def deleteReview(id):

    token = request.cookies.get('token')
    data = {
        'token': token,
    }

    try:
        req = requests.post(f'http://localhost:5002/deleteReview/{id}', json=data)
    except:
        return {'main': 'reviews service is not available'}, 504

    return req.text, req.status_code








@app.route("/books", methods=["POST", "GET"])
def showBookList():

    try:
        req = requests.get(f'http://localhost:5001/getBookList')
    except:
        return {'main': 'library service is not available'}, 504

    return req.text, req.status_code


#33507 5004
app.run(threaded=True, port=5000)
#app.run()
#app.run(threaded=True)
#app.run(debug=True, host='books-main-app.herokuapp.com')

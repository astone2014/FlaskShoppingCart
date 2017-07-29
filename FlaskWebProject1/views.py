import json
from datetime import datetime
import FlaskWebProject1.sqlserver
from flask import render_template, make_response, request, redirect, url_for
from FlaskWebProject1 import app
from FlaskWebProject1.sqlserver import sqlclass
import random

sql = sqlclass()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	messages = ""
	if request.method == 'POST':
		username = request.form['user']
		password = request.form['pass']
		user = sql.loginUser(username)
		print(user)
		if not user:
			return redirect(url_for('login', message="Incorrect Username"))
		else:
			id = str(user['id'])
			uname = user['username']
			if password == user['password']:
				response = make_response(redirect(url_for('home', 
											  user=uname.title(),  
											  products=sql.getStore(), 
											  cart=sql.getCart(id))))
				response.set_cookie('userID', id)
				return response
			else:
				messages = "Incorrect Password"
	else:
		try:
			messages = request.args['message']
		except:
			None
	return render_template('login.html', message=messages)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = request.form['user']
		password = request.form['pass']
		user = sql.createUser(username, password)
		print(user)
		if not user:
			return redirect(url_for('signup', message="Username already taken!"))
		else:
			id = str(user['id'])
			uname = user['username']
			dic = sql.getStore()
			response = make_response(redirect(url_for('home', 
											user=uname.title(),  
											products=sql.getStore(), 
											cart=sql.getCart(request.cookies.get('userID')))))
			response.set_cookie('userID', id)
			return response
	else:
		try:
			messages = request.args['message']
		except:
			messages = ""
		return render_template('signup.html', message=messages)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	userID = request.cookies.get('userID')
	return render_template(
			'cart.html',
			products = sql.getCart(userID),
	)
@app.route('/cart', methods=['GET', 'POST'])
def cart():
	if request.method == 'POST':
		product = sql.addCart(request.cookies.get('userID'), request.json['product'])
		return "added %s - $%s" % (product['name'], product['price'])

@app.route('/addCart', methods=['GET', 'POST'])
def addCart():
	if request.method == 'POST':
		product = sql.addCart(request.cookies.get('userID'), request.json['product'])
		return json.dumps(sql.getCart(request.cookies.get('userID')))

@app.route('/removeCart', methods=['GET', 'POST'])
def removeCart():
	if request.method == 'POST':
		product = sql.removeCart(request.cookies.get('userID'), request.json['product'])
		return json.dumps(sql.getCart(request.cookies.get('userID')))

@app.route('/home')
def home():
	dic = sql.getStore()
	return render_template(
		'index.html',
		title='Home Page',
		user=sql.getUser(request.cookies.get('userID'))['username'].title(),
		products=dic,
		cart=sql.getCart(request.cookies.get('userID')),
	)
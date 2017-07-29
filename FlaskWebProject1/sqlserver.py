import MySQLdb

class sqlclass():
	def __init__(self):
		self.name = ""

	# USERS
	def loginUser(self, username):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT username, password, id FROM users WHERE username = '%s'" % username)
		data = cursor.fetchone()
		db.close()
		return data

	def getUser(self, id):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT username, password, id FROM users WHERE id = '%s'" % id)
		data = cursor.fetchone()
		db.close()
		return data

	def createUser(self, username, password):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		data = self.getUser(username)
		if data is None:
			print("DATA IS NONE: ", data)
			try:
				cursor.execute("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password))
				db.commit()
				data = self.getUser(username)
			except:
				db.rollback()
		else:
			print("DATA IS: ", data)
			data = None

		db.close()
		return data

	# STORE
	def getStore(self):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM shopping_cart")
		data = cursor.fetchall()
		db.close()
		return data

	def getProductInfo(self, product):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM shopping_cart WHERE name = '%s'" % product)
		data = cursor.fetchone()
		db.close()
		return data
	
	#CART
	def getCart(self, id):
		cart = "cart"
		username = self.getUser(id)['username']
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""CREATE TABLE IF NOT EXISTS `%s_Cart` ( 
						  `id_product` int(11) NOT NULL AUTO_INCREMENT, 
						  `quantity` int(11) NOT NULL, 
						  `name` varchar(100) NOT NULL, 
						  `image` varchar(256) NOT NULL, 
						  `description` varchar(250) NOT NULL, 
						  `price` float(6) NOT NULL, 
						  PRIMARY KEY (`id_product`) 
						);""" % (username)
		)
		db.commit()

		cursor.execute("SELECT * FROM %s_Cart" % (username))
		cart = cursor.fetchall()

		db.close()
		return cart

	def getCartItem(self, id, product):
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM %s_Cart WHERE name = '%s'" % (self.getUser(id)['username'], product))
		data = cursor.fetchone()
		db.close()
		return data

	def addCart(self, id, product):
		productInfo = self.getProductInfo(product)
		print(productInfo)
		username = self.getUser(id)['username']
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute("SELECT * FROM %s_Cart WHERE name = '%s'" % (username, product))
		cart = cursor.fetchone()
		if cart is None:
			cursor.execute("INSERT INTO %s_Cart (name, price, image, quantity) VALUES ('%s', '%s', '%s', '1')" % (username, productInfo['name'], productInfo['price'], productInfo['image']))
			db.commit()
		else:
			cursor.execute("UPDATE %s_Cart SET `quantity`='%d' WHERE `name`='%s'" % (username, cart['quantity'] + 1, productInfo['name']))
			db.commit()
		db.close()
		return productInfo

	def removeCart(self, id, product):
		cart = "cart"
		username = self.getUser(id)['username']
		db = MySQLdb.connect("149.56.101.13", "miltonlaxer", "1102star", "store")
		cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("DELETE FROM %s_Cart WHERE name = '%s'" % (username, product))
		db.commit()
		db.close()
		return cart
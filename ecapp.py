from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_restful import Resource
#from flask_bootstrap import Bootstrap
import MySQLdb
from MySQLdb import escape_string as thwart
#from flaskext.mysql import MySQL
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import sys
import gc
import re
from copy import deepcopy
from operator import itemgetter



reload(sys)
sys.setdefaultencoding('ISO-8859-1')

app = Flask(__name__)
app.secret_key = 'some_secret'

#MySQL configurations
mysql = MySQLdb
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'HiGroup6!'
#app.config['MYSQL_DATABASE_DB'] = 'Easycook'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app) 


@app.route("/")
def index():
	return render_template('index.html')

@app.route("/about")
def about():
        return render_template('about.html')


@app.route("/search/")		#in search page, it will shows like search/?keyword=apple, two function have same functionality
def search_recipe():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	keyword = request.values.get('keyword')
	keyword_list = keyword.split(" ")
	search_key = request.values.get('searchkey')
	sort_key = request.values.get('sortkey')

	total_dict = {} #a dictionary
	total_list = []
	if search_key == 'Ingredient':
		if len(keyword_list) == 1:
			keyword = keyword_list[0]
			cursor.execute("SELECT id_R, Name_R, rating FROM Recipe WHERE categories LIKE '%s'"%('%'+ keyword + '%'))
			data = cursor.fetchall()

			for i in data:
				if i[0] not in total_dict:
					r_dict = {
					'RecipeID':i[0],
					'RecipeName':i[1],
					'Rating':i[2]
					}
					total_dict[i[0]] = r_dict

			for key,value in total_dict.iteritems():
				total_list.append(value)
			if sort_key == "Name":
				total_list = sorted(total_list, key=itemgetter('RecipeName'))
			else:
				total_list = sorted(total_list, key=itemgetter('Rating'), reverse=True) 
			
			return render_template('search_recipe.html', data = total_list, key = search_key, keylist = keyword_list, sortkey = sort_key)

		if len(keyword_list) > 1:
			keyword = keyword_list[0]
			cursor.execute("SELECT r.id_R, r.Name_R, r.rating, r.categories FROM Recipe r WHERE r.categories LIKE '%s' ORDER BY r.Name_R"%('%'+ keyword + '%'))
			data = cursor.fetchall()

			for i in data:
				if i[0] not in total_dict:
					r_dict = {
					'RecipeID':i[0],
					'RecipeName':i[1],
					'Rating':i[2],
					'Categories':i[3]
					}
					total_dict[i[0]] = r_dict
					#print(r_dict['Categories'])

			temp_dict_1 = total_dict
			temp_dict_2 = {}
			for t in range(1,len(keyword_list)):
				keyword = keyword_list[t]

				for key,value in temp_dict_1.iteritems():
					#print(value['RecipeName'])
					if keyword.lower() in value['Categories'].lower():
						temp_dict_2[key] = value

				temp_dict_1 = {}
				temp_dict_1 = deepcopy(temp_dict_2)
				temp_dict_2 = {}

			for key,value in temp_dict_1.iteritems():
				total_list.append(value)

			if sort_key == "Name":
				total_list = sorted(total_list, key=itemgetter('RecipeName'))
			else:
				total_list = sorted(total_list, key=itemgetter('Rating'), reverse=True) 

			return render_template('search_recipe.html', data = total_list, key = search_key, keylist = keyword_list, sortkey = sort_key)
	else:
		if len(keyword_list) == 1:
			keyword = keyword_list[0]
			cursor.execute("SELECT r.id_R, r.Name_R, r.rating FROM Recipe r WHERE r.name_R LIKE '%s' ORDER BY r.Name_R"%('%'+ keyword + '%',))
			data = cursor.fetchall()

			for i in data:
				#print i
				if i[0] not in total_dict:
					r_dict = {
					'RecipeID':i[0],
					'RecipeName':i[1],
					'Rating':i[2]
					}
					total_dict[i[0]] = r_dict
			for key,value in total_dict.iteritems():
				total_list.append(value)

			if sort_key == "Name":
				total_list = sorted(total_list, key=itemgetter('RecipeName'))
			else:
				total_list = sorted(total_list, key=itemgetter('Rating'), reverse=True) 

			return render_template('search_recipe.html', data = total_list, key = search_key, keylist = keyword_list, sortkey = sort_key)

		if len(keyword_list) > 1:
			keyword = keyword_list[0]
			cursor.execute("SELECT r.id_R, r.Name_R, r.rating FROM Recipe r WHERE r.name_R LIKE '%s' ORDER BY r.Name_R"%('%'+ keyword + '%',))
			data = cursor.fetchall()

			for i in data:
				if i[0] not in total_dict:
					r_dict = {
					'RecipeID':i[0],
					'RecipeName':i[1],
					'Rating':i[2]
					}
					total_dict[i[0]] = r_dict

			temp_dict_1 = total_dict

			temp_dict_2 = {}
			for t in range(1,len(keyword_list)):
				keyword = keyword_list[t]

				for key,value in temp_dict_1.iteritems():
					#print(value['RecipeName'])
					if keyword.lower() in value['RecipeName'].lower():
						temp_dict_2[key] = value

				temp_dict_1 = {}
				temp_dict_1 = deepcopy(temp_dict_2)
				temp_dict_2 = {}

			for key,value in temp_dict_1.iteritems():
				total_list.append(value)

			if sort_key == "Name":
				total_list = sorted(total_list, key=itemgetter('RecipeName'))
			else:
				total_list = sorted(total_list, key=itemgetter('Rating'), reverse=True) 

		return render_template('search_recipe.html', data = total_list, key = search_key, keylist = keyword_list, sortkey = sort_key)



@app.route("/search/<string:kw>")	#by this API, you can search by /search/apple, two function have same functionality
def search_recipe_bykw(kw):
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	# encode error
	connection.set_character_set('utf8')
	cursor.execute('SET CHARACTER SET utf8;')
	#print(kw)
	keyword = kw
	cursor.execute("SELECT r.id_R, i.Name_R, i.Name_I, r.rating FROM Recipe r, Ingre i WHERE r.name_R = i.name_R AND i.name_I LIKE '%s' ORDER BY i.Name_I"%('%'+ keyword + '%',))
	data = cursor.fetchall()
        total_dict = []
	for i in data:
		if i:
			r_dict = {
			'RecipeID':i[0],
			'RecipeName':i[1],
			'IngredientName':i[2],
			'Rating':i[3]
			}
		total_dict.append(r_dict)
	return render_template('search_recipe.html', data = total_dict)


@app.route("/jumptorecipe/<number>")
def jump_recipe(number):
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	cursor.execute("SELECT * from Recipe where id_R = %s" % number)
	i = cursor.fetchall()[0]
	# change ingredient string into a list
	#print(i[6])
	ingredient = i[6][2:-2] if i[6]!=None else None
	#print(ingredient)
	ingrelist = ingredient.split("', '")
	
	# change direction string into a list
	#print(i[8])
	direction = i[8][2:-2] if i[8]!=None else None
	#print(direction)
	if direction==None:
		dirlist=[]
	else:
		dirlist = direction.split("', '")
	# change category string into a list
	#print(i[7])
	category = i[7][2:-2] if i[7]!=None else None
	catelist = category.split("', '")

	if i[1]!=None:
		des = i[1].strip()
	else:
		des = ''
	# create a dictionary
	r_dict = {
	'ID':i[10],
	'Name':i[0],
	'Description':des,
	'Calories':i[2],
	'Fat':i[3],
	'Protein':i[4],
	'Sodium':i[5],
	'Ingredient':ingrelist,
	'Categories':catelist,
	'Directions':dirlist,
	'Rating':i[9]}
        cursor.execute('SELECT User_name, id_U, id_C, comment FROM Comment,EC_user WHERE User_id=id_U and id_R=%s;'%number)
	cdata = cursor.fetchall()

        comment_dict = []
	for i in cdata:
		#print(i)
		if i:
			c_dict={
			'uName':i[0],
			'uID':i[1],
			'cID':i[2],
			'Comment':i[3],
			}
		comment_dict.append(c_dict)

	username = request.values.get('name')
	fav = False
	if 'logged_in' in session:
		cursor.execute("SELECT id_R FROM Favorite_R WHERE id_U = %s and id_R = %s" %(session['user_id'],number))
		#print('user', session['user_id'])
		#print(type(session['user_id']))
		user_fav_exist = cursor.fetchall()
		#print('number', number)
		#print(type(number))
		#print(user_fav_exist)
		if user_fav_exist != ():
			if int(user_fav_exist[0][0]) == int(number):
				#print('uuuuu',user_fav_exist[0][0])
				fav = True #fav done
				#print('true',fav)
		elif user_fav_exist == ():
			fav = False #to do fav
			#print('false',fav)
		#print(user_fav_exist)

		#print(fav)
		return render_template('get_recipe.html', name = 'Dear customer', data = r_dict, cdata = comment_dict, fav = fav)
	else:
		return render_template('get_recipe.html', name = 'Dear customer', data = r_dict, cdata = comment_dict, fav = fav)

@app.route("/addrecipe", methods = ['GET', 'POST'])
def addrecipe():
	return render_template('add_recipe.html')

@app.route("/newrecipe", methods = ['GET', 'POST'])
def newrecipe():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	#print("1")
	name = request.values.get('name')
	#print(name)
	des = request.values.get('description')
	cal = request.values.get('calories')
	if cal=="":
		cal="NULL"

	fat = request.values.get('fat')
	if fat=="":
		fat="NULL"

	protein = request.values.get('protein')
	if protein=="":
		protein="NULL"
	#print("protein" ,protein)
	#print(type(protein))

	sodium = request.values.get('sodium')
	if sodium=="":
		sodium="NULL"
	
	ingre = request.values.get('ingredients')
	ingrelist = ingre.split(';')
	st_ingre = "['"+"', '".join(ingrelist)+"']"
	#print(st_ingre)	

	cat = request.values.get('categories')
	catlist = cat.split(';')
	st_cat = "['"+"', '".join(catlist)+"']"
	#print(st_cat)	

	direc = request.values.get('directions')
	direclist = direc.split(';')
	st_direc = "['"+"', '".join(direclist)+"']"
	#print(st_direc)
	
	rating = request.values.get('rating')
	if rating=="":
		rating="NULL"
	print(rating)
	try:	#transaction
		cursor.execute('''INSERT INTO Recipe(name_R, description, calories, fat, protein, sodium, ingredients, categories, directions, rating) VALUES("%s","%s",%s,%s,%s,%s,"%s","%s","%s","%s");'''%(thwart(name), thwart(des), cal, fat, protein, sodium, thwart(st_ingre), thwart(st_cat), thwart(st_direc), rating))
		connection.commit()
		cursor.execute('SELECT LAST_INSERT_ID();')
		rid = cursor.fetchone()[0];
	except MySQLdb.Error, e:
		print("Transaction failed, rolling back. Error was:")
		print(e.args)
		try:  # empty exception handler in case rollback fails
			connection.rollback()
		except:
			pass

	try:
		for x in catlist:
			cursor.execute("INSERT INTO Ingre(name_I, name_R) VALUES('%s','%s');"%(thwart(x), thwart(name)))
			connection.commit()
	except:
		connection.rollback()
	uid = session['user_id']
	#print("rid", rid)
	try:
		cursor.execute("INSERT INTO newrecipe(uid,rid) VALUES(%s, %s);"%(uid, rid))
		connection.commit()
	except:
		connection.rollback()
	cursor.close()
	connection.close()

	return redirect('/jumptorecipe/%s'%rid)

@app.route("/edit_recipe", methods = ['GET', 'POST'])
def edit_recipe():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	rid = request.values.get('rid')
	cursor.execute('SELECT * FROM Recipe WHERE id_R=%s;'%rid)
	temp = cursor.fetchall()
	return render_template('edit_recipe.html', recipe = temp)


@app.route("/editrecipe", methods = ['GET', 'POST'])
def editrecipe():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	#print("1")
	rid = request.values.get('rid')
	#print('rrr',rid)
	cursor.execute('''SELECT name_R FROM Recipe WHERE id_R=%s;'''%rid)
	oldname = cursor.fetchall()[0][0]
	name = request.values.get('name')
	#print(name)

	des = request.values.get('description')
        cal = request.values.get('calories')
        if cal=="":
                cal="NULL"

        fat = request.values.get('fat')
        if fat=="":
                fat="NULL"

        protein = request.values.get('protein')
        if protein=="":
                protein="NULL"
        #print("protein" ,protein)
        #print(type(protein))

        sodium = request.values.get('sodium')
        if sodium=="":
                sodium="NULL"

        ingre = request.values.get('ingredients')
        ingrelist = ingre.split(';')
        st_ingre = "['"+"', '".join(ingrelist)+"']"
        #print(st_ingre)

        cat = request.values.get('categories')
        catlist = cat.split(';')
        st_cat = "['"+"', '".join(catlist)+"']"
        #print(st_cat)

        direc = request.values.get('directions')
        direclist = direc.split(';')
        st_direc = "['"+"', '".join(direclist)+"']"
        #print(st_direc)

	rating = request.values.get('rating')
        if rating=="":
			rating="NULL"

	#print(1)
	#print('''UPDATE Recipe SET name_R="%s", description="%s", calories=%s, fat=%s, protein=%s, sodium=%s, ingredients="%s", categories="%s", directions="%s" WHERE id_R=%s;'''%(name, des, cal, fat, protein, sodium, ingre, cat, direc,rid))

	cursor.execute('''UPDATE Recipe SET name_R="%s", description="%s", calories=%s, fat=%s, protein=%s, sodium=%s, ingredients="%s", categories="%s", directions="%s", rating="%s" WHERE id_R=%s;'''%(thwart(name), thwart(des), cal, fat, protein, sodium, thwart(ingre), thwart(cat), thwart(direc),rating,rid))
	connection.commit()
	#print(2)
	catlist = cat.split(",")
	for x in catlist:
		#print(3)
		cursor.execute("UPDATE Ingre SET name_I='%s' WHERE name_R='%s';"%(thwart(x),thwart(oldname)))
		connection.commit()
	cursor.execute("UPDATE Ingre SET name_R='%s' WHERE name_R='%s';"%(thwart(name),thwart(oldname)))
	connection.commit()
	cursor.close()
	connection.close()
	return redirect('profile')


@app.route("/deleterecipe/<rid>", methods = ['GET', 'POST'])
def delete_recipe(rid):
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	#print("Begin deleting")
	#print(cid)
	cursor.execute("DELETE FROM Recipe WHERE id_R=%s" %(rid))
	connection.commit()
	cursor.close()
	connection.close()
	return redirect(request.referrer)


@app.route("/favorite/", methods = ['GET','POST'])
def favorite():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	rid = request.values.get('rid')
	#print('rrrrrrr',rid)
	uid = session['user_id']
	cursor.execute('SELECT id_R FROM Favorite_R WHERE id_U=%s and id_R=%s;'%(uid,rid))
	check_u_r_exist = cursor.fetchall()
	#print('cccc',check_u_r_exist)
	if check_u_r_exist == ():

		#print('''INSERT INTO Favorite_R (id_R, id_U) VALUES (%s,%s);'''%(rid, uid))
		cursor.execute('''INSERT INTO Favorite_R (id_R, id_U) VALUES (%s,%s);'''%(rid, uid))
		connection.commit()
		cursor.close()
		connection.close()

	else:
		if int(check_u_r_exist[0][0]) == int(rid):
			#print('1')
			cursor.execute('DELETE FROM Favorite_R WHERE id_R = %s AND id_U = %s;'%(rid, uid))
			connection.commit()
			cursor.close()
			connection.close()
		elif int(check_u_r_exist[0][0]) != int(rid):
			#print('2')
			#print(rid)
			#print(type(rid))
			#print(check_u_r_exist[0][0])
			#print(type(check_u_r_exist[0][0]))
			cursor.execute('''INSERT INTO Favorite_R (id_R, id_U) VALUES (%s,%s);'''%(rid, uid))
			connection.commit()
			cursor.close()
			connection.close()
	return redirect(request.referrer)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
#	connection = mysql.connect()
	cursor = connection.cursor()
	email = request.values.get('inputEmail')
	name = request.values.get('inputName')
	password = request.values.get('inputPW')
	country = request.values.get('inputCountry')
	x = cursor.execute('SELECT * FROM EC_user WHERE User_email="%s";'%email)
	y = cursor.execute('SELECT * FROM EC_user WHERE User_name="%s";'%name)

	if x > 0 or y > 0:
		flash("This email/username has already been used, please use another email.")
	else:
		sql = '''INSERT INTO `EC_user`(`User_email`, `User_name`, `User_pw`, `User_country`) VALUES("%s","%s","%s","%s");'''%(email, name, password, country)
		cursor.execute(sql)
		connection.commit()
		flash("Thank you for register!")

	connection.rollback()
	cursor.close()
	connection.close()
	return render_template('index.html')

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('login_page'))
	return wrap

@app.route('/logout')
@login_required
def logout():
	session.clear()
	session['logged_in'] = False
	flash("You have been logged out!")
	gc.collect()
	return redirect(request.referrer)


@app.route('/login/', methods = ['GET','POST'])
def login_page():
	#error = None
	try:
		connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
		cursor = connection.cursor()

		if request.method == 'GET':
			data = cursor.execute('SELECT * FROM EC_user WHERE User_email = "%s";' %thwart(request.values.get('email')))
			data = cursor.fetchone()[1]
			password = request.values.get('PW')

			if password == data:
				session['logged_in'] = True
				session['user_email'] = request.values.get('email')
				cursor.execute('SELECT User_id FROM EC_user WHERE User_email="%s";'%thwart(request.values.get('email')))
				iddata = cursor.fetchall()
				userid = iddata[0][0]

				cursor.execute('SELECT User_name FROM EC_user WHERE User_email="%s";'%thwart(request.values.get('email')))
				user = cursor.fetchall()
				username = user[0][0]
				session['user_name'] = username

				session['user_id']=userid
				flash("You are now logged in.")
				return redirect(request.referrer)
			else:
				flash("Invalid credentials. Try Again.(E1)")  #wrong pw
		gc.collect()
		cursor.close()
		connection.close()
		return redirect(request.referrer)

	except Exception as e:
		#flash(e)
		flash("Invalid credentials. Try Again.(E2)")  #no such email
		return redirect(request.referrer)


@app.route("/addcomment/", methods = ['GET','POST'])
def add_comment():
        connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
        cursor = connection.cursor()
        if request.method == 'GET':
                uid = session['user_id']
		rid = request.values.get('rid')
		#print(rid)
                comment = request.values.get('usercomment')
		try:
			#print('''INSERT INTO Comment (id_R, id_U, comment) VALUES (%s,%s,'%s');'''%(rid, uid, thwart(request.values.get('usercomment'))))
                	cursor.execute('''INSERT INTO Comment(id_R,id_U,comment) VALUES(%s,%s,'%s');''' %(rid,uid,thwart(request.values.get('usercomment'))))
			connection.commit()
			cursor.close()
			connection.close()
		except:
			print('Error in Insertion')
	return redirect(request.referrer)


@app.route("/editcomment/<cid>", methods = ['GET', 'POST'])
def edit_comment(cid):
        connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
        cursor = connection.cursor()
	cursor.execute("SELECT id_R FROM Comment WHERE id_C=%s"%(cid))
	xx = cursor.fetchall()
	rid = xx[0][0]
	#print(rid)
	#print(type(rid))
        if request.method == 'GET':
                comment = request.values.get('editusercom')
                try:
			cursor.execute("UPDATE Comment SET comment='%s' WHERE id_C=%s" % (comment, cid))
                        connection.commit()
                except:
                        print('Error in Updating')
	cursor.close()
	connection.close()
        return redirect(request.referrer)

@app.route("/deletecomment/<cid>", methods = ['GET', 'POST'])
def delete_comment(cid):
        connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
        cursor = connection.cursor()
	#print("Begin deleting")
	#print(cid)
        cursor.execute("SELECT id_R FROM Comment WHERE id_C=%s"%(cid))
        xx = cursor.fetchall()
        rid = xx[0][0]
	#print(rid)
	#print(type(rid))
        if request.method == 'GET':
                try:
                        cursor.execute("DELETE FROM Comment WHERE id_C=%s" %(cid))
			connection.commit()
                except:
                        print('Error in Deleting')
        cursor.close()
	connection.close()
	return redirect(request.referrer)

@app.route("/profile", methods = ['GET', 'POST'])
def profile():
	connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
	cursor = connection.cursor()
	if session['logged_in']:
		uid = session['user_id']
	else:
		return render_template('index.html')
	cursor.execute('SELECT id_R, id_U FROM Favorite_R WHERE id_U = %s;'%uid)
	fav_and_user_list = cursor.fetchall()
	#print(fav_and_user_list)
	fav_list = []
	for i in fav_and_user_list:
		cursor.execute('SELECT name_R FROM Recipe WHERE id_R = %s;'%i[0])
		temp = cursor.fetchall()[0][0]
		fav_list.append((int(i[0]),temp))
	#print(fav_list)

	cursor.execute('SELECT rid FROM newrecipe WHERE uid = %s;'%uid)
	user_re_list = cursor.fetchall()
	#print(user_re_list)
	user_recipe = []
	for i in user_re_list:
		cursor.execute('SELECT name_R FROM Recipe WHERE id_R = %s;'%i[0])
		temp = cursor.fetchall()[0][0]
		user_recipe.append((int(i[0]),temp))
	#print(user_recipe)

	cursor.execute('SELECT Rating, Calrories, Fat, Protein, Sodium FROM Nutrition WHERE id_U = %s;'%uid)
	list = cursor.fetchall()
	if list:
		#print("Nutrition list:", list)
		rating = list[0][0]

		nut_list = {
		'Calories':list[0][1],
		'Fat':list[0][2],
		'Protein':list[0][3],
		'Sodium':list[0][4]
		}
	else:
		rating=0
		nut_list = {
		'Calories':0,
		'Fat':0,
		'Protein':0,
		'Sodium':0
		}

	#print("Nutrition list 2:",nut_list)
	cursor.execute('SELECT AVG(calories), AVG(fat), AVG(protein), AVG(sodium) FROM Recipe;')
	avg_list = cursor.fetchall()
	avg_nut = {
	'Calories': avg_list[0][0],
	'Fat': avg_list[0][1],
	'Protein': avg_list[0][2],
	'Sodium': avg_list[0][3]
	}
	
#****************Recommendation starts****************
#******************Stored procedure*******************
	cursor.callproc('get_rec', [uid])	
	temp_list = cursor.fetchall()
	result = []
	total_dict = {}
	if temp_list != ():
		for i in range(min(5,len(temp_list))):
			if temp_list[0] not in total_dict.keys():
				r_dict = {
				'RecipeID':temp_list[i][0],
				'RecipeName':temp_list[i][1],
				'Weight':temp_list[i][2]
				}
				total_dict[temp_list[i][0]] = r_dict
		#print(total_dict.values())
		
		for i in total_dict.values():
			result.append((i['RecipeID'],i['RecipeName']))

	return render_template("profile.html", all_fav = fav_list, all_recipe = user_recipe, rating = rating, nutrition = nut_list, avg_nutrition = avg_nut, recommend = result)


@app.errorhandler(404)
def page_not_found(e):
	flash("Woops, this page is still under construction. (404)")
	flash("Click icon back to Home. (404)")
	return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
	flash("500 ERROR, check out below.")
	flash(e)
	return render_template("500.html", error = e)


if __name__ == "__main__":
	app.run()

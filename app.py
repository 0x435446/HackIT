from flask import Flask
from flask import render_template,jsonify
from flask import request,redirect,session,send_file,send_from_directory
from hashlib import sha256
import importlib.util
import MySQLdb



app = Flask(__name__)

app.secret_key = 'PapanasiCuBranza123456'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlagFlag123.'
app.config['MYSQL_DB'] = 'BlockIT'

app.config['UPLOAD_FOLDER']='/tmp/upload'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['TEMPLATES_AUTO_RELOAD'] = True

#FlagFlag123.


@app.route('/', methods=['GET', 'POST'])
def index():
	print (session['loggedin'])
	if session['loggedin'] == True:
		return render_template('index.html')
	else:
		return redirect('/login')


@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
	if session['loggedin'] == True:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		cursor.execute("SELECT * FROM challenges")
		data = cursor.fetchall()
		print (data)
		return render_template('challenges.html')
	else:
		return redirect('/login')


@app.route('/getCategoryDetails', methods=['GET', 'POST'])
def getCategoryDetails():
	if session['loggedin'] == True:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		print (request.form['Category'])
		cursor.execute("SELECT challenges.Nume,Puncte,users.Nume,Autor,Dificultate,Location FROM challenges inner join users ON users.ID=challenges.Firstblood WHERE challenges.Categorie='"+request.form['Category']+"'")
		data = cursor.fetchall()
		ceva=[]
		forret=[]
		for i in data:
			ceva.append(i)
		for i in ceva:
			forret.append("|".join(str(v) for v in i))
		print (forret)
		return "^".join(forret)
	else:
		return redirect('/login')

@app.route('/Challenges/<path:filename>', methods=['GET', 'POST'])
def download(filename):    
	if session['loggedin'] == True:
		return send_from_directory(directory='Challenges', filename=filename)
	else:
		return redirect('/login')


@app.route('/getChallengeDetails', methods=['GET', 'POST'])
def getChallengeDetails():
	if session['loggedin'] == True:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		cursor.execute("SELECT challenges.Nume,Puncte,Descriere, Location FROM challenges WHERE challenges.Nume='"+request.form['Challenge']+"'")
		data = cursor.fetchall()
		ceva = []
		for i in data[0]:
			ceva.append(str(i))
		print (ceva)
		return "|".join(ceva)
	else:
		return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')



@app.route('/log', methods=['GET', 'POST'])
def log():
	if session['loggedin'] == False:
		if request.method == 'POST':
			print (request.form)
			username = MySQLdb.escape_string(request.form['username']).decode()
			password = MySQLdb.escape_string(request.form['password']).decode()
			x = 1
			if x == 1:
				db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
				cursor = db.cursor()
				cursor.execute("SELECT * FROM users")
				users = list(cursor.fetchall())
				db.close()
				for i in range(len(users)):
					if users[i][1] == username:
						print ("USERNAME CORECT")
						if (sha256(password.encode()).hexdigest()==users[i][2]):
							print ("Logare cu success")
							session['loggedin'] = True
							session['username']=username
							print (session['loggedin'])
						else:
							print ("INCORRECT")
					else:
						print ("INCORRECT")
		return redirect("/")
	else:
		return redirect("/")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['loggedin'] = False
	return redirect("/")
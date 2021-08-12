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

	return render_template('index.html')


@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
	db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
	cursor = db.cursor()
	cursor.execute("SELECT * FROM challenges")
	data = cursor.fetchall()
	print (data)
	return render_template('challenges.html')


@app.route('/getCategoryDetails', methods=['GET', 'POST'])
def getCategoryDetails():
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

@app.route('/Challenges/<path:filename>', methods=['GET', 'POST'])
def download(filename):    
    return send_from_directory(directory='Challenges', filename=filename)
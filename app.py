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
	if 'loggedin' not in session:
		session['loggedin'] = False
		session['username']=""
		session['ID']=""

	if session['loggedin'] == True:
		return render_template('index.html')
	else:
		return redirect('/login')

@app.route('/challenges', methods=['GET', 'POST'])
def challenges():
	if session['loggedin'] == True:
		print (session['username'])
		print (session['ID'])
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		cursor.execute("SELECT * FROM challenges")
		data = cursor.fetchall()
		return render_template('challenges.html')
	else:
		return redirect('/login')


@app.route('/getCategoryDetails', methods=['GET', 'POST'])
def getCategoryDetails():
	if session['loggedin'] == True:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		print (request.form['Category'])
		cursor.execute("SELECT challenges.Nume,challenges.Puncte,users.Nume,Autor,Dificultate,Location FROM challenges inner join users ON users.ID=challenges.Firstblood WHERE challenges.Categorie='"+request.form['Category']+"'")
		data = cursor.fetchall()
		ceva=[]
		forret=[]
		for i in data:
			ceva.append(i)
		for i in ceva:
			forret.append("|".join(str(v) for v in i))

		cursor.execute("SELECT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='"+request.form['Category']+"'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			print (str(i[1]),"====",session['ID'])
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		'''
		for i in solved:
			retSolved.append("|".join(str(v) for v in i))
		'''
		print (solved)
		return "^".join(forret)+"~"+'|'.join(solved)
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
							session['ID']=users[i][0]
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


@app.route('/register', methods=['GET', 'POST'])
def register():
	if session['loggedin'] == False:
		if request.method == 'POST':
			print (request.form)
			username = MySQLdb.escape_string(request.form['username']).decode()
			password = MySQLdb.escape_string(request.form['password']).decode()
			email = MySQLdb.escape_string(request.form['email']).decode()
			x = 1
			if x == 1:	
				db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit")
				cursor = db.cursor()
				cursor.execute("INSERT INTO users (Nume,Parola,Email) VALUES('"+ username +"','"+ sha256(password.encode()).hexdigest() +"','"+email+"')")
				db.commit()
				db.close()
		return redirect("/")
	else:
		return redirect("/")


@app.route('/submitFlag', methods=['GET', 'POST'])
def submitFlag():
	if session['loggedin'] == True:
		flag = str(MySQLdb.escape_string(request.form['flag']))
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		cursor.execute("SELECT ID, challenges.Nume,Puncte FROM challenges WHERE challenges.Flag='"+flag+"'")
		data = cursor.fetchall()
		puncte = 0
		numeChallenge=""
		IDChallenge=""

		if len(data) > 0:
			puncte = int(data[0][2])
			numeChallenge = str(data[0][1])
			IDChallenge = str(data[0][0])
			cursor.execute("SELECT * FROM solves WHERE solves.ID_challenge='"+IDChallenge+"' and solves.ID_user = '"+str(session['ID'])+"'")
			data = cursor.fetchall()
			if len(data) == 0:
				print ("AM AJUNS AICI   "+str(IDChallenge))

				cursor.execute("INSERT INTO solves (ID_user,ID_challenge) VALUES('"+ str(session['ID']) +"','"+str(IDChallenge)+"')")
				db.commit()

				cursor.execute("SELECT Puncte FROM users WHERE users.ID='"+str(session['ID'])+"'")
				data = cursor.fetchall()
				Puncte_curente = int(data[0][0])
				Puncte_curente += int(puncte)

				cursor.execute("UPDATE users SET Puncte = "+str(Puncte_curente)+" WHERE ID='"+str(session['ID'])+"'")
				db.commit()

				cursor.execute("SELECT Solves FROM challenges WHERE challenges.ID='"+str(IDChallenge)+"'")
				data = cursor.fetchall()
				Solves = int(data[0][0])
				Solves += 1

				cursor.execute("SELECT Firstblood FROM challenges WHERE challenges.ID='"+str(IDChallenge)+"'")
				data = cursor.fetchall()
				Fb = int(data[0][0])
				ok = 0
				if str(Fb) == "-1":
					ok = 1

				cursor.execute("UPDATE challenges SET Solves = "+str(Solves)+" WHERE ID='"+str(IDChallenge)+"'")
				db.commit()

				if ok == 1:
					cursor.execute("UPDATE challenges SET Firstblood = "+str(session['ID'])+" WHERE ID='"+str(IDChallenge)+"'")
					db.commit()
			db.close()

		return redirect('/challenges')
	else:
		return redirect('/login')



@app.route('/profile', methods=['GET', 'POST'])
def profile():
	if session['loggedin'] == True:
		db=MySQLdb.connect(host="localhost",user="root",passwd="FlagFlag123.",db="hackit" )
		cursor = db.cursor()
		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Networking'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Networking_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Forensics'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Forensics_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Web'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Web_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Cryptography'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Cryptography_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Reversing'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Reversing_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Pwn'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Pwn_Solved = len(solved)

		cursor.execute("SELECT DISTINCT challenges.Nume, solves.ID_user FROM challenges inner join solves ON solves.ID_challenge=challenges.ID WHERE challenges.Categorie='Misc'")
		data = cursor.fetchall()
		solved = []
		retSolved=[]
		for i in data:
			if str(i[1]) == str(session['ID']):
				solved.append(i[0])
		Misc_Solved = len(solved)


		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Networking'")
		data = cursor.fetchall()
		Total_Networking=len(data)
		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Forensics'")
		data = cursor.fetchall()
		Total_Forensics=len(data)
		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Reversing'")
		data = cursor.fetchall()
		Total_Reversing=len(data)
		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Pwn'")
		data = cursor.fetchall()
		Total_Pwn=len(data)
		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Cryptography'")
		data = cursor.fetchall()
		Total_Crypto=len(data)
		cursor.execute("SELECT challenges.Nume FROM challenges WHERE challenges.Categorie='Web'")
		data = cursor.fetchall()
		Total_Web=len(data)

		cursor.execute("SELECT users.Puncte FROM users WHERE users.ID='"+str(session['ID'])+"'")
		data = cursor.fetchall()
		Puncte_user=data[0][0]
		print ("AICI BOSS",Puncte_user)

		return render_template('profile.html',
			Networking_Solved=Networking_Solved, Forensics_Solved=Forensics_Solved, Web_Solved=Web_Solved, Cryptography_Solved=Cryptography_Solved, Reversing_Solved=Reversing_Solved, Pwn_Solved=Pwn_Solved,
			Total_Networking = Total_Networking, Total_Forensics=Total_Forensics, Total_Web=Total_Web, Total_Crypto=Total_Crypto, Total_Reversing=Total_Reversing,Total_Pwn=Total_Pwn,
			Username=session['username'],
			Puncte=Puncte_user)
	else:
		return redirect('/login')

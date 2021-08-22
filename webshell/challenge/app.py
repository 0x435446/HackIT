from flask import Flask
from flask import render_template,jsonify
from flask import request,redirect,session,send_file,send_from_directory
import subprocess


app = Flask(__name__)

app.secret_key = 'ceaceaceacea'
#FlagFlag123.


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		command=request.form['command']
		if len(command.split(" ")) <3:
			if command.split(" ")[0] == 'ls' or command.split(" ")[0] == 'cat' or command.split(" ")[0] == 'pwd'or command.split(" ")[0] == 'whoami':
				if len(command.split(" "))==1:
					command+=" "
				if command.split(" ")[0] == 'whoami':
					output = subprocess.check_output(command.split(" ")[0], shell=True).decode().replace("\n","<br>")
					print (output)
					return output
				elif ".." not in command.split(" ")[1]:
					output = subprocess.check_output(command.split(" ")[0]+" ~/ReadMe/ReadMe/"+command.split(" ")[1], shell=True).decode().replace("\n","<br>")
					print (output)
					return output
				else:
					return "Noughty Noughty"
			else:
				return "Noughty Noughty"
		else:
			return "Noughty Noughty"
	else:	
		return render_template('index.html')
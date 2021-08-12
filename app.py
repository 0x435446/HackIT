from flask import Flask
from flask import render_template,jsonify
from flask import request,redirect,session,send_file
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





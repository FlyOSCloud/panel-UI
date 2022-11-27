# FlyOS Cloud Project GPL-3.0 LICENSE
# login.py creator: Edward Hsing
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, UserMixin, login_user, logout_user
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
import socket

# for sqlite
import sqlite3
conn = sqlite3.connect('flyos.db')
cs = conn.cursor()
try:
    cs.execute('''CREATE TABLE user
        (id varchar(20) PRIMARY KEY,
            name varchar(20),
            password varchar(20)
            );''')
except:
    pass
passwordhash = generate_password_hash('123456')
cs.execute(f"REPLACE INTO user (id, name, password) VALUES ('1', 'admin', '{passwordhash}')")
cs.execute(f"REPLACE INTO user (id, name, password) VALUES ('2', 'admin1', '{passwordhash}')")
conn.commit()
cs.close()
conn.close()


def checkuser(username, password):
        conn = sqlite3.connect('flyos.db')
        cs = conn.cursor()
        cursor = cs.execute(f"select * from user where name='{username}';")
        print(cursor)
        for row in cursor:
            uid = row[0]
            getusername = row[1]
            getpassword = row[2]
        cs.close()
        conn.close()
        try:
            if getusername == username:
                if check_password_hash(getpassword, password):
                    return True
            else:
               return None
        except:
            return None
class User(UserMixin):
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return "1"

# end flyos user init
#start web function
def netip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
        s.close()
    except:
        return 'Failed to obtain IP address'
def internetip():
    try:
        import requests
        return requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    except:
        return 'fetch failed or no internet connection'
def networkconf():
    return netip()
#end web function
app = Flask(__name__)

app.secret_key = os.urandom(24) # protect flyos
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user
@app.route('/')
@login_required
def redirectmain():
    redirect(url_for('panelmain'))
@app.route('/panel/main')
@login_required
def panelmain():
    return render_template('./main.html',username=user_name,
                                         osuname=subprocess.getoutput("uname -a"),
                                         network_conf=networkconf())
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_name
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        print(user_name + password)
        user = User()
        if user_name == '':
            return 'Incorrect username or password'
        if password == '':
            return 'Incorrect username or password'
        if checkuser(user_name, password):
            login_user(user)
            return redirect(url_for('panelmain'))
        return 'Incorrect username or password'
        

    return render_template('./login.html')
@app.route('/system/runcmd/')
@login_required
def syscmd():
    getcmd = request.args.get('shell')
    get_result = os.popen(getcmd).read()
    return get_result
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route("/panel/internetip")
@login_required
def checkinternetip():
    return render_template('./internetip.html',internetip=internetip(),netip=netip())
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

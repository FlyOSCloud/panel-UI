import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def changedbpassword(password):
    passwordhash = generate_password_hash(password)
    conn = sqlite3.connect('flyos.db')
    cs = conn.cursor()
    cursor = cs.execute(f"select * from user where name='admin';")
    cs.execute(f"UPDATE user SET password = '{passwordhash}' WHERE id = 1;")
    # UPDATE user SET password = '{password}' WHERE id = 1;
    conn.commit()
    cs.close()
    conn.close()
print("""
FlyOS Settings
Enter an option to continue, like 1 or 2 or 3
-----------------------------------------------------------------
1.Change user "flyos" password
2.View network configuration
3.Set Panel Admin Password
0.EXIT
-----------------------------------------------------------------
""")
while True:
    opts = input("please enter an option:")
    if opts == '0':
        os.system("python3 /flyos/bootscript.py")
    if opts == '1':
        os.system("passwd flyos")
    if opts == '2':
        os.system("ifconfig -a")
    if opts == '3':
        passwd = input('Please set a password for the user "admin": ')
        changedbpassword(passwd)
        print("[*] Done!")
    
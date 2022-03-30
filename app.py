from flask import Flask,render_template,request,redirect,url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
   conn = psycopg2.connect(
   host = 'localhost',
   database = 'X',
   user = 'postgres',
   password = 'X'
   )

   return conn

@app.route("/register")
def register(error =None):   
    return render_template("register.html", error=error)

@app.route("/register", methods=["POST"])
def registers():

    conn = get_db_connection()
    curr = conn.cursor()

    users_list = curr.execute("SELECT username, password FROM users")

    if request.method == 'POST':
        in_name = request.form['name']
        in_user = request.form['username']
        in_pass = request.form['password']
        in_mail = request.form['email']
        if [in_user,in_pass] not in users_list:
            curr.execute("INSERT INTO users (name, username, password, email) VALUES (%s, %s, %s, %s)" [in_name, in_user, in_pass, in_mail])
            curr.close()
            conn.close()
            return redirect(url_for('/'))
        else:
            curr.close()
            conn.close()
            return redirect(url_for('register',errType='existingaccount'))

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/", methods=["POST", "GET"])
def logins():

    conn = get_db_connection()
    curr = conn.cursor()

    users_list = curr.execute("SELECT username, password FROM users")

    if request.method == 'POST':
        in_user = request.form['username']
        in_pass = request.form['password']
        if [in_user, in_pass] in users_list:
            name = curr.execute("SELECT name FROM users WHERE username = %s AND password = %s" [in_user, in_pass])
            curr.close()
            conn.close()
            return redirect(url_for('shop',name=name,username=in_user,password=in_pass))
        else:
            return redirect(url_for('login',errType='faillogin'))

@app.route("/shop/<name>")
def shop(name):
    return render_template("shop.html", name=name)

@app.route("/shop/<name>", methods=["POST", "GET"])
def purchase(name, username, password):
    i=1

if __name__ == '__main__':
   app.run(debug=True)
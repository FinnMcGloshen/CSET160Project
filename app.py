from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
username = 'admin'
pswrd = 'welcome1'
userpass = [['admin','password']]

@app.route('/welcome/<userID><password>')
def welcome(name):
    return render_template('welcome.html',name=name)


conn = psycopg2.connect(
    host = 'localhost',
    database = 'flask_db',
    password = 'pgadmin',
    user = 'postgres'
)

cur = conn.cursor()

cur.execute('INSERT INTO books (title, author)'
'VALUES(%s, %s)',
('TestName','TestAuthor'))

conn.commit()
cur.close()
conn.close()

@app.route('/login')
def hello():
    return render_template('login.html')


@app.route('/incorrect/<errType>')
def incorrect(errType):
    return render_template('incorrect.html',errType=errType)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        userpassed = request.form['pw']
        if [user,userpassed] in userpass:
            return redirect(url_for('welcome',name=user,password = userpassed))
        
        else:
            return redirect(url_for('incorrect',errType='Incorrect Password'))

@app.route('/sign_up')
def reg():
    return render_template('sign_up.html')


@app.route('/sign_up', methods=['POST','GET'])
def register():
    if request.method == 'POST':
                user = request.form['unr']
                pass1 = request.form['pwr']
                if [user,pass1] not in userpass:
                    userpass.append([user,pass1])
                    return redirect(url_for('login'))
                else:
                    return redirect(url_for('incorrect',errType = 'Account already exists'))
    else:
        user = request.args.get('nm')
        userpassed = request.args.get('pw')
        if [user,userpassed] in userpass:
            return redirect(url_for('welcome',name = user))
        else:
            return redirect(url_for('incorrect',errType='Account already exists'))


if __name__ == '__main__':
    app.run(debug=True)
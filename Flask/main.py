from flask import Flask, render_template, send_from_directory, request, redirect
import sqlite3  

class DBclass:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.cur = self.db.cursor()
    def execute(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
db = DBclass("Flask/database.db")

app = Flask(__name__, template_folder="../") 
@app.route("/") 
def root() -> str: 
    return render_template('SignupPage/signup.html')

@app.route("/LoginPage/login.html") 
def login_page() -> str: 
    return render_template('LoginPage/login.html')

@app.route("/SignupPage/signup.html") 
def signup_page() -> str: 
    return render_template('SignupPage/signup.html')


@app.route("/user_signup", methods = ["POST"])
def user_signup():
    user_name = request.form["username"]
    user_phone = request.form["mobileNumber"]
    user_email = request.form["email"]
    user_passw = request.form["password"]

    users = db.execute(f'SELECT * FROM user WHERE phone="{user_phone}";')
    if len(users):
        print("User Already Exists")
        return render_template("SignupPage/signup.html")
    print("Signing up User", user_name, user_phone, user_email, user_passw )
    db.execute(f'INSERT INTO user (name, phone, email, passw) VALUES ( "{user_name}", "{user_phone}", "{user_email}", "{user_passw}");')
    db.db.commit()
    user = db.execute(f'SELECT * FROM user WHERE phone="{user_phone}";')[0]

    return redirect(f"ProfilePage/profile.html?id={user[0]}")

@app.route("/user_login", methods = ["POST"])
def user_login():
    user_email = request.form["email"]
    user_passw = request.form["password"]

    users = db.execute(f'SELECT id,passw FROM user WHERE email="{user_email}";')
    if len(users) == 0:
        print('No User Found with this Email')
        return render_template("LoginPage/login.html", error_code= "No User Found with this Email")
    
    db_passw = users[0][1]
    if user_passw != db_passw:
        print("Wrong Password", user_passw, db_passw)
        return render_template("LoginPage/login.html", error_code= "Wrong Password")

    user_id = users[0][0]
    return redirect(f'ProfilePage/profile.html?id={user_id}')    

@app.route("/ProfilePage/profile.html") 
def profile_page() -> str: 
    user_id = request.args.get('id') 
    (user_name, user_phone, user_email) = db.execute(f'SELECT name, phone, email FROM user WHERE id={user_id}')[0]
    print("Profile ", user_name, user_phone, user_email)
    return render_template('ProfilePage/profile.html', 
                           name = user_name,
                           phone = user_phone,
                           email = user_email)



    
if __name__ == "__main__": 
    app.run(debug=True)
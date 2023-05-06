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
    return render_template('SignUpPage/signup.html')

# Default Page load

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('../', path) 

@app.route("/LoginPage/login.html") 
def login_page() -> str: 
    return render_template('LoginPage/login.html')

@app.route("/SignUpPage/signup.html") 
def signup_page() -> str: 
    return render_template('SignUpPage/signup.html')

@app.route("/ProfilePage/profile.html") 
def profile_page() -> str: 
    user_id = request.args.get('id') 
    (user_name, user_phone, user_email) = db.execute(f'SELECT name, phone, email FROM user WHERE id={user_id}')[0]
    print("Profile ", user_name, user_phone, user_email)
    return render_template('ProfilePage/profile.html', 
                           name = user_name,
                           phone = user_phone,
                           email = user_email)


@app.route("/DashBoardPage/dashboard.html") 
def dashboard_page() -> str: 
    user_id = request.args.get('id')
    data1 = db.execute(f'SELECT p_group.name, group_expense.id, group_expense.date, expense_contri.amt \
                       FROM p_group INNER JOIN group_expense INNER JOIN expense_contri \
                       ON expense_contri.u_id={user_id} AND \
                            group_expense.id=expense_contri.e_id AND \
                            group_expense.g_id=p_group.id \
                        ORDER BY group_expense.date ASC; ')
    data2 = db.execute(f'SELECT group_expense.id, group_expense.amt \
                       FROM group_expense \
                       WHERE group_expense.payee_id={user_id};')
    data3 = db.execute(f'SELECT user1.name, user2.name, payment.date, payment.amt\
                       FROM user user1 INNER JOIN user user2 INNER JOIN payment\
                       ON payment.u1_id=user1_id AND payment.u2_id=user2_id\
                       ORDER BY payment.date ASC;')


# API endpoints

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

@app.route("/add_expense", methods = ["POST"])
def add_expense():
    payee_id = request.form["user_id"]
    total_amt = request.form["user_id"]
    contri_ids = request.form["user_id"]
    contri_amts = request.form["user_id"]
    exp_date = request.form["user_id"]
    exp_name = request.form["user_id"]
    group_id = request.form["user_id"]

    db.execute(f'INSERT INTO group_expense (g_id, payee_id, amt, date, name) VALUES ({group_id}, {payee_id}, {total_amt}, {exp_date}, {exp_name});')
    db.db.commit()
    exp_id = db.execute(f'SELECT id FROM group_expense WHERE date={exp_date} AND g_id={group_id};')[0][0]
    
    for i, contri_id, contri_amt in enumerate(zip(contri_ids, contri_amts)): 
        db.execute(f'INSERT INTO expense_contri (e_id, u_id, amt) VALUES ({exp_id}, {contri_id}, {contri_amts});')
    db.db.commit()
    return "OK", 200

@app.route("/add_payment", methods = ["POST"])
def add_payment():
    u1_id = request.form["user_id"]
    u2_id = request.form["user_id"]
    total_amt = request.form["user_id"]
    paym_date = request.form["user_id"]
    group_id = request.form["user_id"]

    db.execute(f'INSERT INTO payment (u1_id, u2_id, amt, date, g_id) VALUES ({u1_id}, {u2_id}, {total_amt}, {group_id}, {paym_date});')
    db.db.commit()



if __name__ == "__main__": 
    app.run(debug=True)
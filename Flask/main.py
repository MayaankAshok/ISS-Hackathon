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

def get_compressed():
    # Contri'd expenses
    data1 = db.execute(f'SELECT u_id, amt FROM expense_contri;')
    # Paid Expenses
    data2 = db.execute(f'SELECT payee_id, amt FROM group_expense;')
    # Personal payments
    data3 = db.execute(f'SELECT u1_id, u2_id, amt FROM payment;')

    data_dict= {}
    for (id, amt) in data1:
        if id in data_dict:
            data_dict[id] -= amt
        else:
            data_dict[id] = -amt
    
    for (id, amt) in data2:
        if id in data_dict:
            data_dict[id] += amt
        else :
            data_dict[id] = amt

    for (id1, id2, amt) in data3:
        if id1 in data_dict:
            data_dict[id1] += amt
        else :
            data_dict[id1] = amt
        if id2 in data_dict:
            data_dict[id2] -= amt
        else :
            data_dict[id2] = -amt
    
    data_pos ={}
    data_neg = {}
    for id, amt in data_dict.items():
        if amt >0:
            data_pos[id] = amt
        if amt <0:
            data_neg[id] = -amt

    final_data = {}
    for id, amt in data_dict.values():
        final_data[id] = []
    
    while True:
        if len(data_pos.keys() == 0):
            break
        val1 = data_pos[data_pos.keys()[0]]
        val2 = data_neg[data_neg.keys()[0]]
        if val1 < val2:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val1])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val1])
            del data_pos[data_pos.keys()[0]]
        elif val1> val2:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val2])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val2])
            del data_neg[data_neg.keys()[0]]
        else:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val2])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val2])
            del data_neg[data_neg.keys()[0]]
            del data_pos[data_pos.keys()[0]]
    return final_data

def get_compressed_group(group_id):
    # Contri'd expenses
    data1 = db.execute(f'SELECT u_id, amt FROM expense_contri\
                       WHERE e_id IN (SELECT id FROM group_expense WHERE g_id={group_id});')
    # Paid Expenses
    data2 = db.execute(f'SELECT payee_id, amt FROM group_expense WHERE g_id={group_id};')
    # Personal payments
    data3 = db.execute(f'SELECT u1_id, u2_id, amt FROM payment WHERE g_id={group_id};')

    data_dict= {}
    for (id, amt) in data1:
        if id in data_dict:
            data_dict[id] -= amt
        else:
            data_dict[id] = -amt
    
    for (id, amt) in data2:
        if id in data_dict:
            data_dict[id] += amt
        else :
            data_dict[id] = amt

    for (id1, id2, amt) in data3:
        if id1 in data_dict:
            data_dict[id1] += amt
        else :
            data_dict[id1] = amt
        if id2 in data_dict:
            data_dict[id2] -= amt
        else :
            data_dict[id2] = -amt
    
    data_pos ={}
    data_neg = {}
    for id, amt in data_dict.items():
        if amt >0:
            data_pos[id] = amt
        if amt <0:
            data_neg[id] = -amt

    final_data = {}
    for id, amt in data_dict.values():
        final_data[id] = []
    
    while True:
        if len(data_pos.keys() == 0):
            break
        val1 = data_pos[data_pos.keys()[0]]
        val2 = data_neg[data_neg.keys()[0]]
        if val1 < val2:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val1])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val1])
            del data_pos[data_pos.keys()[0]]
        elif val1> val2:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val2])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val2])
            del data_neg[data_neg.keys()[0]]
        else:
            final_data[data_pos.keys()[0]].append([data_neg.keys()[0], val2])
            final_data[data_neg.keys()[0]].append([data_pos.keys()[0], -val2])
            del data_neg[data_neg.keys()[0]]
            del data_pos[data_pos.keys()[0]]
    return final_data



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
    self_id = request.args.get('self_id')
    (user_name, user_phone, user_email) = db.execute(f'SELECT name, phone, email FROM user WHERE id={user_id};')[0]
    print("Profile ", user_name, user_phone, user_email)
    print(db.execute("PRAGMA table_info(group_participant);"))
    # Mutual Groups
    mut_groups = db.execute(f'SELECT name FROM p_group WHERE\
                            id IN ( SELECT g_id FROM group_participant WHERE u_id={user_id})\
                            AND id IN ( SELECT g_id FROM group_participant WHERE u_id={user_id});')
    # Contri'd expenses
    data1 = db.execute(f'SELECT p_group.name, group_expense.id, group_expense.date, expense_contri.amt \
                       FROM p_group INNER JOIN group_expense INNER JOIN expense_contri \
                       ON expense_contri.u_id={user_id} AND \
                            group_expense.id=expense_contri.e_id AND \
                            group_expense.g_id=p_group.id \
                        ORDER BY group_expense.date ASC; ')
    # Paid Expenses
    data2 = db.execute(f'SELECT group_expense.id, group_expense.amt \
                       FROM group_expense \
                       WHERE group_expense.payee_id={user_id};')
    
    net_amount = sum([data[1] for data in data2]) - sum([data[3] for data in data1])


    return render_template('ProfilePage/profile.html', 
                           name = user_name,
                           phone = user_phone,
                           email = user_email)

@app.route("/DashboardPage/dashboard.html") 
def dashboard_page() -> str: 
    user_id = request.args.get('id')
    # Contri'd expenses
    data1 = db.execute(f'SELECT  group_expense.id, p_group.name, group_expense.date, expense_contri.amt, group_expense.name \
                       FROM p_group INNER JOIN group_expense INNER JOIN expense_contri \
                       ON expense_contri.u_id={user_id} AND \
                            group_expense.id=expense_contri.e_id AND \
                            group_expense.g_id=p_group.id \
                        ORDER BY group_expense.date ASC; ')
    # Paid Expenses
    data2 = db.execute(f'SELECT group_expense.id, group_expense.amt \
                       FROM group_expense \
                       WHERE group_expense.payee_id={user_id};')
    # Personal payments
    data3 = db.execute(f'SELECT user1.name, user2.name, payment.date, payment.amt\
                       FROM user user1 INNER JOIN user user2 INNER JOIN payment\
                       ON payment.u1_id={user_id} OR payment.u2_id={user_id}\
                       ORDER BY payment.date ASC;')
    data1_dict = {}
    for (id, *data) in data1:
        data1_dict[id] = data
    data2_dict = {}
    for (id, *data) in data2:
        data2_dict[id] = data

    records = []
    for id, data in data1_dict.values():
        record_type = 'expense'
        record_date = data[1]
        record_group = data[0]
        amt = -data[2]
        if id in data2_dict.keys():
            amt+= data2_dict[id][0]
        record_amt = amt
        record_name = data[3]
        records.append([record_type, record_date, record_name, record_group, record_amt])

    for (name1, name2, date, amt) in data3:
        records.append(['payment', date, name1, name2, amt])
    
    records.sort(key = lambda a: a[1], reverse= True)
    records = records[:15]

    return render_template("/DashboardPage/dashboard.html", records = records)

@app.route("/DashboardPage/dashboard1.html") 
def dashboard1_page() -> str: 
    user_id = request.args.get('id')

    return render_template("/DashboardPage/dashboard1.html")

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

@app.route("/add_to_group", methods = ["POST"])
def add_payment():
    user_id = request.form["user_id"]
    group_id = request.form["user_id"]
    db.execute(f"INSERT INTO group_participant (u_id, g_id) VALUES ({user_id}, {group_id});")
    db.db.commit()


if __name__ == "__main__": 
    app.run(debug=True)
from flask import Flask, render_template, send_from_directory, request, redirect
import sqlite3  
import datetime

class DBclass:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.cur = self.db.cursor()
    def execute(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
db = DBclass("Flask/database.db")

currentuserid = -1

def get_compressed():
    # Contri'd expenses
    data1 = db.execute(f'SELECT u_id, amt FROM expense_contri;')
    # Paid Expenses
    data2 = db.execute(f'SELECT payee_id, amt FROM group_expense;')
    # Personal payments
    data3 = db.execute(f'SELECT u1_id, u2_id, amt FROM payment;')
    print(data3)
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
    print(data_dict)
    data_pos ={}
    data_neg = {}
    for id, amt, in data_dict.items():
        if amt >0:
            data_pos[id] = amt
        if amt <0:
            data_neg[id] = -amt

    final_data = {}
    for id, amt in data_dict.items():
        final_data[id] = []
    
    while True:
        if len(data_pos.keys())==0:
            break
        if len(data_neg.keys())==0:
            break
        val1 = data_pos[list(data_pos.keys())[0]]
        val2 = data_neg[list(data_neg.keys())[0]]
        if val1 < val2:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val1])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val1])
            del data_pos[list(data_pos.keys())[0]]
        elif val1> val2:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val2])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val2])
            del data_neg[list(data_neg.keys())[0]]
        else:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val2])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val2])
            del data_neg[list(data_neg.keys())[0]]
            del data_pos[list(data_pos.keys())[0]]
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
    for (id, amt) in data_dict.items():
        if amt >0:
            data_pos[id] = amt
        if amt <0:
            data_neg[id] = -amt

    final_data = {}
    for id in data_dict.values():
        final_data[id] = []
    
    while True:
        if len(data_pos.keys() )==0:
            break
        val1 = data_pos[list(data_pos.keys())[0]]
        val2 = data_neg[list(data_neg.keys())[0]]
        if val1 < val2:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val1])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val1])
            del data_pos[list(data_pos.keys())[0]]
        elif val1> val2:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val2])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val2])
            del data_neg[list(data_neg.keys())[0]]
        else:
            final_data[list(data_pos.keys())[0]].append([list(data_neg.keys())[0], val2])
            final_data[list(data_neg.keys())[0]].append([list(data_pos.keys())[0], -val2])
            del data_neg[list(data_neg.keys())[0]]
            del data_pos[list(data_pos.keys())[0]]
    return final_data

def get_groups(user_id):
    data_u = db.execute(f'SELECT id, name FROM user;')
    user_dict = {}
    for id, name in data_u:
        user_dict[id] = name
    final_data = []
    data1 = db.execute(f"SELECT id, name from p_group \
                      WHERE id IN (SELECT g_id FROM group_participant WHERE u_id={user_id});")
    for data in data1:
        data_2 = db.execute(f"SELECT u_id FROM group_participant WHERE g_id={data[0]}")
        members= []
        for (user_id,) in data_2:
            members.append([user_id, user_dict[user_id]])
        final_data.append([data[0], data[1], members])
    # return [[1, 'Hello', [[1,'name1'], [2,'name2']]], [2, 'World',[ [3, 'name3'], [4, 'name4']]]]
    return final_data

def get_common_groups(user1_id, user2_id):
    data_u = db.execute(f'SELECT id, name FROM user;')
    user_dict = {}
    for id, name in data_u:
        user_dict[id] = name
    final_data = []
    data1 = db.execute(f"SELECT id, name from p_group \
                      WHERE id IN (SELECT g_id FROM group_participant WHERE u_id={user1_id})\
                       AND id IN (SELECT g_id FROM group_participant WHERE u_id={user2_id});")

    return data1
    # return [[1, 'Hello', [[1,'name1'], [2,'name2']]], [2, 'World',[ [3, 'name3'], [4, 'name4']]]]


def get_common_records(user1_id, user2_id):
    data3 = db.execute(f'SELECT u1_id, u2_id, amt FROM payment;')
    data3 = [data for data in data3 if user1_id in [data[0], data[1]] and user2_id in [data[0], data[1]]]
    final_data =[]
    for data in data3:
        if data[0] == user1_id:
            final_data.append([1, amt])
        else:
            final_data.append([-1, amt])
    return final_data


def get_timeline(user_id):
    user_id = int(user_id)
    data1 = db.execute(f'SELECT expense_contri.u_id, expense_contri.amt, group_expense.date \
                       FROM expense_contri INNER JOIN group_expense \
                       ON group_expense.id=expense_contri.e_id;')
    # Paid Expenses
    data2 = db.execute(f'SELECT payee_id, amt, date FROM group_expense;')
    # Personal payments
    data3 = db.execute(f'SELECT u1_id, u2_id, amt, date FROM payment;')
    dates = list(set([data[2] for data in data1]+ [data[2] for  data in data2] + [data[3] for data in data3]))
    credits= [0]*len(dates)
    debits= [0]* len(dates)
    print (data1)
    print(data2)
    print(data3)
    
    for data in data1:
        if data[0]==user_id:
            debits[dates.index(data[2])] += data[1]
    for data in data2:
        if data[0]== user_id:
            credits[dates.index(data[2])] += data[1]
    for data in data3:
        if data[0]== user_id:
            credits[dates.index(data[3])] += data[2]
        if data[1] == user_id:
            credits[dates.index(data[3])] += data[2]
    return [dates, credits, debits]

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
    

    # Payments
    paym_to = db.execute(f"SELECT amt FROM payment where u2_id={user_id}; ")
    paym_from = db.execute(f"SELECT amt FROM payment where u1_id={user_id}; ")
    
    net_amount = sum([data[1] for data in data2]) - sum([data[3] for data in data1]) + sum([data[0] for data in paym_from]) - sum([data[0] for  data in paym_to])
    
    common_records = get_common_records(self_id, user_id)
    common_groups = get_common_groups(self_id, user_id)
    return render_template('ProfilePage/profile.html', self_id = self_id,
                           name = user_name,
                           phone = user_phone,
                           email = user_email,
                           groups = get_groups(self_id),
                           common_records = common_records,
                           common_groups = common_groups)

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
                       ON (payment.u1_id={user_id} AND user1.id={user_id})\
                        OR (payment.u2_id={user_id} AND user2.id={user_id})\
                       ORDER BY payment.date ASC;')
    data1_dict = {}
    for (id, *data) in data1:
        data1_dict[id] = data
    data2_dict = {}
    for (id, *data) in data2:
        data2_dict[id] = data

    records = []
    for id, data in data1_dict.items():
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
    print(records)
    records.sort(key = lambda a: a[1], reverse= True)
    records = records[:15]
    
    remaining_debt=  get_compressed()

    [dates, credits, debits] = get_timeline(user_id)
    for i in range(len(dates)):
        dates[i] = datetime.datetime.utcfromtimestamp(int(dates[i])).strftime('%Y-%m-%d')
    print(get_timeline(user_id))

    return render_template("/DashboardPage/dashboard.html", 
                        records = records,
                        groups = get_groups(user_id),
                        payeeID = user_id,
                        dates = dates,
                        credits = credits,
                        debits = debits
                               )


@app.route("/GroupPage/group.html") 
def group_page() -> str: 
    group_id = request.args.get('groupid')
    user_id = request.args.get('id')
    # Paid Expenses
    data1 = db.execute(f'SELECT id, name FROM user;')
    data2 = db.execute(f'SELECT payee_id, amt, name, date \
                       FROM group_expense \
                       WHERE g_id={group_id};')
    # Personal payments
    data3 = db.execute(f'SELECT u1_id, u2_id, date, amt\
                       FROM payment WHERE g_id={group_id};')

    groupname = db.execute(f'SELECT name FROM p_group WHERE id={group_id};')
    print(groupname)
    groupname = groupname[0][0]

    user_dict = {}
    for (id, name) in data1:
        user_dict[id] = name

    print(data3)

    records = []
    for (payee_id, amt, name, date) in data2:
        date = datetime.datetime.utcfromtimestamp(int(date)).strftime('%b %d, %Y at %H:%2m%p')
        records.append(['expense', date, user_dict[payee_id], name, amt])

    for (id1, id2, date, amt) in data3:
        date = datetime.datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d')
        print(date)
        records.append(['payment', date, user_dict[id1], user_dict[id2], amt])
    
    records.sort(key = lambda a: a[1], reverse= True)
    records = records[:15]

    # remaining_debt = get_compressed_group(group_id)
    print(records)
    print("hello")
    return render_template("/GroupPage/group.html", records = records, id=user_id, 
            groupname=groupname)

@app.route("/ExpenseTrackingPage/expense.html")
def expense_page() -> str:
    id = request.args.get('id')
    events=[]
    data1 = db.execute(f'SELECT p_group.name, group_expense.g_id, group_expense.amt, group_expense.date, group_expense.name \
                       FROM group_expense \
                       INNER JOIN p_group ON p_group.id = group_expense.g_id\
                       INNER JOIN group_participant ON group_participant.g_id = group_expense.g_id\
                       WHERE group_participant.u_id={id};')
    print(data1)
    for data in data1:
        time=datetime.datetime.utcfromtimestamp(int(data[3])).strftime('%m-%d-%Y-%H-%M').split('-')
        content = (data[1],data[0],data[2])
        events.append((time,content,data[4]))
        print("Data: "+data);

    return render_template("/ExpenseTrackingPage/expense.html", id=id,events=events)


@app.route("/DashboardPage/dashboard1.html") 
def dashboard1_page() -> str: 
    user_id = request.args.get('id')
    print("dashboard_1", get_group_info(user_id))
    return render_template("/DashboardPage/dashboard1.html", groups = get_groups(user_id))

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
        return render_template("SignUpPage/signup.html")
    print("Signing up User", user_name, user_phone, user_email, user_passw )
    db.execute(f'INSERT INTO user (name, phone, email, passw) VALUES ( "{user_name}", "{user_phone}", "{user_email}", "{user_passw}");')
    db.db.commit()
    user = db.execute(f'SELECT * FROM user WHERE phone="{user_phone}";')[0]
    currentuserid = user[0]
    return redirect(f"DashboardPage/dashboard.html?id={user[0]}")

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
    currentuserid = user_id
    return redirect(f'DashboardPage/dashboard.html?id={user_id}')    

@app.route("/add_expense", methods = ["POST"])
def add_expense():
    payee_id = request.form["PayeeID"]
    total_amt = int(request.form["Amount"])
    contri_ids = request.form["ContriID"]
    contri_ids = contri_ids.split(',')
    contri_amts = [int((int(total_amt)/len(contri_ids)))] * len(contri_ids)
    contri_amts[-1] += total_amt - sum(contri_amts)
    exp_date = request.form["ExpDate"]
    exp_name = request.form["ExpName"]
    group_id = request.form["GrpID"]

    print(payee_id, total_amt, contri_ids, contri_amts, exp_date, exp_name, group_id)

    db.execute(f'INSERT INTO group_expense (g_id, payee_id, amt, date, name) VALUES ({group_id}, {payee_id}, {total_amt}, {exp_date}, "{exp_name}");')
    db.db.commit()
    exp_id = db.execute(f'SELECT id FROM group_expense WHERE date={exp_date} AND g_id={group_id};')[0][0]
    
    for i, (contri_id, contri_amt) in enumerate(zip(contri_ids, contri_amts)): 
        db.execute(f'INSERT INTO expense_contri (e_id, u_id, amt) VALUES ({exp_id}, {contri_id}, {contri_amt});')
    db.db.commit()
    return "OK", 200

@app.route("/add_payment", methods = ["POST"])
def add_payment():
    u1_id = request.form["usr1ID"]
    u2_id = request.form["usr2ID"]
    total_amt = request.form["amount"]
    paym_date = request.form["PayDate"]
    group_id = request.form["GrpID"]
    print(u1_id, u2_id, total_amt, paym_date, group_id)
    db.execute(f'INSERT INTO payment (u1_id, u2_id, amt, date, g_id) VALUES ({u1_id}, {u2_id}, {total_amt}, {group_id}, {paym_date});')
    db.db.commit()
    return "OK", 200

@app.route("/add_to_group", methods = ["POST"])
def add_to_group():
    user_phone = request.form["user_phone"]
    group_id = request.form["group_id"]
    data = db.execute(f'SELECT id FROM user WHERE phone="{user_phone}";')
    if len(data==0):
        return
    user_id = data[0][0] 
    db.execute(f"INSERT INTO group_participant (u_id, g_id) VALUES ({user_id}, {group_id});")
    db.db.commit()

@app.route("/add_grp",methods=["POST"])
def add_grp():
    group_name=request.form["GrpName"]
    mbr_contacts = request.form['MemContact'].split(',')
    print("Adding Group ", group_name)
    db.execute(f'INSERT INTO p_group(name) VALUES ("{group_name}");')
    group_id = db.execute(f'SELECT id FROM p_group WHERE name="{group_name}";')[0][0]
    for contact in mbr_contacts:
        user_id = db.execute(f'SELECT id FROM user WHERE phone="{contact}"' )[0][0]
        db.execute(f"INSERT INTO group_participant (u_id, g_id) VALUES ({user_id}, {group_id});")
    db.db.commit()
    return "OK", 200

@app.route("/get_group_participant", methods = ["POST"])
def get_group_participant():
    user_id = request.args.get["group_id"]
    data1 = db.execute(f'SELECT id, name FROM user;')
    user_dict = {}
    for id, name in data1:
        user_dict[id] = name


if __name__ == "__main__": 
    app.run(debug=True)
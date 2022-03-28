import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='19216811',
        database='emeraldchat',
        charset='utf8mb4'
    )


def db_update(id, name, username, message, room, action, timestamp):
    if not message:
        message = 'None'
    id = str(id)
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (id,name,username,message,room,action,timestamp) VALUES (%(id)s,%(name)s,%(username)s,%(message)s,%(room)s,%(action)s,%(timestamp)s)",
                   {'id': id, 'name': name, 'username': username, 'message': message, 'room': room, 'action': action, 'timestamp': timestamp}) 
    db.commit()
    db.close()


def regex_query(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"""SELECT DISTINCT * FROM users WHERE name REGEXP '^{name}' GROUP BY ID""")
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute(
        f"""SELECT DISTINCT * FROM users WHERE username REGEXP '^{name}' GROUP BY ID""")
        result = cursor.fetchall()
    db.close()
    print(result)
    return result


def get_id(id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM users WHERE id = '""" + id + """'""")
    result = cursor.fetchall()
    db.close()
    return result

def return_name(id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"""SELECT name, username FROM users WHERE id = {id}""")
    result = cursor.fetchall()
    db.close()
    #print(result)
    if len(result[0][0]) >= 3:
        return result[0][0]
    return f"{result[0][0]} (#{result[0][1]})"

def get_last_record_id(id, only_wfaf):
    db = connect_db()
    cursor = db.cursor()
    if only_wfaf:
        cursor.execute(
            f"""SELECT * FROM users where id = {id} and room = 'WFAF' ORDER BY timestamp DESC LIMIT 1""")
    else:
        cursor.execute(
            f"""SELECT * FROM users where id = {id} ORDER BY timestamp DESC LIMIT 1""")
    result = cursor.fetchall()
    db.close()
    try:
        return result[0]
    except:
        return None

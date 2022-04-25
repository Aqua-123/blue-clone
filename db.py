import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='19216811',
        database='emeraldchat',
        charset='utf8mb4'
    )

def query_runner(query):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result
    
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
    query = f"""SELECT DISTINCT * FROM users WHERE name REGEXP '^{name}' GROUP BY ID"""
    result = query_runner(query)
    if len(result) == 0:
        query = f"""SELECT DISTINCT * FROM users WHERE username REGEXP '^{name}' GROUP BY ID"""
        result = query_runner(query)
    return result


def get_id(id):
    query = "SELECT * FROM users WHERE id = '" + id + "'"
    return query_runner(query)

def return_name(id):
    query = f"""SELECT name, username FROM users WHERE id = {id}"""
    result = query_runner(query)
    if len(result[0][0]) >= 3:
        return result[0][0]
    return f"{result[0][0]} (#{result[0][1]})"

def get_last_record_id(id, only_wfaf):
    if only_wfaf:
        query =  f"""SELECT * FROM users where id = {id} and room = 'WFAF' ORDER BY timestamp DESC LIMIT 1"""
    else:
        query = f"""SELECT * FROM users where id = {id} ORDER BY timestamp DESC LIMIT 1"""
    result = query_runner(query)
    try:
        return result[0]
    except:
        return None

def get_all_messages():
    query = """SELECT message FROM users where message != 'None' ORDER BY room"""
    return query_runner(query)
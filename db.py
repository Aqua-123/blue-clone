import mysql.connector
import time

def connect_db():
    return mysql.connector.connect(host='localhost',
                                   user='root',
                                   passwd='19216811',
                                   database='emeraldchat',
                                   charset='utf8mb4')


def query_runner(query):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result

def rec_without_wfaf(id):
    query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen where id = {id} and room != 'WFAF'"""
    return query_runner(query)

def rec_with_wfaf(id):
    query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen where id = {id} and room = 'WFAF'"""
    return query_runner(query)

def db_update(id, name, username, message, room, action, timestamp):
    start = time.perf_counter()
    if not message:
        message = 'None'
    id = str(id)
    db = connect_db()
    cursor = db.cursor()
    data = {
            'id': id,
            'name': name,
            'username': username,
            'message': message,
            'room': room,
            'action': action,
            'timestamp': timestamp
        }
    cursor.execute(
        "INSERT INTO all_log (id,name,username,message,room,action,timestamp) VALUES (%(id)s,%(name)s,%(username)s,%(message)s,%(room)s,%(action)s,%(timestamp)s)",
        data)
    cursor.execute(
        "INSERT INTO latest_seen (id,name,username,message,room,action,timestamp) VALUES (%(id)s,%(name)s,%(username)s,%(message)s,%(room)s,%(action)s,%(timestamp)s)",
        data)
    db.commit()
    db.close()
    end = time.perf_counter()


def regex_query(name, db_name = 'latest_seen'):
    query = f"""SELECT DISTINCT id, name, username, message, room, action, timestamp FROM {db_name} WHERE name REGEXP '^{name}' GROUP BY ID"""
    result = query_runner(query)
    if len(result) == 0:
        query = f"""SELECT DISTINCT id, name, username, message, room, action, timestamp FROM {db_name} WHERE username REGEXP '^{name}' GROUP BY ID"""
        result = query_runner(query)
    return result


def get_id(id):
    query = "SELECT id, name, username, message, room, action, timestamp FROM latest_seen WHERE id = '" + id + "' LIMIT 1"
    return query_runner(query)


def return_name(id):
    query = f"""SELECT name, username FROM latest_seen WHERE id = {id} ORDER BY unique_key DESC LIMIT 1"""
    result = query_runner(query)
    if len(result[0][0]) >= 3:
        return result[0][0]
    return f"{result[0][0]} (#{result[0][1]})"


def get_last_record_id(id, only_wfaf):
    if only_wfaf:
        query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen where id = {id} and room = 'WFAF' ORDER BY unique_key DESC LIMIT 1"""
    else:
        query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen where id = {id} ORDER BY unique_key DESC LIMIT 1"""
    result = query_runner(query)
    try:
        return result[0]
    except:
        return None


def get_all_messages():
    query = """SELECT message FROM latest_seen where message != 'None' ORDER BY room"""
    return query_runner(query)

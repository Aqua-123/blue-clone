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
    query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen2 where id = {id} and room != 'WFAF'"""
    return query_runner(query)


def rec_with_wfaf(id):
    query = f"""SELECT id, name, username, message, room, action, timestamp FROM latest_seen2 where id = {id} and room = 'WFAF'"""
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
        "INSERT INTO latest_seen2 (id,name,username,message,room,action,timestamp) VALUES (%(id)s,%(name)s,%(username)s,%(message)s,%(room)s,%(action)s,%(timestamp)s)",
        data)
    db.commit()
    db.close()
    end = time.perf_counter()


def regex_query(name, db_name='latest_seen2'):
    start = time.perf_counter()
    # query = f"""SELECT DISTINCT id, name, username, message, room, action, timestamp FROM {db_name} WHERE concat (name,username) REGEXP '^{name}' Group by id"""
    query = f"""SELECT distinct id, name, username FROM {db_name} WHERE match(name, username) against('"{name}"+') Group by id"""
    result = query_runner(query)
    # if not result:
    #    query = f"""SELECT DISTINCT id, name, username FROM {db_name} WHERE username like '{name}%' Group by id"""
    #    result = query_runner(query)
    end = time.perf_counter()
    print(f"Query took {end - start} seconds")
    return result


def get_id(id):
    query = "SELECT id, name, username, message, room, action, timestamp FROM latest_seen2 WHERE id = '" + id + "' LIMIT 1"
    return query_runner(query)


def return_name(id):
    query = f"""SELECT name, username FROM latest_seen2 WHERE id = {id} ORDER BY unique_key DESC LIMIT 1"""
    result = query_runner(query)
    if len(result[0][0]) >= 3:
        return result[0][0]
    return f"{result[0][0]} (#{result[0][1]})"


def get_last_record_id(id, only_wfaf):
    start = time.perf_counter()
    if only_wfaf:
        query = f"""SELECT timestamp FROM latest_seen2 where unique_key = (SELECT MAX(unique_key) FROM latest_seen2 where id = {id} and room = 'WFAF')"""
    else:
        query = f"""SELECT id, name, username, room, timestamp FROM latest_seen2 where unique_key = (SELECT MAX(unique_key) FROM latest_seen2 where id = {id})"""
    result = query_runner(query)
    end = time.perf_counter()
    print(f"Query took {end - start} seconds")
    try:
        return result[0]
    except BaseException:
        return None


def get_all_messages():
    query = """SELECT message FROM latest_seen2 where message != 'None' ORDER BY room"""
    return query_runner(query)

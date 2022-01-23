from flask import Flask
from flask import request
from db import connection_database
from redis_local import get_connection
import json
import sys

app = Flask(__name__)



redis = get_connection()

if redis == -1:
    print("REDIS CONNECTION FAILED")
    sys.exit(-1)


def  check_db(db_conn):
    if db_conn == -1:
        print("DATABASE CONNECTION FAILED")
        sys.exit(-1)


sql_shrani = "INSERT INTO data (name, proga, score, scoreNumeric) values (%s, %s, %s, %s)"
sql_pridobi = "SELECT * FROM data "
sql_pridobi_id = "SELECT * FROM data WHERE id = %s"
sql_delete_id = "DELETE FROM data WHERE id = %s"
sql_delete_all = "DELETE FROM data WHERE 1=1"

@app.route("/shrani",methods=['POST'])
def shrani_podatek():

    data = request.json
    try:
        args = (data['name'],data['proga'],data['score'], data['scoreNumeric'])
    except:
        return 'data is malformed or not complete'
    if data != None:
        database = connection_database()
        check_db(database)
        cursor = database.cursor()
        print(args)
        cursor.execute(sql_shrani,args)
        database.commit()
        # print(podatki_leaderboard)
        cursor.close()
        database.close()
        return 'OK'
    else:
        return 'FAILED Something went wrong! data is None'


@app.route("/pridobi",methods=['GET'])
def pridobi_podatke():
    database = connection_database()
    check_db(database)

    cursor = database.cursor()
    cursor.execute(sql_pridobi)
    data = cursor.fetchall()
    cursor.close()
    database.close()
    if data == None:
        return "404"

    print(data)
    for e in data:
        if not redis.exists(e[0]):
            redis.set(e[0],json.dumps(list(e)))
            redis.expire(e[0], 60)
    return json.dumps(list(data))

@app.route("/pridobi/<get_id>",methods=['GET'])
def pridobi_podatek(get_id):
    if redis.exists(get_id):
        return redis.get(get_id)
    else:    
        database = connection_database()
        check_db(database)

        cursor = database.cursor()

        args = tuple([int(get_id)])
        print(args)
        cursor.execute(sql_pridobi_id,args)
        data = cursor.fetchone()
        cursor.close()
        database.close()
        if data == None:
            return "404"
        redis.set(data[0],json.dumps(list(data)))
        redis.expire(data[0], 60)
        return json.dumps(data)

@app.route("/delete/<delete_id>",methods=['DELETE'])
def delete_id(delete_id):
    args = tuple([int(delete_id)])
    try:
        database = connection_database()
        check_db(database)

        cursor = database.cursor()

        cursor.execute(sql_delete_id,args)
        database.commit()
        redis.delete(delete_id)
        cursor.close()
        database.close()
        return 'OK'
    except:
        return 'FAILED try catch -> ni idja al pa ni podatka s tem idjem'
    return "FAILED!"


@app.route('/nuke',methods=['DELETE'])
def nuke():
    database = connection_database()
    check_db(database)
    cursor = database.cursor()
    cursor.execute(sql_delete_all)
    database.commit()
    redis.flushdb()
    cursor.close()
    database.close()
    return "OK"



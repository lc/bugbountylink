import pymysql
import random
import string

stringList = string.ascii_letters + string.digits


class db:
    host = "127.0.0.1"
    user = "bugbountylink"
    password = "<PASSWORD>"
    db = "bugbountylink"


def dbconnect():
    connection = pymysql.connect(host=db.host, user=db.user, password=db.password,
                                 db=db.db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


def generateLink():
    new = True

    while(new):
        generatedID = ''.join(random.sample(stringList, 6))
        if(canCreate(generatedID) == True):
            new = False
    return(generatedID)


def canCreate(id):
    # check if the id exists yet or not
    # preventing collisions in db
    conn = dbconnect()
    sql = "SELECT count(*) FROM links WHERE id = %s"
    with conn.cursor() as cursor:
        cursor.execute(sql, (id,))
        res = cursor.fetchone()
        conn.close()
        if res['count(*)'] > 0:
            return(False)
        else:
            return(True)

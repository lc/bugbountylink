import pymysql
import random
import string

stringList = string.ascii_letters + string.digits

class db:
    host = "127.0.0.1"
    user = "bugbountylink"
    password = "bugbountylink123!"
    db = "bugbountylink"


def dbconnect():
    connection = pymysql.connect(host=db.host, user=db.user, password=db.password,
                                 db=db.db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


def insertLink(domain):
    count = 0
    success = False
    conn = dbconnect()
    while(success is False and count < 3):
        try:
            generatedID = ''.join(random.sample(stringList, 12))
            add = "INSERT INTO links (id,dest) VALUES (%s,%s);"
            with conn.cursor() as cursor:
                cursor.execute(add, (generatedID, domain))
                conn.commit()
                success = True
        except pymysql.IntegrityError:
            count += 1

    return generatedID if success else None



def rick():
    conn = dbconnect()
    add = "INSERT INTO links (id,dest) VALUES ('admin','https://www.youtube.com/watch?v=dQw4w9WgXcQ');"
    with conn.cursor() as cursor:
        cursor.execute(add)
        conn.commit()
        print("rick roll the hackerz")

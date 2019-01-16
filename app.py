from flask import Flask, render_template, request, json, redirect
import random
import pymysql
import config

app = Flask(__name__)

config.generateLink()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=["POST"])
def genLink():
    if(request.method == 'POST'):
        linkId = config.generateLink()
        domain = request.form['link']
        conn = config.dbconnect()
        add = "INSERT INTO links (id,dest) VALUES (%s,%s);"
        with conn.cursor() as cursor:
            cursor.execute(add, (linkId, domain))
            conn.commit()
        return render_template("default.html", html="<p>Shortened link: <a href='/"+linkId+"'>http://bugbounty.link/"+linkId+"</a></h2 >")
    if(request.method == 'GET'):
        return redirect("/", code=302)


@app.route('/<link>')
def linkage(link):
    conn = config.dbconnect()
    getLink = "SELECT dest FROM links WHERE id = %s;"
    with conn.cursor() as cursor:
        cursor.execute(getLink, (link,))
        res = cursor.fetchone()
        conn.close()
    if(res is None):
        return redirect('/', code=302)
    else:
        destination = res['dest']
        return redirect(destination, code=302)


if __name__ == '__main__':
    app.run()

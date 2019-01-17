from flask import Flask, render_template, request, json, redirect
import random
import pymysql
import config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=["GET", "POST"])
def genLink():
    if(request.method == 'POST'):
        domain = request.form['link']
        response = config.insertLink(domain)
        return render_template("default.html", html="<p>"+response+"</p>")
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

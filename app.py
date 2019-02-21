
from flask import Flask, render_template, request, json, redirect
from rate_limiting import get_ip, rate_limit, record_link_event

import config
import pymysql
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=["GET", "POST"])
@rate_limit
def genLink():
    if(request.method == 'POST'):
        domain = request.form['link']
        generatedID = config.insertLink(domain)

        if generatedID is None:
            response = "Sorry we encountered an error!"
        else:
            record_link_event(generatedID)
            response = "Shortened link: <a href='/"+generatedID+"'>http://bugbounty.link/"+generatedID+"</a>"

        return render_template("default.html", html="<p>"+response+"</p>")
    if(request.method == 'GET'):
        return redirect("/", code=302)


@app.route('/<link>')
@rate_limit
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
        record_link_event(link)
        destination = res['dest']
        return redirect(destination, code=302)


if __name__ == '__main__':
    app.run()

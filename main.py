#!/usr/bin/python3

import os
import secrets
from flask import Flask, request, redirect, url_for, render_template, session
from flask_bootstrap5 import Bootstrap
from flask_session import Session
from prepare_info import get_information, strip_html, get_clean_data 
from forms import searchForm

app = Flask(__name__)  # Pass __name__ here

# create temp folder to store the session
os.makedirs("temp_session", exist_ok=True)

app.secret_key = secrets.token_hex(16)

Bootstrap(app)

# store temporary data using a session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.abspath("temp_session")
app.config['SESSION_PERMANENT'] = False

# Initialises a session
Session(app)

#...................... Route logics......................
@app.route("/", methods=["GET", "POST"])
def home():
    form = searchForm()
    if form.validate_on_submit():
        # Get form data
        name = form.name.data
        age = form.age.data
        sex = form.sex.data
        pregnant = form.pregnant.data
        sexually_active = form.sexually_active.data
        health_issue = form.health_issue.data
        params = {
            "age": age,
            "sex": sex,
            "pregnant": pregnant,
            "sexually active": sexually_active,
            "tobaccouse": health_issue
        }
        api_url = url = "https://odphp.health.gov/myhealthfinder/api/v4/myhealthfinder.json"
        data = get_information(url=api_url, params=params)
        clean_data = strip_html(data=data)
        api_response = get_clean_data(clean_data=clean_data)
        session["api_response"] = api_response
        return redirect(url_for("get_infos"))
    return render_template("index.html", form=form)

@app.route("/get_infos", methods=["GET"])
def get_infos():
    # Get the response or default to empty lists
    api_response = session.get("api_response", None)

    if not api_response or not isinstance(api_response, (tuple, list)) or len(api_response) != 3:
        titles, subtitles, contents= [], [], []
    else:
        titles, subtitles, contents = api_response

    info_items = zip(titles, subtitles, contents)
    return render_template("info.html", info_items=info_items)

@app.route("/article/<title>/<subtitle>")
def read_article(title, subtitle):
    api_response = session.get("api_response", ([], [], []))
    titles, subtitles, contents = api_response

    matched_content = ""
    # Find the index where both title and subtitle match
    for i, (t, s) in enumerate(zip(titles, subtitles)):
        if t == title and s == subtitle:
            matched_content = contents[i]
            break

    return render_template("article.html", title=title, subtitle=subtitle, content=matched_content)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

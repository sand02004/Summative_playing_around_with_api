#!/usr/bin/python3

from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)  # Pass __name__ here

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        age = request.form.get("age")
        sex = request.form.get("sex")
        pregnant = request.form.get("pregnant")
        sexually_active = request.form.get("sexual_activity")
        health_issue = request.form.get("health_issues")
        print(name)
        return redirect(url_for("get_infos"))
    return render_template("index.html")

@app.route("/get_infos")
def get_infos():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

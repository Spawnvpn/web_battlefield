from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/<id>", methods=["GET", "POST"])
def index(id):
    name = request.args.get("name")
    return render_template("index.html", name=name)
import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from bson.objectid import ObjectId
from pymongo import MongoClient


app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client["ipa2026_db"]  # dictionary calling
collection = db["routers"]

# data = [] //No more list in the memory -> instead we use mongo


@app.route("/")
def main():
    data = list(collection.find())
    return render_template("index.html", data=data)


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        collection.insert_one({"ip": ip, "username":
        username,
        "password": password})
        # data.append({"ip": ip, "username": username, "password": password})
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete_comment():
    # try:
    #     idx = int(request.form.get("idx"))
    #     if 0 <= idx < len(data):
    #         data.pop(idx)
    # except Exception:
    #     pass
    try:
        doc_id = request.form.get("idx")
        if doc_id:
            collection.delete_one({"_id": ObjectId(doc_id)})
    except Exception as e:
        print(f"Error: {e}")
    return redirect(
        url_for("main")
    )  # url_for will look for the path of main() function


@app.route("/router-detail/<router_id>")
def router_detail(router_id):
    data = collection.find_one({"_id": ObjectId(router_id)})
    if data:  # change the _id (ObjectId) to string
        data["_id"] = str(data["_id"])
    return render_template("router-detail.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

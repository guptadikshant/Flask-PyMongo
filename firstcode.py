import flask
from flask.templating import render_template
from flask_pymongo import PyMongo
from pymongo.errors import BulkWriteError


app = flask.Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/dikshant"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route("/add_one")
def add_one():
    record1 = {
    "_id":10,
    "name" : "Saranyaa",
    "phone" : 3542,
    "Company" : "Wipro",
    "Salary" : 60000
                }
    db.productdetails.insert_one(record1)
    return flask.jsonify(message="success")

@app.route("/add_many")
def add_many():
    try:
        todo_many = db.todos.insert_many([
            {'_id': 1, 'title': "todo title one ", 'body': "todo body one "},
            {'_id': 8, 'title': "todo title two", 'body': "todo body two"},
            {'_id': 2, 'title': "todo title three", 'body': "todo body three"},
            {'_id': 9, 'title': "todo title four", 'body': "todo body four"},
            {'_id': 10, 'title': "todo title five", 'body': "todo body five"},
            {'_id': 5, 'title': "todo title six", 'body': "todo body six"},
        ], ordered=False)
    except BulkWriteError as e:
        return flask.jsonify(message="duplicates encountered and ignored",
                             details=e.details,
                             inserted=e.details['nInserted'],
                             duplicates=[x['op'] for x in e.details['writeErrors']])

    return flask.jsonify(message="success", insertedIds=todo_many.inserted_ids)

@app.route("/")
def home():
    return "<h1>Welcome</h1>"

@app.route("/get_todo/<int:id>")
def insert_one(id):
    todo = db.productdetails.find_one({"_id": id})
    return todo

@app.route("/uploads", methods=["GET","POST"])
def save_upload():
    if flask.request.method == "POST":
        file = flask.request.files["file"]
        db.save_file(file.filename)
        return "<h1>file saved fine!!</h1>"
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
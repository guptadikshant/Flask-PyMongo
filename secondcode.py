from flask import Flask, request, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dikshant"
mongo = PyMongo(app)

#Configuring collection name we are going to work with
#db_operations = mongo.db.<COLLECTION_NAME>
db_operations = mongo.db.users


@app.route('/',methods=["GET","POST"])
def index():
    return render_template("home.html")

@app.route('/save-file', methods=['POST'])
def save_file():
    if 'new_file' in request.files:
        new_file = request.files['new_file']
        mongo.save_file(new_file.filename, new_file)
        data = {'File Name' : new_file.filename}
        db_operations.insert(data)
    return render_template("index.html")

@app.route('/retrieve-file/<name>')
def retrieve_file(name):
    return mongo.send_file(name)

if __name__ == "__main__":
    app.run(debug=True)

from types import MethodDescriptorType
from flask import Flask, request, render_template, jsonify
from flask.globals import current_app

from db_instance import DBInstance


# Instantiate flask app
app = Flask(__name__)

# Basic config for flask app
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "my-secret-key"
app.config["SESSION_TYPE"] = "filesystem"


def get_success_dict(success_message):
    return {"icon": "success", "title": "Success", "text": success_message}

def get_success_dict_with_redict(success_message, url):
    success_dict = get_success_dict(success_message)
    success_dict["url"] = url

    return success_dict

def get_error_dict(error_message):
    return {"icon": "error", "title": "Error", "text": error_message}


@app.route("/", methods=["GET"])
def index():

    if request.method == "GET":
        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM deadlines ORDER BY deadline")

        return jsonify({"deadlines": cursor.fetchall()})

@app.route("/add-deadline", methods=['GET', 'POST'])
def add_deadline():

    if request.method == "GET":
        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM subjects")
        subject_names = cursor.fetchall()
        subject_names = [subject_name[0] for subject_name in subject_names]

        return render_template("add-deadline.html", subject_names=subject_names)
    elif request.method == "POST":
        task = request.form.get("task")
        subject_name = request.form.get("subject_name")
        type = request.form.get("type")
        deadline = request.form.get("deadline")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute(f"""SELECT * FROM deadlines WHERE task = '{task}' AND name = '{subject_name}'""")
        cursor.fetchall()

        if cursor.rowcount > 0:
            return jsonify(get_error_dict("Deadline already exists!"))

        try:
            cursor.execute(f"""INSERT INTO deadlines (task, name, type, deadline) VALUES(
                            '{task}', '{subject_name}', '{type}', '{deadline}')""")
            db.commit()
        except Exception as e:
            print(e)
            return jsonify(get_error_dict("Error adding deadline!"))

        return jsonify(get_success_dict_with_redict("Deadline added successfully!", "/"))

@app.route("/add-subject", methods=['GET', 'POST'])
def add_subject():

    if request.method == "GET":
        return render_template("add-subject.html")
    elif request.method == "POST":
        subject_name = request.form.get("subject_name")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM subjects WHERE name='{subject_name}'")
        cursor.fetchall()

        if(cursor.rowcount > 0):
            return jsonify(get_error_dict("Subject already exists!"))

        try:
            cursor.execute(f"INSERT INTO subjects (name) VALUES ('{subject_name}')")
            db.commit()
        except:
            return jsonify(get_error_dict("Error adding subject!"))

        return jsonify(get_success_dict_with_redict("Subject added successfully!", "/"))

@app.route("/remove-subject", methods=['GET', 'POST'])
def remove_subject():

    if request.method == 'GET':
        db = DBInstance.get_instance()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM subjects")
        except:
            return jsonify(get_error_dict("Error getting subjects!"))

        subject_names = cursor.fetchall()
        subject_names = [subject_name[0] for subject_name in subject_names]

        return render_template("remove-subject.html", subject_names=subject_names)
    elif request.method == 'POST':
        subject_name = request.form.get("subject_name")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        try:
            cursor.execute(f"DELETE FROM subjects WHERE name='{subject_name}'")
            db.commit()
        except:
            return jsonify(get_error_dict("Error removing subject!"))

        return jsonify(get_success_dict_with_redict("Subject removed successfully!", "/"))

if __name__ == "__main__":
    app.run(debug=True)
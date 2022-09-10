from flask import Flask, json, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime

from .db_instance import DBInstance


# Instantiate flask app
app = Flask(__name__)
CORS(app, support_credentials=True)

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


def get_day_difference(date):
    today = datetime.today().strftime("%Y-%m-%d")

    today = datetime.strptime(today, "%Y-%m-%d")
    date = datetime.strptime(date, "%Y-%m-%d")

    return (date - today).days


def get_error_dict(error_message):
    return {"icon": "error", "title": "Error", "text": error_message}


def get_deadlines_from_db():
    db = DBInstance.get_instance()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM deadlines ORDER BY deadline")
    deadlines = cursor.fetchall()
    deadlines = [
        {
            "task": deadline[0],
            "subject": deadline[1],
            "type": deadline[2],
            "deadline": deadline[3],
            "days_left": get_day_difference(deadline[3]),
        }
        for deadline in deadlines
        if get_day_difference(deadline[3]) >= 0
    ]

    return deadlines


@app.route("/", methods=["GET"])
def index():

    if request.method == "GET":
        return render_template("index.html", deadlines=get_deadlines_from_db())


@app.route("/get-deadlines", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_deadlines():

    if request.method == "GET":
        return jsonify(get_deadlines_from_db())


@app.route("/add-deadline", methods=["GET", "POST"])
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

        cursor.execute(
            f"""SELECT * FROM deadlines WHERE task = '{task}' AND name = '{subject_name}'"""
        )
        cursor.fetchall()

        if cursor.rowcount > 0:
            return jsonify(get_error_dict("Deadline already exists!"))

        try:
            cursor.execute(
                f"""INSERT INTO deadlines (task, name, type, deadline) VALUES(
                            '{task}', '{subject_name}', '{type}', '{deadline}')"""
            )
            db.commit()
        except Exception as e:
            print(e)
            return jsonify(get_error_dict("Error adding deadline!"))

        return jsonify(
            get_success_dict_with_redict("Deadline added successfully!", "/")
        )


@app.route("/remove-deadline", methods=["GET", "POST"])
def remove_deadline():

    if request.method == "GET":
        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM deadlines ORDER BY deadline")
        deadlines = cursor.fetchall()
        tasks = [
            deadline[0]
            for deadline in deadlines
            if get_day_difference(deadline[3]) >= 0
        ]
        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()
        subjects = list(set([subject[0] for subject in subjects]))

        return render_template("remove-deadline.html", subjects=subjects, tasks=tasks)
    elif request.method == "POST":
        task = request.form.get("task")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute(f"""SELECT * FROM deadlines WHERE task = '{task}'""")
        cursor.fetchall()

        if cursor.rowcount == 0:
            return jsonify(get_error_dict("Deadline does not exist!"))

        try:
            cursor.execute(f"""DELETE FROM deadlines WHERE task = '{task}'""")
            db.commit()
        except Exception as e:
            print(e)
            return jsonify(get_error_dict("Error removing deadline!"))

        return jsonify(
            get_success_dict_with_redict("Deadline removed successfully!", "/")
        )


@app.route("/add-subject", methods=["GET", "POST"])
def add_subject():

    if request.method == "GET":
        return render_template("add-subject.html")
    elif request.method == "POST":
        subject_name = request.form.get("subject_name")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM subjects WHERE name='{subject_name}'")
        cursor.fetchall()

        if cursor.rowcount > 0:
            return jsonify(get_error_dict("Subject already exists!"))

        try:
            cursor.execute(f"INSERT INTO subjects (name) VALUES ('{subject_name}')")
            db.commit()
        except:
            return jsonify(get_error_dict("Error adding subject!"))

        return jsonify(get_success_dict_with_redict("Subject added successfully!", "/"))


@app.route("/remove-subject", methods=["GET", "POST"])
def remove_subject():

    if request.method == "GET":
        db = DBInstance.get_instance()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM subjects")
        except:
            return jsonify(get_error_dict("Error getting subjects!"))

        subject_names = cursor.fetchall()
        subject_names = [subject_name[0] for subject_name in subject_names]

        return render_template("remove-subject.html", subject_names=subject_names)
    elif request.method == "POST":
        subject_name = request.form.get("subject_name")

        db = DBInstance.get_instance()
        cursor = db.cursor()

        try:
            cursor.execute(f"DELETE FROM subjects WHERE name='{subject_name}'")
            db.commit()
        except:
            return jsonify(get_error_dict("Error removing subject!"))

        return jsonify(
            get_success_dict_with_redict("Subject removed successfully!", "/")
        )


if __name__ == "__main__":
    app.run(debug=True)

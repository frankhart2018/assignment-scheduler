from flask import Flask, request, render_template, jsonify

from db_instance import DBInstance


# Instantiate flask app
app = Flask(__name__)

# Basic config for flask app
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "my-secret-key"
app.config["SESSION_TYPE"] = "filesystem"


def get_success_dict(success_message):
    return {"icon": "success", "title": "Success", "text": success_message}

def get_error_dict(error_message):
    return {"icon": "error", "title": "Error", "text": error_message}

@app.route("/", methods=['GET'])
def index():

    if request.method == "GET":
        db = DBInstance.get_instance()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM subjects")
        subject_names = cursor.fetchall()
        subject_names = [subject_name[0] for subject_name in subject_names]

        return render_template("index.html", subject_names=subject_names)

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

        success_dict = get_success_dict("Subject added successfully!")
        success_dict['url'] = "/"

        return jsonify(success_dict)

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

        success_dict = get_success_dict("Subject removed successfully!")
        success_dict['url'] = "/"

        return jsonify(success_dict)

if __name__ == "__main__":
    app.run(debug=True)
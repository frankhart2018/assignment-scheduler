import sqlite3


existing_db = sqlite3.connect("deadlines.db")
existing_db_cursor = existing_db.cursor()

new_db = sqlite3.connect("deadlines_new.db")
new_db_cursor = new_db.cursor()

with open("asched/static/tables/create_tables.sqlite", "r") as f:
    new_db_cursor.executescript(f.read())

existing_db_cursor.execute("SELECT * FROM subjects")
existing_db_subjects = existing_db_cursor.fetchall()

for subject in existing_db_subjects:
    new_db_cursor.execute(f"INSERT INTO subjects(name) VALUES('{subject[0]}')")
    new_db.commit()

existing_db_cursor.execute("SELECT * FROM deadlines")
existing_db_deadlines = existing_db_cursor.fetchall()

for deadline in existing_db_deadlines:
    new_db_cursor.execute(
        f"""INSERT INTO deadlines(task, name, type, deadline) 
                              VALUES ('{deadline[0]}', '{deadline[1]}', '{deadline[2]}', '{deadline[3]}')"""
    )
    new_db.commit()

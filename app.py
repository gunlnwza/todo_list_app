from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create the database (run once to initialize)
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def task_list():
    tasks = Task.query.all()  # Fetch all tasks from the database
    return render_template("task_list.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_content = request.form.get("task")
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)  # Add task to the database
        db.session.commit()  # Save changes
    return redirect(url_for("task_list"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)  # Find the task by its ID
    if task:
        db.session.delete(task)  # Delete task from the database
        db.session.commit()  # Save changes
    return redirect(url_for("task_list"))

if __name__ == "__main__":
    app.run(debug=True)

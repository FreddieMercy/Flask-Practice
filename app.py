from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # database ops
from datetime import datetime

app = Flask(__name__)  # only referencing this file
# three / (///) means relative path, four / (////) means abs path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    # setup the database
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# decorator of the function right below
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)  # add new data entry
            db.session.commit()  # commit/confirm add this entry
            return redirect('/')  # back to the root page
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    taskToUpdate = Todo.query.get_or_404(id)  # seems like passed by reference
    if request.method == 'POST':
        taskToUpdate.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue when updating your task'
    else:
        return render_template('update.html', task=taskToUpdate)


# __name__ has to be the last one to define
if __name__ == "__main__":
    app.run(debug=True)

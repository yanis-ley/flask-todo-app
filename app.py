from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SECRET_KEY']='LongAndRandomSecretKey'
db = SQLAlchemy(app)

class TodoListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Todo' + str(self.id)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/todos', methods=['GET', 'POST'])
def createTodo():
        if request.method =='POST':
            todo_title = request.form['title']
            new_todo = TodoListItem(title=todo_title)
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/todos')
        else:
            all_todos = TodoListItem.query.all()
            return render_template('todos.html', todos=all_todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo = TodoListItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todos')





















if __name__ == '__main__':
    app.run(debug=True)
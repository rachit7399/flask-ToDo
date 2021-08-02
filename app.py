from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Completed(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Doing(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    completed = Completed.query.all() 
    doing = Doing.query.all()
    return render_template('index.html', allTodo=allTodo, completed=completed, doing=doing)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/complete/<int:sno>')
def complete(sno):
    doing = Doing.query.filter_by(sno=sno).first()
    completed = Completed(title=doing.title, desc=doing.desc)
    db.session.add(completed)
    db.session.delete(doing)
    db.session.commit()
    return redirect("/")

@app.route('/doing/<int:sno>')
def doing(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    doing = Doing(title=todo.title, desc=todo.desc)
    db.session.add(doing)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/back_doing/<int:sno>')
def back_doing(sno):
    complete = Completed.query.filter_by(sno=sno).first()
    doing = Doing(title=complete.title, desc=complete.desc)
    db.session.add(doing)
    db.session.delete(complete)
    db.session.commit()
    return redirect("/")

@app.route('/back_todo/<int:sno>')
def back_todo(sno):
    doing = Doing.query.filter_by(sno=sno).first()
    todo = Todo(title=doing.title, desc=doing.desc)
    db.session.add(todo)
    db.session.delete(doing)
    db.session.commit()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
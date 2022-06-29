from flask import Flask, redirect,render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ToDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key =True)
    title= db.Column(db.String(200),nullable=False)
    desc= db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(request.url)                 
    alltodo=Todo.query.all()    
    return render_template("index.html",alltodo=alltodo)

@app.route("/update/<int:sno>",methods=['POST','GET'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/") 
    todo=Todo.query.filter_by(sno=sno).first()     
    return render_template("update.html",todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactpage")
def contactpage():
    return "Yet to implement contact methods"

@app.route("/show")
def products():
    # alltodo=Todo.query.all()
    # print(alltodo)
    return "This is products Page"


    
    



if __name__== "__main__":
    app.run(debug=True, port = 9000)
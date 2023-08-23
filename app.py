from flask import Flask,render_template,jsonify,redirect,request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key="key"
db.init_app(app)

class TODO(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)

with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def Home():
    if request.method=="POST":

       title=request.form.get("title")
       todo=TODO(title=title)
       db.session.add(todo)
       db.session.commit()
    alltodo=TODO.query.all()
    return render_template("index.html",alltodo=alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):

    todo=TODO.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=="POST":

       title=request.form.get("title")
       todo=TODO.query.filter_by(sno=sno).first()
       todo.title=title
       db.session.add(todo)
       db.session.commit()
       return redirect("/")
    todo=TODO.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)


        


if __name__=="__main__":
    app.run(debug=True)
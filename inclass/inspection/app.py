from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import matplotlib
matplotlib.use('Agg') #allows creation of plots without GUI popup
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Inspection(db.Model):
    """A Model for an Item in the Inspection List

    Args:
        db (_type_): database model

    Returns:
        __repr__: string rep.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<bridge {self.id}>'

@app.route('/', methods=["POST","GET"])
def index():
    """Main page for App

    Returns:
        page: home page
    """
    if request.method == "POST":
        bridge_name = request.form['name']
        new_bridge = Inspection(name=bridge_name)
        try:
            db.session.add(new_bridge)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return f'Error:{e}'
    else:
        bridges = Inspection.query.order_by(Inspection.date_created).all()
        return render_template('index.html',bridges=bridges)

def delete(id):
    """delete an item from the Inspection list

    Args:
        id (int): uuid for each item in the Inspection list

    Returns:
        redirect: delete and return to home
    """
    bridge_to_delete = Inspection.query.get_or_404(id)
    try:
        db.session.delete(bridge_to_delete)
        db.session.commit()  
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    """update an item from the Inspection list

    Args:
        id (int): uuid for each item in the Inspection list

    Returns:
        redirect: update and return to home
    """
    bridge = Inspection.query.get_or_404(id)
    if request.method == "POST":
        bridge.name = request.form['name']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return "Error"
    else:
        return render_template("update.html", bridge=bridge)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://gireesh:1111@localhost:5432/solutionhub"
app.config["SECRET_KEY"]="\xe4dMX!\xa4\xfa\xe2'H\x02\xa1e\xc2\xb97\xff?g\xf3\x97\x03\xd8\xec"

db=SQLAlchemy(app)

class SignUp(db.Model):
    __tablename__="signups"

    signup_id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(length=255))
    last_name=db.Column(db.String(length=255))
    email=db.Column(db.Text)
    password=db.Column(db.Text)
    retype_password=db.Column(db.Text)
    
    m=db.relationship("Login",cascade='all,delete-orphan')

class Login(db.Model):
    __tablename__="logins"

    login_id=db.Column(db.Integer,primary_key=True)
    signup_id=db.Column(db.Integer,db.ForeignKey('signups.signup_id'))
    email=db.Column(db.Text)
    password=db.Column(db.Text)

    s=db.relationship('SignUp')

class Topic(db.Model):
    __tablename__="topics"

    topic_id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(length=255))

    task=db.relationship("Solution",cascade='all,delete-orphan')

class Solution(db.Model):
    __tablename__="solutions"

    solution_id=db.Column(db.Integer,primary_key=True)
    topic_id=db.Column(db.Integer,db.ForeignKey('topics.topic_id'))
    description=db.Column(db.String(length=255))

    topic=db.relationship('Topic')
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/aboutus')
def about():
    return render_template('about_us.html')
@app.route('/login')
def fun():
    return render_template("login.html")
@app.route('/show_topics')
def topics():
    return render_template("topics.html",topics=Topic.query.all())

@app.route('/solution/<topic_id>')
def sol(topic_id):
    return render_template("solutions.html",solutions=Solution.query.filter_by(topic_id=topic_id).all(),topic=Topic.query.filter_by(topic_id=topic_id).first())

@app.route('/add_new_topic',methods=['GET','POST'])
def add_topic():
    if not request.form['q']:
        flash("enter a new topic","tomato")
    else:
        topic=Topic(title=request.form['q'])
        db.session.add(topic)
        db.session.commit()
        flash("Topic added successfully","lawngreen")

    return redirect(url_for('topics'))

@app.route('/add_new_solution/<topic_id>',methods=['GET','POST'])
def add_solution(topic_id):
    if not request.form['s']:
        flash("enter a new solution","tomato")
    else:
        solution=Solution(description=request.form['s'],topic_id=topic_id)
        db.session.add(solution)
        db.session.commit()
        flash("solution added successfully","lawngreen")
    return redirect(url_for('sol',topic_id=topic_id))

@app.route('/delete_solution/<topic_id>/<solution_id>')
def del_sol(topic_id,solution_id):
    k=Solution.query.filter_by(solution_id=solution_id).first()
    db.session.delete(k)
    db.session.commit()

    return redirect(url_for('sol',topic_id=topic_id))

@app.route('/delete_topic/<dt>')
def del_topic(dt):
    a=Topic.query.filter_by(topic_id=dt).first()
    db.session.delete(a)
    db.session.commit()

    return redirect(url_for('topics'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['em']
        password = request.form['ps']

        # Perform the actual login authentication by querying the database.
        user = Login.query.filter_by(email=email).first()

        if user and user.password==password:
            return redirect(url_for('topics'))
        else:
            flash("Invalid email or password.", "tomato")
            return redirect(url_for('login'))

    return render_template("login.html")
@app.route('/signup',methods=['GET','POST'])
def sign():
    if request.method=='POST':
        fn=request.form['fn']
        ln=request.form['ln']
        email=request.form['e']
        passw=request.form['p']
        repass=request.form['rp']

        k=SignUp.query.filter_by(email=email).first()
        if k:
            flash("email already exist","tomato")
        else:
            m=SignUp(first_name=fn,last_name=ln,email=email,password=passw,retype_password=repass)
            if m.password != m.retype_password:
                flash("password doesn't match","tomato")
            else:
                db.session.add(m)
                db.session.commit()
                return redirect(url_for('topics'))
    return render_template("signup.html")
if __name__=="__main__":
    app.run(debug=True)
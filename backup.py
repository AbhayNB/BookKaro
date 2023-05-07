from flask import Flask,render_template,request,flash,session,redirect
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookkaro2.db"
UPLOAD_FOLDER = 'media/'
db = SQLAlchemy(app)
# db.init_app(app)
# app.app_context().push()
app.secret_key = "secret key"
class Venue(db.Model):
    venue_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    location=db.Column(db.String(200),nullable=False)
    place=db.Column(db.String(200),nullable=False)
    capacity=db.Column(db.Integer,nullable=False)
    shows=db.relationship("Shows",secondary="venueshow")
    def __repr__(self) -> str:
        return f"{self.venue_id} - {self.name}"
class Shows(db.Model):
    show_id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    image=db.Column(db.String(200),nullable=False,default='logo.png')
    desc=db.Column(db.String(500),nullable=False)
    release_dt=db.Column(db.String(200),nullable=False)
    rating=db.Column(db.Integer,nullable=True)
    price=db.Column(db.Integer,nullable=False)
    tag=db.Column(db.String(200),nullable=False)
    stock=db.Column(db.Integer,nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.show_id} - {self.title}"
class VenueShow(db.Model):
    __tablename__='venueshow'
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True)
    show_id= db.Column(db.Integer,db.ForeignKey("shows.show_id"),primary_key=True)
    
class User(db.Model):
    uid= db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String(200),nullable=False)
    Email= db.Column(db.String(200),nullable=False)
    Pass= db.Column(db.String(200),nullable=False)
class Admin(db.Model):
    uid= db.Column(db.Integer,primary_key=True)
    Name= db.Column(db.String(200),nullable=False)
    Email= db.Column(db.String(200),nullable=False)
    Pass= db.Column(db.String(200),nullable=False)
    Admin=db.Column(db.String(200),nullable=False,default=True)
@app.route('/create_venue',methods=['GET','POST'])
def create_venue():
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    
    if request.method=='POST':
        vname=request.form['vname']
        loc=request.form['loc']
        capicitty=request.form['cap']
        place=request.form['place']
        newv=Venue(name=vname,location=loc,capacity=capicitty,place=place)
        db.session.add(newv)
        db.session.commit() 
        return 'Venue successfully uploaded <a href="/venueadmin">See all venues</a>'
    return render_template('create_venue.html')
@app.route('/')
def home():
    try:
        if not session['loged_in']:
            return redirect('/login')
    except:
        return redirect('/login')
    
    return render_template('index.html')
@app.route('/<int:slug>/shows/create',methods=['GET','POST'])
def create_show(slug):
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    vid=slug
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        file=request.files['file']
        date=request.form['date']
        price=request.form['price']
        stock=request.form['stock']
        rating=request.form['rating']
        filename = secure_filename(file.filename)
        file.save(os.path.join('media/', filename))
        #print('upload_image filename: ' + filename)
        newm=Shows(title=title,image=filename,desc=desc,release_dt=date,price=price,rating=rating,tag=stock,stock=stock)
        db.session.add(newm)
        db.session.commit()
        newr=VenueShow(venue_id=vid,show_id=Shows.query.all()[-1].show_id)
        db.session.add(newr)
        db.session.commit()
        print(Shows.query.all())
    return render_template('create_show.html',sulg=slug)
@app.route('/login',methods=['GET','POST'])
def login():  
    if request.method=='POST':
        email=request.form['email']
        pw=request.form['pw']
        q=db.session.query(User).filter(User.Email.in_([email]), User.Pass.in_([pw]))
        res=q.first()
        if res:
            session['loged_in']=True
            return redirect('/')
        else:
            return "User Not Found!!!!!!"
    return render_template('login.html')
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        email=request.form['email']
        pw=request.form['pw']
        q=db.session.query(Admin).filter(Admin.Email.in_([email]), Admin.Pass.in_([pw]))
        res=q.first()
        if res:
            session['admin']=True
            session['loged_in']=True
            return redirect('/admin_home')
        else:
            return "User Not Found!!!!!!"
    return render_template('admin_login.html')
@app.route('/register_user',methods=['GET','POST'])
def register_user():
    if request.method=='POST':
        email=request.form['email']
        pw=request.form['pw']
        name=request.form['name']
        newu=User(Name=name,Email=email,Pass=pw)
        db.session.add(newu)
        db.session.commit()
        return redirect('/login')
    return render_template('register_user.html')
@app.route('/register_admin',methods=['GET','POST'])
def register_admin():
    if request.method=='POST':
        email=request.form['email']
        pw=request.form['pw']
        name=request.form['name']
        newu=Admin(Name=name,Email=email,Pass=pw)
        db.session.add(newu)
        db.session.commit()
        return redirect('/admin_home')
    return render_template('register_admin.html')
@app.route('/logout',methods=['GET','POST'])
def logout():
    session['loged_in']=False
    session['admin']=False
    return redirect('/login')
@app.route('/admin_home',methods=['GET','POST'])
def admin_home():
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    return render_template('admin_home.html')
@app.route('/venueadmin',methods=['GET','POST'])
def venueadmin():
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    venue=Venue.query.all()
    return render_template('venues.html',venues=venue)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
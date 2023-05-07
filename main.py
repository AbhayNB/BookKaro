"""
This is basicaly a ticket booking app 

here for making login system i have used sqlalchemy for database and session to make user remain logged in

"""
"""Templates Folder contains all the html files"""
""" Static folder contains all all media files and static files"""
""" instance folder contain database """
""" api.py file contain code for api"""
""" models.py file contain all models """
""" structure:
-Project
--instance
---our database
--static
---media files & static files
--template
---all html files
--api.pt
--main.py
--models.py
--apidoc.yaml

"""
""" Importing Modules """

from flask import Flask,render_template,request,flash,session,redirect
import os
# from models import *
from api import *
from werkzeug.utils import secure_filename

""" configuring app setting """
#==============================================================================
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb2.db"  # created Database
UPLOAD_FOLDER = 'media/' # folder to upload media files
db.init_app(app)
api.init_app(app)
app.app_context().push()
app.secret_key = "secret key"

#=====================================================================================


""" Views & controlls """
""" View and controller for creating venues """
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
""" View and controller for  home page where people can see the shows and venues"""
@app.route('/')
def home():
    try:
        if not session['loged_in']:
            return redirect('/login')
    except:
        return redirect('/login')
    venue=Venue.query.all()
    return render_template('index.html',venues=venue)

""" View and controller for creating shows """
@app.route('/<int:slug>/shows/create',methods=['GET','POST'])
def create_show(slug):
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    vid=slug
    cap=Venue.query.get(vid).capacity

    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        file=request.files['file']
        date=request.form['date']
        price=request.form['price']
        stock=request.form['stock']
        rating=request.form['rating']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/', filename))
        newm=Shows(title=title,image=filename,desc=desc,release_dt=date,price=price,rating=rating,tag=stock,stock=cap,venue_id=vid)
        db.session.add(newm)
        db.session.commit()
        newr=VenueShow(venue_id=vid,show_id=Shows.query.all()[-1].show_id)
        db.session.add(newr)
        db.session.commit()
        return redirect('/venueadmin')
    return render_template('create_show.html',sulg=slug)
""" View and controller for for logging in users """
@app.route('/login',methods=['GET','POST'])
def login():  
    if request.method=='POST':
        email=request.form['email']
        pw=request.form['pw']
        q=db.session.query(User).filter(User.Email.in_([email]), User.Pass.in_([pw]))
        res=q.first()
        if res:
            session['loged_in']=True
            session['uname']=res.Name
            session['uid']=res.uid
            session['email']=res.Email
            return redirect('/')
        else:
            return "User Not Found!!!!!!"
    return render_template('login.html')
""" View and controller for for logging in Admin"""
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
""" View and controller for for registering users """
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

""" View and controller for for registering admin """

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
""" View and controller for logout """

@app.route('/logout',methods=['GET','POST'])
def logout():
    session['loged_in']=False
    session['admin']=False
    return redirect('/login')


""" View and controller for  home of admin"""

@app.route('/admin_home',methods=['GET','POST'])
def admin_home():
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    return render_template('admin_home.html')

""" View and controller for The venue and show management """

@app.route('/venueadmin',methods=['GET','POST'])
def venueadmin():
    try:
        if not session['admin']:
            return redirect('/admin_login')
    except:
        return redirect('/admin_login')
    venue=Venue.query.all()
    return render_template('venues.html',venues=venue)

""" View and controller for deleting shows """

@app.route('/del_show/<int:show_id>/<int:venue_id>',methods=['GET','POST'])
def del_show(show_id,venue_id):
    show=Shows.query.get(show_id)
    vs=VenueShow.query.get((show_id,venue_id))
    if show==None:
        return 'Show Not Found'
    db.session.delete(show)
    db.session.delete(vs)
    db.session.commit()
    return redirect('/venueadmin')

""" View and controller for Editing Shows """

@app.route('/edit_show/<int:show_id>/<int:venue_id>',methods=['GET','POST'])
def edit_show(show_id,venue_id):
    show=Shows.query.get(show_id)
    if show==None:
        return 'show not found'

    if request.method=='POST':
        show.title=request.form['title']
        show.desc=request.form['desc']
        file=request.files['file']
        show.release_dt=request.form['date']
        show.price=request.form['price']
        show.stock=request.form['stock']
        show.rating=request.form['rating']
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/', filename))
        show.image=filename
        db.session.commit()
        return redirect('/venueadmin')
    return render_template('edit_show.html',show=show)

""" View and controller for deleting venue """

@app.route('/del_venue/<int:venue_id>',methods=['GET','POST'])
def del_venue(venue_id):
    venue=Venue.query.get(venue_id)
    vs=VenueShow.query.all()
    if venue==None:
        return 'venue Not Found'
    
    for a in vs:
        if a.venue_id==venue_id:
            db.session.delete(a)
    db.session.delete(venue)
    db.session.commit()
    return redirect('/venueadmin')

""" View and controller for editing venue"""

@app.route('/edit_venue/<int:venue_id>',methods=['GET','POST'])
def edit_venue(venue_id):
    venue=Venue.query.get(venue_id)
    if venue==None:
        return 'venue Not Found'
    if request.method=='POST':
        venue.name=request.form['vname']
        venue.location=request.form['loc']
        venue.capicitty=request.form['cap']
        venue.place=request.form['place']
        db.session.commit()
        return redirect('/venueadmin')
    return render_template('edit_venue.html',venue=venue)

""" View and controller for booking a ticket """

@app.route('/book/<int:show_id>/<int:venue_id>/<int:uid>',methods=['GET','POST'])
def book(show_id,venue_id,uid):
    venue=Venue.query.get(venue_id)
    show=Shows.query.get(show_id)
    vs=VenueShow.query.get((show_id,venue_id))
    user=User.query.get(uid)
    if request.method=='POST':
        seats=request.form['seats']
        if int(show.stock)-int(seats)<0:
            return " Cant book Seat more then available"
        if ShowBooks.query.get((uid,venue_id,show_id)):
            sb=ShowBooks.query.get((uid,venue_id,show_id))
            sb.seats=sb.seats+int(seats)
        else:
            newb=ShowBooks(uid=uid,show_id=show_id,venue_id=venue_id,seats=seats)
            db.session.add(newb)
        
        
        show.stock=show.stock-int(seats)
        db.session.commit()
    return render_template('bookshow.html',show=show,vs=vs,user=user,venue=venue)

""" View and controller for viewing user profile """

@app.route('/user_prof')
def user_prof():
    return render_template('/usel_prof.html')

""" View and controller for viewing shows booked by the user"""
@app.route('/user_prof/<int:uid>')
def booked_show(uid):
    user=User.query.get(uid)
    venue=Venue.query.all()
    return render_template('/booked_shows.html',user=user,venue=venue)

""" View and controller for searching venue and shows """
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        q=request.form['search']
        query="%"+q+"%"
        result1= Venue.query.filter(Venue.name.like(query)).all()
        result2= Shows.query.filter(Shows.title.like(query)).all()
        return render_template('result.html',q=q,venues=result1,shows=result2)
    return redirect('/')
@app.route('/add_to/<int:venue_id>/<int:show_id>',methods=['GET','POST'])
def addto(venue_id,show_id):
    venues=Venue.query.all()
    show=Shows.query.get(show_id)
    if request.method=='POST':
        uvi = request.form.getlist('venue')
        for a in uvi:
            tv=Venue.query.get(int(a))
            newm=Shows(title=show.title,image=show.image,desc=show.desc,release_dt=show.release_dt,price=show.price,rating=show.rating,tag=show.tag,stock=tv.capacity,venue_id=int(a))
            db.session.add(newm)
            db.session.commit()
            newr=VenueShow(venue_id=int(a),show_id=Shows.query.all()[-1].show_id)
            db.session.add(newr)
            db.session.commit()
        return redirect('/venueadmin')
    return render_template('addvenues.html',vid=venue_id,sid=show_id,venues=venues)
@app.route('/venue_detail/<int:venue_id>')
def venue_detail(venue_id):
    venue=Venue.query.get(venue_id)
    return render_template('venuedetail.html',venue=venue)
@app.route('/view_users')
def view_users():
    users=User.query.all()
    return render_template('view_user.html',users=users)
#===============================================================================================================    
""" Main """
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
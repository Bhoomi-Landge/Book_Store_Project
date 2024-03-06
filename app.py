from flask import Flask,render_template,request,redirect,json

from  flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file=f"sqlite:///{os.path.join(project_dir,'mydatabase.db')}"

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file
db=SQLAlchemy(app)

class Book(db.Model):
    name=db.Column(db.String(100),nullable=False,primary_key=True)
    Author=db.Column(db.String(100),nullable=False)
    price=db.Column(db.String(100),nullable=False)
    img_url=db.Column(db.String(100),nullable=False)
    
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(50),default='user')
    
with app.app_context():
    #db.drop_all()
    db.create_all()
@app.route('/')
def home():
    return 'This is a home page'

@app.route('/<user>')
def user(user):
    return render_template('index.html',user=user,isActive=False)

@app.route('/profile/<name>')
def profile(name):
    return '<h1>This is profile of %s<h1>' % name

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/books',methods=['GET','POST'])
def books():
    if request.method=='POST':
        search_query=request.form['search_query']
        if search_query:
             books=Book.query.filter(Book.name.ilike(f"%{search_query}%")| Book.Author.ilike(f"%{search_query}%")).all()
        else:
            books=Book.query.all()
    else:   
        books=Book.query.all()
    return render_template('books.html',books=books)
@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/submitbook',methods=['POST'])
def submitbook():
    name=request.form['name']
    author=request.form['Author']
    price=request.form['price']
    img_url=request.form['img_url']
    book=Book(name=name,Author=author,price=price,img_url=img_url)
    db.session.add(book)
    db.session.commit()
    return redirect ('/books')

@app.route('/updatebooks')
def updatebooks():
    books=Book.query.all()
    
    return render_template('updatebooks.html',books=books)
@app.route('/update',methods=['POST'])
def update():
    newname=request.form['newname']
    oldname=request.form['oldname']
    newAuthor=request.form['newAuthor']

    newprice=request.form['newprice']
    newimg_url=request.form['newimg_url']
    book=Book.query.filter_by(name=oldname).first()
    book.name=newname
    book.author=newAuthor
    book.price=newprice
    book.img_url=newimg_url
    db.session.commit()
    return redirect('/books')

@app.route('/delete', methods=['POST'])
def delete():
    name=request.form['name']
    book= Book.query.filter_by(name=name).first()
    db.session.delete(book)
    db.session.commit()
    
    return redirect('/books')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    
    app.run(debug=True)



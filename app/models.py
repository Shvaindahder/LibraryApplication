from flask_login import UserMixin

from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash


class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True, nullable=False)
    email = db.Column(db.String(40), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_info = db.relationship('UserInfo', uselist=False, backref='user_account')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<UserAccount {}>'.format(self.username)

    def __str__(self):
        return 'Username: {}\nEmail: {}'.format(self.username, self.email)


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, nullable=False)
    surname = db.Column(db.String(50), index=True, nullable=False)
    age = db.Column(db.Integer)
    birthday = db.Column(db.DateTime, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))


@login.user_loader
def load_user(id):
    return UserAccount.query.get(int(id))


book_authors = db.Table('book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user_account.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, nullable=False)
    description = db.Column(db.Text)
    year = db.Column(db.String(4))
    lang = db.Column(db.String(2))
    book_img = db.Column(db.JSON)
    ebook_link = db.Column(db.JSON)
    author = db.relationship(
        'Author', secondary=book_authors,
        backref=db.backref('book', lazy='dynamic'), lazy='dynamic'
    )

    def add_author(self, author):
        self.author.append(author)

    def __repr__(self):
        return '<Book: {}>'.format(self.name)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    f_name = db.Column(db.String(35), nullable=False)

    def __repr__(self):
        return '<Author: {} {}.{}.>'.format(self.surname, self.name[0], self.f_name[0])



from flask import Flask, jsonify, request
from flask_login import UserMixin
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hang:123@localhost:5432/typeracer'
app.secret_key = 'this string need to be changed'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)


class Excerpt(db.Model):
    __tablename__ = 'excerpts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    wpm = db.Column(db.Integer)
    time = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    excerpt_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


db.create_all()


@app.route('/')
def root():
    return jsonify(['Hello', 'World'])


@app.route('/excerpts')
def list():
    excerpts = Excerpt.query.all()
    jsonized_excerpt_objects_list = []
    for excerpt in excerpts:
        jsonized_excerpt_objects_list.append(excerpt.as_dict())

    return jsonify(jsonized_excerpt_objects_list)


@app.route('/scores', methods=['POST'])
def create():
    new_score = Score(wpm=request.get_json()['wpm'],
                      time=request.get_json()['time'],
                      errors=request.get_json()['error_count'],
                      user_id=1,
                      excerpt_id=request.get_json()['excerpt_id'])
    db.session.add(new_score)
    db.session.commit()
    response = jsonify({"code" : 200})
    return response

if __name__ == "__main__":
    app.run(debug=True)

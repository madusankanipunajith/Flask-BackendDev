from flask import Flask
from flask import jsonify , request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# using for serializing or deserializing the data object
ma = Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default= datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body

class AtricleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')

atricle_schema = AtricleSchema()
atricles_schema = AtricleSchema(many=True)

# routes
@app.route('/get', methods=['GET'])
def get_article():
    all_articles = Articles.query.all()
    result = atricles_schema.dump(all_articles)
    return jsonify(result)

@app.route('/get/<id>', methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    result = atricle_schema.dump(article)
    return jsonify(result)

@app.route('/add', methods=['POST'])
def add_atricle():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return atricle_schema.jsonify(articles)

@app.route('/update/<id>', methods=['PUT'])
def update_article(id):
    atricle = Articles.query.get(id)
    title = request.json['title']
    body = request.json['body']

    atricle.title = title
    atricle.body = body

    db.session.commit()
    result = atricle_schema.dump(atricle)
    return jsonify(result)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    result = atricle_schema.dump(article)
    return jsonify(result)


# run the application
if __name__ == "__main__":
    app.run(debug=True)
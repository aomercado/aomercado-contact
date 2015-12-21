from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo
from flask.ext.pymongo import ASCENDING

from localsettings import *


app = Flask(__name__)

app.config['MONGO_DBNAME'] = DBNAME
app.config['MONGO_HOST'] = HOST
app.config['MONGO_PORT'] = PORT
app.config['MONGO_USERNAME'] = USERNAME
app.config['MONGO_PASSWORD'] = PASSWORD
mongo = PyMongo(app, config_prefix='MONGO')

CORS(app, resources={
    r"/contact/*": {
        "origins": [r".*aomercado\.github\.io", r".*aomercado\.com"]
    }
})


@app.route('/contact', methods=['POST'])
def receive_message():
    if not request.json or 'mail' not in request.json:
        abort(400)
    contact = {'mail': request.json['mail']}
    contacts = mongo.db.get_collection('contact')
    if not contacts.find_one({'mail': contact.get('mail')}):
        contacts.insert_one(contact)
    return jsonify({'contact': make_public(contact)}), 201


@app.route('/contact/<mail>', methods=['GET'])
def get_mail(mail):
    contacts = mongo.db.get_collection('contact')
    contact = contacts.find_one({'mail': mail})
    if not contact:
        abort(404)
    return jsonify({'contact': make_public(contact)})


def make_public(contact):
    return {'mail': contact['mail']}

if __name__ == '__main__':
    app.run()

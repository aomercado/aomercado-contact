from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo

from localsettings import DBNAME
from localsettings import HOST
from localsettings import PORT
from localsettings import USERNAME
from localsettings import PASSWORD


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
    },
    r"/market/*": {
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


@app.route('/market', methods=['POST'])
def receive_market():
    if not request.json or 'mail' not in request.json or \
       'name' not in request.json or 'phone' not in request.json or \
       'market' not in request.json or 'message' not in request.json:
        abort(400)
    message = {
        'mail': request.json['mail'],
        'name': request.json['name'],
        'phone': request.json['phone'],
        'market': request.json['market'],
        'message': request.json['message'],
    }
    market_contacts = mongo.db.get_collection('marketcontacts')
    market_contacts.insert_one(message)
    return jsonify({'message': make_public(message)}), 201


@app.route('/market/<mail>', methods=['GET'])
def get_message(mail):
    market_contacts = mongo.db.get_collection('marketcontacts')
    message = market_contacts.find_one({'mail': mail})
    if not message:
        abort(404)
    return jsonify({'message': make_public(message)})


def make_public(contact):
    return {'mail': contact['mail']}

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite3"
db=SQLAlchemy(app)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagid = db.Column(db.String(10), nullable=False)

@app.route('/api/addTag', methods=['POST'])
def addTag():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify({
            'status': '0',
            'message': 'error'
        }), 400

    res_json = request.json
    tagid = res_json['tagid']
    exists = Tag.query.filter_by(tagid=tagid).first()
    if exists is not None:
        return jsonify({
            'status': '2',
            'message': 'already exists'
        })  
    new_item = Tag(tagid=tagid)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        'status': '1',
        'message': 'ok'
    })

@app.route('/api/removeTag', methods=['POST'])
def removeTag():
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return jsonify({
            'status': '0',
            'message': 'error'
        }), 400

    res_json = request.json
    tagid = res_json['tagid']
    exists = Tag.query.filter_by(tagid=tagid).first()
    if exists is None:
        return jsonify({
            'status': '2',
            'message': 'does not exist'
        })  
    
    db.session.delete(exists)
    db.session.commit()

    return jsonify({
        'status': '1',
        'message': 'ok'
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
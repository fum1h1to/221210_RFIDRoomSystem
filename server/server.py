from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from pytz import timezone
from dateutil import parser
import datetime

import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite3"
db=SQLAlchemy(app)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagid = db.Column(db.String(10), nullable=False)
    isEntered = db.Column(db.Boolean, default=False)
    lastEnterTime = db.Column(db.DateTime, nullable=True)
    lastLeaveTime = db.Column(db.DateTime, nullable=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagid = db.Column(db.String(10), nullable=False)
    entering = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

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

@app.route('/api/enter', methods=['POST'])
def enterTag():
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
    
    if exists.isEntered:
        return jsonify({
            'status': '3',
            'message': 'already entered'
        })

    exists.isEntered = True
    exists.lastEnterTime = db.func.now()
    
    new_log = Log(tagid=tagid, entering=True)
    db.session.add(new_log)

    db.session.commit()

    return jsonify({
        'status': '1',
        'message': 'ok'
    })

@app.route('/api/leave', methods=['POST'])
def leaveTag():
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

    if not exists.isEntered:
        return jsonify({
            'status': '3',
            'message': 'already left'
        })
    
    exists.isEntered = False
    exists.lastLeaveTime = db.func.now()

    new_log = Log(tagid=tagid, entering=False)
    db.session.add(new_log)

    db.session.commit()

    return jsonify({
        'status': '1',
        'message': 'ok'
    })

@app.route('/')
def index():
    tags = Tag.query.all()
    return render_template('index.html', tags=tags)

@app.route('/log')
def log():
    logs = Log.query.all()
    return render_template('log.html', logs=logs)


@app.route('/data/graph')
def graph1():
    
    logs = Log.query.all()
    userdict = {}
    dataframe = []
    for log in logs:

        if log.entering:
            userdict[log.tagid] = log.timestamp + datetime.timedelta(hours=9)
        else:
            finish = log.timestamp + datetime.timedelta(hours=9)
            dataframe.append(dict(
                User=log.tagid,
                Date=userdict[log.tagid].strftime('%m-%d'),
                Start=userdict[log.tagid],
                Finish=finish
            ))


    df = pd.DataFrame(dataframe)
    fig = px.timeline(
        df,  # 使用するデータフレーム
        x_start='Start', x_end='Finish',  # 横軸の開始・終了の列名
        y='User',  # 縦軸の列名
    )
    # グラフ全体とホバーのフォントサイズ変更
    fig.update_layout(font_size=20, hoverlabel_font_size=20)
    fig.write_html('templates/graph.html')

    return render_template('graph.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
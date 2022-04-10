import plotly
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import json

app = Flask(__name__)
history = []

def get_plot(data):
    fig = go.Figure()
    if not data:
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.add_trace(go.Box(y=data[0], name='A', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[1], name='B', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[2], name='C', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[3], name='D', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[4], name='F', marker_color='indianred'))
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def get_all_data():
    engine = create_engine('mysql+pymysql://admin:root1234@boxplot.co5oyjgpvi8x.us-east-1.rds.amazonaws.com:3306/boxplot', max_overflow=10)
    base_sql = "select score from moody2022_new where "
    conditions = []
    conditions.append("GRADE = 'A' ")
    conditions.append("GRADE = 'B' ")
    conditions.append("GRADE = 'C' ")
    conditions.append("GRADE = 'D' ")
    conditions.append("GRADE = 'F' ")
    scores = []
    for condition in conditions:
        sql = base_sql + condition
        scores.append(engine.execute(sql).fetchall())
    for score in scores:
        for i in range(len(score)):
            score[i] = float(score[i][0])
    return scores


def get_query_data(s):
    if not s:
        return[]
    engine = create_engine('mysql+pymysql://admin:root1234@boxplot.co5oyjgpvi8x.us-east-1.rds.amazonaws.com:3306/boxplot', max_overflow=10)
    s = s.lower()
    first_condition = " where "
    base_sql = "select score from moody2022_new "
    for i in range(len(s) - 5):
        if (s[i:i + 5] == 'where'):
            first_condition = s[i:]
    condition = "GRADE = '"
    grades = ['A', 'B', 'C', 'D', 'F']
    if first_condition == " where ":
        return []
    scores = []
    i = 0
    while i < len(first_condition):
        if first_condition[i:i + 5] == 'where':
            break
    str_list = list(first_condition)
    str_list.insert(i + 5, '(')
    str_list.append(') ')
    first_condition = (''.join(str_list))

    for i in range(5):
        sql = base_sql + first_condition + ' and ' + condition + grades[i] + "'"
        scores.append(engine.execute(sql).fetchall())
    for score in scores:
        for i in range(len(score)):
            score[i] = float(score[i][0])
    return scores

@app.route("/", methods=['GET'])
def welcome():
    return render_template("welcome.html")

@app.route("/index", methods=['POST', 'GET'])
def start():
    try:
        s = request.form.get("sql_query")
        history.append(s)
        if len(history) > 20:
            del history[0]
        data = get_all_data()
        query_data = get_query_data(s)
        return render_template('index.html', graph1=get_plot(data), graph2=get_plot(query_data))
    except:
        return render_template('fail.html')

@app.route("/history", methods=['POST', 'GET'])
def queryHistory():
    return render_template('history.html', his = history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


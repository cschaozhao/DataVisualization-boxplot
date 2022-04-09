import plotly
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import json

app = Flask(__name__)


# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/boxplot'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#
#
# app.config.from_object(Config)
# db = SQLAlchemy(app)
#
# class Moody(db.Model):
#     __tablename__ = 'moody2022'
#     score = db.Column(db.Float, primary_key=True)
#     grade = db.Column(db.String)
#     dozes_off = db.Column(db.String)
#     texting_in_class = db.Column(db.String)
#     participation = db.Column(db.Float)
#
# def get_data():
#     try:
#         socks = Moody.query.filter_by(dozes_off='never').order_by(Moody.score).all()
#
#         return
#     except Exception as e:
#         print(e)
#
def get_plot(data):
    fig = go.Figure()
    if not data:
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.add_trace(go.Box(y=data[0], name='A', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[1], name='B', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[2], name='C', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[3], name='D', marker_color='indianred'))
    fig.add_trace(go.Box(y=data[4], name='F', marker_color='indianred'))
    # fig.update_layout(title_text="Distribution of Scores by Grade for all")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # fig.show()


def get_all_data():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/boxplot', max_overflow=10)
    base_sql = "select score from moody2022 where "
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
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/boxplot', max_overflow=10)
    s = s.lower()
    first_condition = " where "
    base_sql = "select score from moody2022 "
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


# def get_query_data(s):
#     engine = create_engine('mysql+pymysql://root:root@localhost:3306/boxplot', max_overflow=10)
#     s = s.lower()
#     first_condition = " where "
#     base_sql = "select score from moody2022 "
#     for i in range(len(s) - 5):
#         if(s[i:i+5] == 'where'):
#             first_condition = s[i:]
#     condition = "GRADE = '"
#     grades=['A', 'B', 'C', 'D', 'F']
#     if first_condition == " where ":
#         return {}
#     scores = {}
#     for i in range(5):
#         sql = base_sql + first_condition + ' and ' + condition + grades[i] + "'"
#         scores[grades[i]] = engine.execute(sql).fetchall()
#     for score in scores.values():
#         for i in range(len(score)):
#             score[i] = float(score[i][0])
#     return scores

# cur = engine.execute(sql)
# return str(cur.fetchall())
# result = cur.fetchall()
# res = '<ul>'
# for a in result:
#     for b in a:
#         res = res + '<li>'
#         res = res + str(b)
#         res = res + '</li>'
# res = res + '</ul>'
# return res

@app.route("/", methods=['GET','POST'])
def start():
    s = request.form.get("sql_query")
    data = get_all_data()
    query_data = get_query_data(s)
    return render_template('index.html', graph1=get_plot(data), graph2=get_plot(query_data))


if __name__ == '__main__':
    app.run()
    # res = get_all_data()
    # get_plot(res)
    # s = "select * from moody2022 where dozes_off='never' or participation>0.1"
    # rr = get_query_data(s)
    # get_plot(rr)
    # print(rr)
    # str = "SELECT * FROM moody2022_new WHERE "

from flask import Flask, render_template,request,flash
import random
import pypyodbc
import time
import redis
import pygal

app = Flask(__name__)
app.secret_key = "Secret! Dont Tell anyone"
conn = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:servermanasa.database.windows.net,1433;Database=database1;Uid=serverm;Pwd=BluDiam0@;")


@app.route('/')
def hello_world():

    return render_template('index.html')


@app.route('/chart_bar', methods=['GET'])
def chart_bar():
    bar_chart = pygal.Bar(width=1000, height=500)
    att = str(request.args.get('att'))
    bar_chart.title = att

    # year = 'y_' + year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 + '-' + hrange1, lrange2 + '-' + hrange2, lrange3 + '-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result[0][0])
    answers = []
    answers.append(result[0][0])
    cursor.execute(sql1)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])

    cursor.execute(sql2)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])

    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('bar_chart.html', chart=bar_chart.render_data_uri())


@app.route('/chart_pie', methods=['GET'])
def chart_pie():
    pie_chart = pygal.Pie(height=300)
    att = str(request.args.get('att'))
    pie_chart.title = att

    # year = 'y_' + year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 + '-' + hrange1, lrange2 + '-' + hrange2, lrange3 + '-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result[0][0])
    answers = []
    answers.append(result[0][0])
    cursor.execute(sql1)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])

    cursor.execute(sql2)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])

    pie_chart.add(range[0], answers[0])
    pie_chart.add(range[1], answers[1])
    pie_chart.add(range[2], answers[2])
    return render_template('pie_chart.html', chart=pie_chart.render_data_uri())


@app.route('/chart_xy', methods=['GET'])
def chart_xy():
    xy_chart = pygal.XY(stroke=False, height=300)
    att = str(request.args.get('att'))
    xy_chart.title = att

    # year = 'y_' + year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 + '-' + hrange1, lrange2 + '-' + hrange2, lrange3 + '-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(" + att + ") from all_month where " + att + " between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result[0][0])
    answers = []
    answers.append(result[0][0])
    cursor.execute(sql1)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])
    cursor.execute(sql2)
    result = cursor.fetchall()
    answers.append(result[0][0])
    print(result[0][0])
    xy_chart.add(range[0], answers[0])
    xy_chart.add(range[1], answers[1])
    xy_chart.add(range[2], answers[2])
    return render_template('pie_chart.html', chart=xy_chart.render_data_uri())


if __name__ == '__main__':
    app.run()

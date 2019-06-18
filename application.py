from flask import Flask, render_template,request
import random
import pypyodbc
import time


app = Flask(__name__)
connection = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:servermanasa.database.windows.net,1433;Database=database1;Uid=serverm;Pwd=BluDiam0@;")


@app.route('/')
def hello_world():
    cursor = connection.cursor()
    cursor.execute("select count(*) from all_month")
    rows = cursor.fetchall()
    count = rows[0][0]
    return render_template('index.html', count=count)


@app.route('/query_random', methods=['GET', 'POST'])
def query_random():
    cursor = connection.cursor()
    query_limit = request.args['query_limit']
    start_time = time.time()
    list_of_times = []
    for i in range(0, int(query_limit)):
        start_intermediate_time = time.time()
        cursor.execute("select TOP 1 * from all_month order by rand()")
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)
    end_time = time.time()
    time_taken = (end_time-start_time) / int(query_limit)
    #time_taken=89
    #list_of_times=[10,20,30]
    return render_template('graph.html', time_taken=time_taken, list_of_times=list_of_times)

@app.route('/restricted')
def restricted():
    cursor=connection.cursor()
    query_limit = request.args['query_limit1']
    lowmag = request.args['lowmag']
    highermag = request.args['highermag']
    start_time1 = time.time()
    for i in range(0, int(query_limit)):
        rngvalue = random.uniform(float(lowmag), float(highermag))
        sql = 'select * from all_month where mag>=? '
        cursor.execute(sql, (rngvalue,))
        end_time1 = time.time()
        time_taken = (end_time1 - start_time1) / int(query_limit)
    return render_template('restricted.html', time_taken=time_taken)


if __name__ == '__main__':
    app.run()

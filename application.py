from flask import Flask, render_template,request,flash
import random
import pypyodbc
import time
import redis
import pygal

app = Flask(__name__)
app.secret_key = "Secret! Dont Tell anyone"
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


@app.route('/redis_cache')
def redis_cache():
    cursor = connection.cursor()
    magnitude = request.args['magnitude']
    host_name = 'redism1.redis.cache.windows.net'
    password = '9HGqR0jGGu2dK7TvXitwPISiq4ETsK5fL5IRngx73hM='
    cache = redis.StrictRedis(host=host_name, port=6380, password=password, ssl=True)
    if not cache.get(magnitude):
        sql = 'select * from quake6 where mag>=? '
        cursor.execute(sql, (magnitude,))
        rows = cursor.fetchall()
        cache.set(magnitude, str(rows))
        flash('In DB Query with Magnitude: ' + str(magnitude))
    else:
        rows_string = cache.get(magnitude)
        flash('In Cache with Magnitude: ' + str(magnitude))
    return render_template('redis_cache.html')


@app.route('/depth_error', methods=['GET', 'POST'])
def depth_error():
    bar_chart = pygal.Bar(width=1000, height=500)
    cursor = connection.cursor()
    depth1 = request.args['depth1']
    depth2 = request.args['depth2']
    longitude = request.args['longitude']
    # start_time = time.time()
    # list_of_times = []
    # for i in range(0, int(query_limit)):
    #     start_intermediate_time = time.time()
    sql = "select * from quake6 where depthError >= ? and depthError <= ? and longitude > ?"
    paramlist = [depth1, depth2, longitude]
    cursor.execute(sql, paramlist)
    result = cursor.fetchall()
    depth = []
    longitude = []
    for row in result:
        depth.append(str(row[3]))
        longitude.append(row[2])
    bar_chart.add(depth, longitude)
    return render_template('depth_error.html', chart=bar_chart.render_data_uri())
    # cursor.execute("select * from quakes6 where depthError > ? and depthError < ? and longitude > ?")
    # end_intermediate_time = time.time()
    # intermediate_time = end_intermediate_time - start_intermediate_time
    # list_of_times.append(intermediate_time)
    # end_time = time.time()
    # time_taken = (end_time-start_time) / int(query_limit)
    # #time_taken=89
    # list_of_times=[10,20,30]
    # return render_template('depth_error.html', result=result)


@app.route('/bar_chart', methods=['GET', 'POST'])
def bar_chart():
    barchart = pygal.Bar(width=1000, height=500)
    cursor = connection.cursor()

    # start_time = time.time()
    # list_of_times = []
    # for i in range(0, int(query_limit)):
    #     start_intermediate_time = time.time()
    depth1 = []
    long = []
    sql = "select depth from quake6 "
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        depth1.append(r[0])
    sql = "select longitude from quake6 "
    cursor.execute(sql)
    result = cursor.fetchall()
    for r in result:
        long.append(r[0])
    # longitude = []
    # for row in result:
    #     depth.append(str(row[3]))
    #     longitude.append(row[2])
    barchart.add(str(depth1), long)
    barchart.render()
    return render_template('chart.html', chart=barchart.render_data_uri())


@app.route('/depth', methods=['GET', 'POST'])
def depth():
    cursor = connection.cursor()
    depth1 = request.args['depth1']
    depth2 = request.args['depth2']
    count = request.args['count']
    # start_time = time.time()
    list_of_times = []
    # for i in range(0, int(query_limit)):
    #     start_intermediate_time = time.time()
    # sql = "select * from quake6 where depthError >= ? and depthError <= ? and longitude > ?"
    # paramlist=[depth1, depth2, longitude]
    # cursor.execute(sql, paramlist)
    # result = cursor.fetchall()
    countList = []
    randList1 = []
    randList2 = []
    for i in range(0, int(count)):
        start_intermediate_time = time.time()
        rand1 = random.randint(int(depth1), int(depth2))
        rand2 = random.randint(int(depth1), int(depth2))
        if(rand1 > rand2):
            t = rand1
            rand1 = rand2
            rand2 = t

        sql = "select count(*) from quake6 where depthError >= ? and depthError <= ?"
        paramlist = [str(rand1), str(rand2)]

        cursor.execute(sql, paramlist)
        result = cursor.fetchall()
        countList.append(result)
        randList1.append(str(rand1))
        randList2.append(str(rand2))
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)

    # cursor.execute("select * from quakes6 where depthError > ? and depthError < ? and longitude > ?")
    # end_intermediate_time = time.time()
    # intermediate_time = end_intermediate_time - start_intermediate_time
    # list_of_times.append(intermediate_time)
    # end_time = time.time()
    # time_taken = (end_time-start_time) / int(query_limit)
    # #time_taken=89
    # list_of_times=[10,20,30]
    count1 = 0
    return render_template('depth.html', result=countList, rand1=randList1, rand2=randList1, count=count1, list= list_of_times)


@app.route('/question2_execute', methods=['GET'])
def question2_execute():
    cursor = connection.cursor()
    sql = "select * from population where State = 'Alabama' or State = 'Florida'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    xy_chart = pygal.XY(stroke=False, height=300)
    xy_chart.title = 'Correlation'
    for r in result:
        db_years = [None, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
        state = ""
        scatterplot_data = []
        for i in range(1, len(r)):
            state = r[0]
            print(r[0])
            population_val = r[i]
            print(r[i])
            population_val = population_val.replace(",", "")
            int_val = int(population_val)
            tuple = (db_years[i], int_val)
            scatterplot_data.append(tuple)
        xy_chart.add(state, scatterplot_data)
    xy_chart.render()
    return render_template('question2.html', chart=xy_chart.render_data_uri())

# @app.route('/redis_cache')
# def redis_cache():
#     cursor = connection.cursor()
#     magnitude = request.args['magnitude']
#     host_name = 'redism1.redis.cache.windows.net'
#     password = '9HGqR0jGGu2dK7TvXitwPISiq4ETsK5fL5IRngx73hM='
#     cache = redis.StrictRedis(host=host_name, port=6380, password=password, ssl=True)
#     for i in range(0, int(count)):
#         start_intermediate_time = time.time()
#         rand1 = random.randint(int(depth1), int(depth2))
#         rand2 = random.randint(int(depth1), int(depth2))
#         if(rand1 > rand2):
#             t = rand1
#             rand1 = rand2
#             rand2 = t
#
#         sql = "select count(*) from quake6 where depthError >= ? and depthError <= ?"
#         paramlist = [str(rand1), str(rand2)]
#
#         cursor.execute(sql, paramlist)
#         result = cursor.fetchall()
#         countList.append(result)
#         randList1.append(str(rand1))
#         randList2.append(str(rand2))
#         if not cache.get(rand1):
#             flash('In DB Query with Magnitude: ' + str(rand1))
#         else:
#             rows_string = cache.get(rand1)
#             flash('In Cache with Magnitude: ' + str(rand1))
#         end_intermediate_time = time.time()
#         intermediate_time = end_intermediate_time - start_intermediate_time
#
#         sql = 'select * from all_month where mag>=? '
#         cursor.execute(sql, (magnitude,))
#         rows = cursor.fetchall()
#         cache.set(magnitude, str(rows))
#
#     return render_template('question7.html')



if __name__ == '__main__':
    app.run()

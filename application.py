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

    return render_template('index.html')


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
    return render_template('question1.html', time_taken=time_taken, list_of_times=list_of_times)


@app.route('/restricted_mag')
def restricted_mag():
    cursor = connection.cursor()
    query_limit = request.args['query_limit1']
    lowmag = request.args['lowmag']
    highermag = request.args['highermag']
    start_time1 = time.time()
    list_of_times = []
    for i in range(0, int(query_limit)):
        start_intermediate_time = time.time()
        sql = 'select * from all_month where mag>=? and mag<=? '
        paramlist = [lowmag, highermag]
        cursor.execute(sql, paramlist)
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)
    end_time1 = time.time()
    time_taken = (end_time1 - start_time1) / int(query_limit)
    return render_template('question2.html', time_taken=time_taken, list_of_times=list_of_times)


@app.route('/restricted_time')
def restricted_time():
    cursor = connection.cursor()
    query_limit = request.args['query_limit1']
    lowtime = str(request.args['lowtime'])
    highertime = str(request.args['highertime'])
    start_time1 = time.time()
    list_of_times = []
    for i in range(0, int(query_limit)):
        start_intermediate_time = time.time()
        sql = 'select * from all_month where CONVERT(VARCHAR, [time]) between ? and ?'
        paramlist = [lowtime, highertime]
        print(paramlist)
        cursor.execute(sql, paramlist)
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)
        print("List of time: ", list_of_times)
        print("Intermediate Time: ", intermediate_time)
    end_time1 = time.time()
    time_taken = (end_time1 - start_time1) / int(query_limit)
    print("Time taken: ", time_taken)
    return render_template('question2.html', time_taken=time_taken, list_of_times=list_of_times)


@app.route('/restricted_CA')
def restricted_CA():
    cursor = connection.cursor()
    query_limit = request.args['query_limit1']
    start_time1 = time.time()
    list_of_times = []
    ca = '%, CA'
    for i in range(0, int(query_limit)):
        start_intermediate_time = time.time()
        sql = 'SELECT * FROM all_month WHERE place LIKE ? '
        cursor.execute(sql, (ca,))
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)
        print("List of time: ", list_of_times)
        print("Intermediate Time: ", intermediate_time)
    end_time1 = time.time()
    time_taken = (end_time1 - start_time1) / int(query_limit)
    print("Time taken: ", time_taken)
    return render_template('question2.html', time_taken=time_taken, list_of_times=list_of_times)


@app.route('/restricted_loc')
def restricted_loc():
    cursor = connection.cursor()
    query_limit = request.args['query_limit1']
    lat = float(request.args['lat'])
    long = float(request.args['long'])
    start_time1 = time.time()
    list_of_times = []
    lat1 = lat + 100
    long1 = long + 100
    lat2 = lat - 100
    long2 = long - 100
    # paramlist = [lat1, long1, lat1, long2]
    for i in range(0, int(query_limit)):
        start_intermediate_time = time.time()
        sql = 'SELECT * FROM all_month WHERE latitude>=? and longitude>=? and latitude<=? and longitude<=? '
        cursor.execute(sql, (lat1, long1, lat2, long2))
        end_intermediate_time = time.time()
        intermediate_time = end_intermediate_time - start_intermediate_time
        list_of_times.append(intermediate_time)
        print("List of time: ", list_of_times)
        print("Intermediate Time: ", intermediate_time)
    end_time1 = time.time()
    time_taken = (end_time1 - start_time1) / int(query_limit)
    print("Time taken: ", time_taken)
    return render_template('question2.html', time_taken=time_taken, list_of_times=list_of_times)


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


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run()
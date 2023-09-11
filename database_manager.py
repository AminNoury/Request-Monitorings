import datetime

from file_opener_manager import request_monitoring
import psycopg2
import schedule
import time as tm


import matplotlib.pyplot as plt
from matplotlib import rc


conn = None
cur = None

try:
    hostname = 'localhost'
    database = 'Monitor'
    username = 'postgres'
    pwd = '!@!King2250778!@!'
    port_id = 5432

    conn = psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
        )

    cur = conn.cursor()
    def create_database():
        create_script = """ CREATE TABLE IF NOT EXISTS request_monitoring (
                                id serial ,
                                url varchar(60),
                                web_size_byte int,
                                first_time time,
                                deference_time_second float
        )
                        """
        cur.execute(create_script)

        return create_database
    create_database()

    def insertion():
        insert_script = 'INSERT INTO request_monitoring (url, web_size_byte, first_time, deference_time_second) VALUES (%s, %s, %s, %s)'
        insert_value = request_monitoring()
        for record in insert_value:
            cur.execute(insert_script, record)
        return insertion
    insertion()



    def select():
        select_script = 'SELECT url, AVG(deference_time_second) FROM request_monitoring GROUP BY url ORDER BY url ASC'
        cur.execute(select_script)
        data = cur.fetchall()
        return data
    select()


    def return_data():
        X_data = []
        Y_data = []
        for i in select():
            if i[0]:
                X_data.append(i[0])
            if i[1]:
                Y_data.append(i[1])
        X_data = [i[12:] for i in X_data]
        rc('font', **{'size': 7})
        plt.title('Average response time in a hour')
        plt.xlabel('web sites')
        plt.ylabel('response time per seconds')
        plt.xticks(rotation=25)
        plt.bar(X_data, Y_data)

        return plt.show()

    return_data()



    conn.commit()

    schedule.every(2).seconds.do(insertion)
    schedule.every(5).seconds.do(select)
    schedule.every(6).seconds.do(return_data)
    while True:
        s = datetime.datetime.now().second
        schedule.run_pending()
        tm.sleep(1)
        e = datetime.datetime.now().second
        print(e - s)

        conn.commit()






        # cur.close()
        # conn.close()

except Exception as error:
        print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()









from file_opener_manager import request_monitoring
import psycopg2


conn = None
cur = None
try:
    hostname = 'localhost'
    database = 'Monitor'
    username = 'postgres'
    pwd = '#'
    port_id = 5432

    conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
    )



    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS request_monitoring')
    create_script = """ CREATE TABLE IF NOT EXISTS request_monitoring (
                            id serial ,
                            url varchar(60),
                            web_size_byte int,
                            first_time time,
                            deference_time_second float
    )
    """

    cur.execute(create_script)


    insert_script = 'INSERT INTO request_monitoring (url, web_size_byte, first_time, deference_time_second) VALUES (%s, %s, %s, %s)'

    insert_values = request_monitoring()
    for record in insert_values:
        cur.execute(insert_script, record)

    conn.commit()


    cur.close()
    conn.close()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


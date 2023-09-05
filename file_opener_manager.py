import requests
import datetime


def request_monitoring():
    with open('d:/urls.txt', 'r') as f:
        urls = f.readlines()
        A = [(url.rstrip('\n')) for url in urls]
    D = []
    for url in A:
        s = datetime.datetime.now()
        r = requests.get(url)
        e = datetime.datetime.now()
        web_size_byte = len(r.text)
        first_time = e - s
        deference_time_second = r.elapsed.total_seconds()
        c = (url, web_size_byte, first_time, deference_time_second)
        D.append(c)
    return D


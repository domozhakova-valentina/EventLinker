from requests import get, post, delete


print(get('http://127.0.0.1:8000/api/v2/users').json())
#print(post('http://127.0.0.1:8000/api/v2/events').json())
#print(post('http://127.0.0.1:8000/api/v2/likes/0').json())

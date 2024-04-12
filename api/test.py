import requests
from requests import get,  delete


class CheckUsersApi:
    def check_get_list(self):
        print(get('http://127.0.0.1:8000/api/v2/users').json())

    def check_get_item(self, id):
        print(get(f'http://127.0.0.1:8000/api/v2/users/{id}').json())

    def check_post_delete(self):
        print("Тест создания нового пользователя:")
        response = requests.post('http://127.0.0.1:8000/api/v2/users', json={
            'name': 'Test User',
            'about': 'Test About',
            'email': 'test@example.com',
            'hashed_password': 'test_password'
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        test_user_id = response.json()['id']
        print("Изменение данных о тестовом пользователе:")
        response = requests.post(f'http://127.0.0.1:8000/api/v2/users/{test_user_id}', json={
            'name': 'Test User New',
            'about': 'Test About New',
            'email': 'test_changed@example.com',
            'hashed_password': 'test_password_new'
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        print("Тест удаления пользователя:")
        print(delete(f'http://127.0.0.1:8000/api/v2/users/{test_user_id}').json())


class CheckEventsApi:
    def check_get_list(self):
        print(get('http://127.0.0.1:8000/api/v2/events').json())

    def check_get_item(self, id):
        print(get(f'http://127.0.0.1:8000/api/v2/events/{id}').json())

    def check_post_delete(self):
        print("Тест создания нового события:")
        response = requests.post('http://127.0.0.1:8000/api/v2/events', json={
            'mini_description': 'test mini_description',
            'description': 'test description',
            'create_user': 1
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        test_event_id = response.json()['id']
        print("Изменение данных о тестовом событии:")
        response = requests.post(f'http://127.0.0.1:8000/api/v2/events/{test_event_id}', json={
            'mini_description': 'test mini_description new',
            'description': 'test description new'
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        print("Тест удаления события:")
        print(delete(f'http://127.0.0.1:8000/api/v2/events/{test_event_id}').json())


class CheckCommentsApi:
    def check_get_list(self):
        print(get('http://127.0.0.1:8000/api/v2/comments').json())

    def check_get_item(self, id):
        print(get(f'http://127.0.0.1:8000/api/v2/comments/{id}').json())

    def check_post_delete(self):
        print("Тест создания нового комментария:")
        response = requests.post('http://127.0.0.1:8000/api/v2/comments', json={
            'text': 'test text',
            'event_id': 1,
            'create_user': 1
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        test_comment_id = response.json()['id']
        print("Изменение данных о тестовом комментарии:")
        response = requests.post(f'http://127.0.0.1:8000/api/v2/comments/{test_comment_id}', json={
            'text': 'test text'
        })

        # Печать статуса ответа
        print(f'Status Code {response.status_code}')
        # Печать данных ответа в формате JSON
        print(response.json())

        print("Тест удаления комментария:")
        print(delete(f'http://127.0.0.1:8000/api/v2/comments/{test_comment_id}').json())


users = CheckUsersApi()
events = CheckEventsApi()
comments = CheckCommentsApi()
d = {'users': users, 'events': events, "comments": comments}
for table in d.keys():
    for id in range(1, 3):
        print(f'Информация об элементе таблицы "{table}" c id={id}:')
        d[table].check_get_item(id)
    print(f'Информация о всех {table}:')
    d[table].check_get_list()
    d[table].check_post_delete()

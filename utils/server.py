import requests

SERVER_API = 'https://ds4.nl/api/v1/'
SERVER_LOGIN = SERVER_API + 'auth-jwt/'
SERVER_USER = SERVER_API + 'user/'
SERVER_TURF = SERVER_API + 'turf/turf_item/'
LOGIN = {
    'username-or-email': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'password': 'xxxxxxxxxxxxxxxxxxxxxxxxx'
}


class Server:
    token = None

    def login(self):
        result = requests.post(SERVER_LOGIN, data=LOGIN)
        try:
            self.token = result.json()['token']
            return result.status_code
        except Exception as e:
            raise e

    def turf(self, user_id):
        print('turf url', SERVER_TURF)
        result = requests.post(
            SERVER_TURF, data={'turf_user_id': user_id, 'turf_count': 1, 'turf_type': 'beer'},
            headers={'Authorization': 'Bearer ' + self.token})
        try:
            return result.json()
        except Exception as e:
            raise e

    def user(self, user_id):
        print(f'{SERVER_USER}{user_id}/')
        result = requests.get(f'{SERVER_USER}{user_id}/', headers={'Authorization': 'Bearer ' + self.token})
        try:
            if result.status_code == 200:
                return result.json()
            else:
                return None
        except Exception as e:
            print("Error", e)
            return None

from configs import settings


class Connection:
    def __init__(self):
        self.user_list = dict()
        self.gift_list = dict()
        self.zbug = []
        self.me = None
        self.access_token_count = 0
    def send_message(self, data):
        api_url = settings.api_url
        endpoint = 'message/custom/send'
        params = {'access_token': self.get_access_token()}
        response = requests.post('{api_url}/{endpoint}', api_url=api_url, endpoint=endpoint, params=params, data=data)
        return response.text['errcode']

    def get_access_token(self):
        # returns active access token
        if time.time() > settings.timer:
            endpoint = 'token'
            params = {'grant_type': 'client_credential',
                      'appid': settings.app_id,
                      'secret': settings.app_secret}
            response = requests.get('{api_url}/{endpoint}', api_url=settings.api_url, endpoint=endpoint, params=params)
            settings.access_token = response.text['access_token']
            settings.timer = time.time() + response.text['expires_in'] - 10.0

            self.access_token_count += 1
            print "Get Access Token! Count: " + str(self.access_token_count)

        return settings.access_token

    def get_user_info(self, openid):
        # returns user info fetched with openid in json format
        endpoint = 'user/info'
        params = {'access_token': self.get_access_token(),
                  'openid': openid,
                  'lang': 'en'}
        response = requests.get('{api_url}/{endpoint}', api_url=settings.api_url, endpoint=endpoint, params=params)
        user = request.json()
        return user

connection = Connection()

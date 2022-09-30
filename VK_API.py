"""
Класс для работы с VK-API
Create at 28.09.2022 19:22:47
~/main.py
"""

__author__ = 'maxc0der'
__copyright__ = 'KIB, 2022'
__license__ = 'KIB'
__credits__ = [
    'maxc0der',
]
__version__ = "20220928"
__status__ = "Production"


import requests
import time
import json


class VK:
    """Class for requests to VK-API

    Attributes:
    _________________
    token - VK-API access token

    Methods:
    _________________
    get(method, request, version='5.86')
    Function that receives response from methods

    get_posts_filtered_by_date(source_id, start_date, end_date):
    Return json-object of posts from source_id with date between start_date and end_date
    """
    def __init__(self, token):
        self.token = token

    def get(self, method, request, version='5.86'):
        """get answer from VK API"""
        response = requests.get(
            'https://api.vk.com/method/' + method,
            params={'access_token': self.token, 'v': version} | request,
            headers={'Accept': 'application/json', "User-Agent": "curl/7.61.0"},
        )
        r = response.content.decode()
        response_json = json.loads(r)
        if 'response' in response_json:
            return response_json['response']
        else:
            return response_json['error']['error_msg']

    def get_posts_filtered_by_date(self, source_id, start_date, end_date):
        """Return json-object of posts from source_id with date between start_date and end_date"""
        result = list()
        offset = 0
        items_count = -1

        while True:
            response = self.get('wall.get', {'owner_id': source_id, 'count': 100, 'offset': offset})
            offset = offset + 100
            if 'error' not in response and not isinstance(response, str):
                items = response['items']
                if response['items'][1]['date'] < start_date:  # 1-st item here, because 0 can be pinned post
                    break
                if response['items'][-1]['date'] < end_date:
                    for item in items:
                        if end_date > item['date'] > start_date:
                            result.append(item)
                if items_count == -1:
                    items_count = response['count']
                if offset >= items_count:
                    break
            else:
                print('Error: ', response)
                break
            time.sleep(0.5)

        return result

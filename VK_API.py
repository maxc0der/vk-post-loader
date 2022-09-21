import requests
import time


class VK:
    def __init__(self, token):
        self.token = token

    def get(self, method, request, version='5.86'):
        response = requests.get(
            'https://api.vk.com/method/' + method,
            params={'access_token': self.token, 'v': version} | request,
            headers={'Accept': 'application/json'},
        )
        response_json = response.json()
        if 'response' in response_json:
            return response_json['response']
        else:
            return response_json['error']['error_msg']

    def get_posts_filtered_by_date(self, source_id, start_date, end_date):
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
                print(response)
                break
            time.sleep(0.5)

        return result

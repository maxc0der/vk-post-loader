"""
Основной файл программы
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

import datetime
import time
import json
from VK_API import VK
import sys
import argparse
import os.path


def date_formatter(x):
    """Input YYYYMMDD date, return Unix-format"""
    return time.mktime(datetime.date(int(x[0:4]), int(x[4:6]), int(x[6:8])).timetuple())


parser = argparse.ArgumentParser(description="Get posts filtered by date")
parser.add_argument('source_id', type=int, help='ID of the group from which we load posts')
parser.add_argument('-f', '--from_date', type=int, help='From what date to filter posts, format YYYYMMDD')
parser.add_argument('-t', '--to_date', type=int, help='To what date to filter posts, format YYYYMMDD')
parser.add_argument('--out', type=str, help='File for save results')
args = parser.parse_args()

assert args.from_date <= args.to_date, '"To" date could not be earlier then "From" date'
assert os.path.exists('private.txt'), 'private.txt with VK-token does not exists'
with open("private.txt", "r") as token_file:
    token = token_file.read()
vkapi = VK(token)


from_time = date_formatter(str(args.from_date))
to_time = date_formatter(str(args.from_date + 1))
with open(args.out, "w", encoding="utf-8") as results_file:
    result = vkapi.get_posts_filtered_by_date(args.source_id, from_time, to_time)
    json.dump(result, results_file,  indent=4, ensure_ascii=False)

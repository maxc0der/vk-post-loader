import datetime
import time
import json
from VK_API import VK
import sys
import codecs


sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='UTF-8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='UTF-8', buffering=1)
token, source_id, start_time, end_time = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

vkapi = VK(token)
start_time = time.mktime(datetime.date(int(start_time[0:4]), int(start_time[4:6]), int(start_time[6:8])).timetuple())
end_time = time.mktime(datetime.date(int(end_time[0:4]), int(end_time[4:6]), int(end_time[6:8])).timetuple()) + 24*3600
print(json.dumps(vkapi.get_posts_filtered_by_date(source_id, start_time, end_time),  indent=4))

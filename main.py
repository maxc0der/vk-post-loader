import requests
import time
from VK_API import VK


vkapi = VK("")
vkapi.get_posts_filtered_by_date('-112510789', int(time.time() - 6*3600), int(time.time() - 3*3600))

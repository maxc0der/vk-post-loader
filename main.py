import requests
import time
from VK_API import VK


print(time.time() - 12*3600, ' ', time.time())
print(type(time.time()))
vkapi = VK('vk1.a.mnzNEGIE85YgWfE8CbL4G9qEvKRotT5u1JsYYRfZsRjG7eoBghZutHrZ8K3WlZ2pLUMbvUyyx7AxJzk1_3RAmQpJ6Q-XP6W9CyC5dbTi1Fd5uK00J_38DwCwNnAWFcAvB4t5NlRzkGmUEQxOYuZih9JyYLJugY-k3g01o9BnUWpDeOn59d5BMiyzX12kW5xc')
vkapi.get_posts_filtered_by_date('-112510789', int(time.time() - 6*3600), int(time.time() - 3*3600))

from VK_API import VK
import pika
from typing import Dict, List, Union
import os
import copy
import json
from core.rabbitmq.messages import send_social_network_message


RABBIT_HOST = '172.24.5.0'
RABBIT_PORT = 5672
RABBIT_PORT_ADMIN = 15672
VIRTUAL_HOST_PIPELINES = 'pipelines'
RABBIT_USER = os.getenv('RABBIT_USER', 'admin')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'admin')
DEFAULT_forwards_push = False
debug = True
SOURCE = 'vk'
EXTRACTOR_SUB_TYPE_HISTORY = 'extractor.history'
EXTRACTOR_SUB_TYPE_FRESH_DATA = "extractor.fresh_data"
with open("private.txt", "r") as token_file:
    token = token_file.read()
vkapi = VK(token)


def new_connection(*, host=RABBIT_HOST):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=RABBIT_PORT,
            virtual_host=VIRTUAL_HOST_PIPELINES,
            credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
        )
    )
    return connection


def message2body(message: Union[Dict, List]) -> bytes:
    return json.dumps(message).encode('utf-8')


def body2message(body: bytes) -> Union[Dict, List]:
    body_str = body.decode('utf-8')
    message = json.loads(body_str)
    return message


def get_task(path):
    with open(path, 'r') as fr:
        message = json.load(fr)
    return message


def push_message(
    publish_channel,
    source,
    channel,
    message,
    headers,
    routing_key,
) -> bool:
    message_headers = copy.copy(headers)

    # triggers = collect_triggers(source, channel, message)
    triggers = []

    if triggers:
        message_headers["trigger"] = True
        for trigger in triggers:
            message_headers[trigger] = True

    return send_social_network_message(
        connection_channel=publish_channel,
        routing_key=routing_key,
        message=message,
        headers=message_headers,
    )


def add_task(path):
    connection = new_connection()
    ch = connection.channel()

    message = get_task(path)
    headers = {
        'source': message['source'],
        'channel': message['channel'],
        'save2db': False,
        'apisynch': False,
    }

    ch.basic_publish(
        exchange='ex-extractor',
        routing_key='',
        body=message2body(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            headers=headers,
        ),
    )
    print(f"Прогружено сообщение {json.dumps(message)}")
    ch.close()
    connection.close()


#add_task('tasks/1.json')

def _callback(connection_channel, method, properties, body, forwards_push: bool = DEFAULT_forwards_push):
    headers = properties.headers
    in_message = body2message(body)
    routing_key = method.routing_key
    worker_uuid = method.consumer_tag
    sub_type = in_message.get('sub_type')
    assert isinstance(worker_uuid, str)
    save2db = headers.get("save2db", False)
    headers['worker_uuid'] = worker_uuid
    channel = in_message.get('channel')

    print(in_message)

    if in_message.get('type') != 'task' \
            or in_message.get('source') != SOURCE \
            or not sub_type \
            or not channel:
        # По ошибке попали сообщения в очередь
        #   просто их скипаем.
        # TODO: писать в лог
        connection_channel.basic_ack(delivery_tag=method.delivery_tag)
        return

        #TODO: пропуск несуществующих каналов

    if sub_type == EXTRACTOR_SUB_TYPE_HISTORY:
        day_from = in_message['day_from']
        day_to = in_message['day_to']
        print('Собираем')

        publish_channel = connection_channel.connection.channel()

        for message in vkapi.get_posts_filtered_by_date(source_id=channel, start_date=day_from, end_date=day_to):
#            print(message)
            if push_message(
                    publish_channel=publish_channel,
                    source=SOURCE,
                    channel=channel,
                    message=message,
                    headers=headers,
                    routing_key=routing_key,
            ):
                print(f"send message {channel}::{message.get('id')}")
        publish_channel.close()
        connection_channel.basic_ack(delivery_tag=method.delivery_tag)

    elif sub_type == EXTRACTOR_SUB_TYPE_FRESH_DATA:
        raise NotImplementedError(f"sub_type={sub_type} не реализовано")
    else:
        raise NotImplementedError(f"sub_type={sub_type} не реализовано")
    return


def callback(connection_channel, method, properties, body, forwards_push: bool = DEFAULT_forwards_push):
    try:
        return _callback(connection_channel, method, properties, body, forwards_push=forwards_push)
        print(body)
        # TODO: Error processing
        connection_channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        if debug:
            raise exc
        # TODO: Error processing
        connection_channel.basic_ack(delivery_tag=method.delivery_tag)


#add_task('tasks/1.json')


connection = new_connection()
connection_channel = connection.channel()
worker_uuid = '001'
connection_channel.basic_consume(
    queue='clq-vk-extractor',
    on_message_callback=lambda ch, m, p, b: callback(ch, m, p, b),
    auto_ack=False,
    consumer_tag=str(worker_uuid),
)
connection_channel.start_consuming()



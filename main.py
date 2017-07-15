import requests
import json
import time
from pymongo import MongoClient
from config import access_token
client = MongoClient('localhost', 27017)
db = client.vk


def api_send(method_name, params, access_token):
    params['access_token'] = access_token
    params['v'] = '5.67'
    return requests.get("https://api.vk.com/method/{}".format(method_name), params=params)

def get_some_messages(out=1, offset=0, count=1):
    result = api_send("messages.get", {
        'out': out,
        'offset': offset,
        'count': count
        }, access_token)
    if result.status_code != 200:
        raise("API status code error: {}, {}, {}".format(result.status_code, 
                                                         result.headers,
                                                         result.content))
    data = json.loads(result.content.decode('utf-8'))
    messages_count = data['response']['count']
    items = data['response']['items']
    return messages_count, items

def get_attachments():
    pass

def dump_messages(out=1): # count=200
    
    db.messages.remove({})
    db.users.remove({})
    db.docs.remove({})
    db.photos.remove({})
    db.links.remove({})
    db.wall.remove({})

    try:
        # messages_count = 400
        user_ids = {}
        attachments = []
        photos = []
        links = []
        wall = []
        messages_count, _ = get_some_messages(out)

        for offset_message_id in range(22000, messages_count, 200):
            _, items = get_some_messages(out, offset_message_id, 200)
            for item in items:
                try:
                    db.messages.insert_one(item)
                    if item['user_id'] not in user_ids:
                        user_ids[item['user_id']] = 1
                        db.users.insert_one({'user_id': item['user_id']})

                    if 'attachments' in item:
                        for attachment in item['attachments']:
                            t = attachment['type']
                            if t == 'sticker':
                                continue
                            if t == 'wall':
                                continue
                            if t == 'video':
                                continue
                            if t == 'gift':
                                continue
                            if t == 'audio':
                                continue
                            if t == 'doc':
                                attachments.append(attachment['doc']['url'])
                                db.docs.insert_one({'url': attachment['doc']['url']})
                                continue
                            if t == 'photo':
                                result = list(map(lambda x: x[6:], filter(lambda x: x.startswith('photo_'), attachment['photo'].keys())))
                                image_url = attachment['photo']["photo_" + result[0]]
                                photos.append(image_url)
                                db.photos.insert_one({'url': image_url})
                                continue
                            if t == 'link':
                                links.append(attachment['link']['url'])
                                db.links.insert_one(attachment['link'])
                                continue

                            print(item)
                            exit()

                except Exception as e:
                    print("Error in item: {} {}".format(item, e))

            print(offset_message_id)
            time.sleep(1)

        print("[Done]. {} users".format(len(user_ids)))
        print("[Done]. {} messages".format(messages_count))
        print("[Done]. {} attachments".format(len(attachments)))

    except Exception as e:
        print("Error: {}".format(e))


if __name__ == "__main__":
    dump_messages()

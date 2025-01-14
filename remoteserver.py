from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message


class RemoteServer :
    def __init__(self,url):
        self.url=url

    def get_user(self)->list[User]:
        response_u = requests.get(self.url+'/users')
        return [User((user['id']), user['name']) for user in response_u.json()]

    def get_channel(self)->list[Channel]:
        response_c = requests.get(self.url+'/channels')
        return [Channel(channel["id"], channel["name"], channel["member_ids"]) for channel in response_c.json()]
##### MARCHE PAS CAR CHANNEL[MEMBER_IDS]#######
    def get_message(self)->list[Message]:
        response_m= requests.get(self.url+'/messages')
        return [Message(message["id"], message["reception_date"], message["sender_id"],message["channel_id"], message["content"]) for message in response_m.json()]
    
    def adding_user(self,nom):
        requests.post(self.url+'/users/create', json={"name": nom})

    def adding_member_to_channel(self, id_channel, id_member):
        requests.post(self.url+f'/channels/{id_channel}/join', json={"user_id": id_member})

    def creating_new_group(self, name, membres):
        requests.post(self.url+f'/channels/create', json={"name": name})
        for channel in self.get_channel():
            if channel.name==name:
                id_channel=channel.id
        for id_membres in membres :
            self.adding_member_to_channel(id_channel,id_membres)
        
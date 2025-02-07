from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message
from server import Server
from typing import override
import sys
sys.stdout.reconfigure(encoding="utf-8")    # Pour ne pas avoir de problème de décodage, on se met directement en utf-8


class RemoteServer(Server) :
    def __init__(self,url:str):
        self.url=url

######### Fonctions qui sont en lien avec des fonctions de la classe Intéraction #############
    @override
    def get_user(self)->list[User]:
        response_u = requests.get(self.url+'/users')
        return [User((user['id']), user['name']) for user in response_u.json()]
    @override
    def get_channel(self)->list[Channel]:
        response_c = requests.get(self.url+'/channels')
        #responce_member_ids=requests.get(self.url+'')
        channels=[]
        for channel in response_c.json():
            id,name=channel["id"],channel["name"]
            responce_member_ids=requests.get(self.url+f'/channels/{id}/members').json()
            member_ids=[member["id"] for member in responce_member_ids]
            channels.append(Channel(id,name,member_ids))
        return channels
    @override
    def get_message(self)->list[Message]:
        response_m= requests.get(self.url+'/messages')
        return [Message(message["id"], message["reception_date"], message["sender_id"],message["channel_id"], message["content"]) for message in response_m.json()]
    
### Concernant les utilisateurs ###
    @override
    def adding_user(self,nom:str)->None:
        requests.post(self.url+'/users/create', json={"name": nom})
    @override
    def deleting_user(self,user_to_delete_id:int)->None:
        response=requests.delete(self.url+f'/users/{user_to_delete_id}')
        if response.status_code != 200:
            print ("Cette fonction n'est pas encore disponible")

### Concernant les groupes ###
    @override
    def displaying_channel_members(self,id_channel:int)->list[User]:
        response= requests.get(self.url+f'/channels/{id_channel}/members')
        print ([User(user["id"],user["name"]) for user in response.json()])
    @override
    def adding_member_to_channel(self, id_channel:int, id_member:int)->None:
        requests.post(self.url+f'/channels/{id_channel}/join', json={"user_id": id_member})
    @override
    def creating_new_group(self, name:str, membres:list[int])->None:
        requests.post(self.url+f'/channels/create', json={"name": name})
        for channel in self.get_channel():
            if channel.name==name:
                id_channel=channel.id
        for id_membres in membres :
            self.adding_member_to_channel(id_channel,id_membres)
    @override
    def deleting_user_from_channel(self,channel_id:int,personne_del_id:int)->None:
            response=requests.delete(self.url+f'/channels/{channel_id}/members/{personne_del_id}')
            if response.status_code != 200:
                print ("Cette fonction n'est pas encore disponible")
            
 ### Concernant les Messages ###
    @override
    def sending_message(self,sender_id:int,channel_id:int,content:str)->None:
        requests.post(self.url+f'/channels/{channel_id}/messages/post', json={"sender_id": sender_id,"content": content})
    @override
    def deleting_message(self,id:int)->None:
        response=requests.delete(self.url+f'/messages/{id}')
        if response.status_code != 200:
            print ("Cette fonction n'est pas encore disponible")
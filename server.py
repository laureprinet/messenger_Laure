from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message


class Server : 
    def __init__(self, nom_fichier):
        self.filename=nom_fichier
        self.users : list[User]=[] 
        self.channels : list[Channel]=[] 
        self.messages : list[Message] =[]
    
    def __repr__(self) -> str :
        return f'Server(name={self.name}, users={self.users}, channels={self.channels})'

    def load_server(self,Server_json_name):         
        with open(Server_json_name) as json_file:
            doc = json.load(json_file)
            self.users=[User(L['id'],L['name']) for L in doc['users']]     
            self.channels=[Channel(L['id'],L['name'],L['member_ids']) for L in doc['channels']]
            self.messages=[Message(L['id'], L['reception_date'], L['sender_id'], L['channel_id'], L['content']) for L in doc['messages']]     

    def save(self):
        server_json={}
        server_json['users']=[{'id':user.id,'name':user.name} for user in self.get_user()]
        server_json['channels']=[{'id':channel.id,'name':channel.name, 'member_ids': channel.member_ids} for channel in self.get_channel()]
        server_json['messages']=[{'id' : message.id, 'reception_date': message.reception_date, 'sender_id':message.sender_id, 'channel_id': message.channel_id, 'content':message.content} for message in self.get_message()]
        Server_json_name=self.filename
        with open(Server_json_name, 'w') as file:
            json.dump(server_json, file)

    def get_user(self)->list[User]:
        return self.users
    
    def get_channel(self)->list[Channel]:
        return self.channels
    
    def get_message(self)->list[Message]:
        return self.messages
    
    def adding_user(self,id,nom):
        self.get_user().append(User(id,nom))
        for user in self.get_user():
            print(User(user.id, user.name))    #on réaffiche tous les users pour voir le nouveau apparaître
        self.save()
    
    def adding_member_to_channel(self,id_channel, id_member):
        for channel in self.get_channel():
            if channel.id==id_channel:
                bon_channel=channel
        bon_channel.member_ids.append(id_member)
        print(bon_channel)
        self.save()

    def creating_new_group(self, name, membres):
        id=max([channel.id for channel in self.server.get_channel()])+1
        self.get_channel().append(Channel(id,name,membres))
        self.save()
        
from datetime import datetime
import json
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message
from server import Server
from typing import override


class LocalServer (Server): 
    def __init__(self, nom_fichier:str):
        self.filename=nom_fichier
        self.users : list[User]=[] 
        self.channels : list[Channel]=[] 
        self.messages : list[Message] =[]
    
    def load_server(self,Server_json_name:str):         
        with open(Server_json_name,"r", encoding="utf-8") as json_file:
            doc = json.load(json_file)
            # Même si vous utilisez votre variable à côté de sa définition,
            # il vaut mieux un nom plus explicite que "L"
            self.users=[User(user['id'],user['name']) for user in doc['users']]
            self.channels=[Channel(channel['id'],channel['name'],channel['member_ids']) for channel in doc['channels']]
            self.messages=[Message(message['id'], message['reception_date'], message['sender_id'], message['channel_id'], message['content']) for message in doc['messages']]

    # La fonction save n'ayant pas vocation à être utilisée
    # hors de la classe, vous pouvez la préfixer par "_"
    def save(self):
        server_json={}
        server_json['users']=[{'id':user.id,'name':user.name} for user in self.get_user()]
        server_json['channels']=[{'id':channel.id,'name':channel.name, 'member_ids': channel.member_ids} for channel in self.get_channel()]
        server_json['messages']=[{'id' : message.id, 'reception_date': message.reception_date, 'sender_id':message.sender_id, 'channel_id': message.channel_id, 'content':message.content} for message in self.get_message()]
        Server_json_name=self.filename
        with open(Server_json_name, 'w', encoding="utf-8") as file:
            json.dump(server_json, file)


######### Fonctions qui sont en lien avec des fonctions de la classe Intéraction #############
    @override
    def get_user(self)->list[User]:
        return self.users
    @override
    def get_channel(self)->list[Channel]:
        return self.channels
    @override
    def get_message(self)->list[Message]:
        return self.messages
    
### Concernant les utilisateurs ###
    @override
    def adding_user(self,nom:str)->None:
        users_id=[user.id for user in self.get_user()]
        if users_id==[]:
            id=1
        else:
            id=max(users_id)+1
        self.users.append(User(id,nom))
        self.save()
    @override
    def deleting_user(self, id_user_to_delete:int)->None:
        for user in self.get_user():
            if user.id==id_user_to_delete:
                # Il vaut mieux éviter de modifier la liste sur
                # laquelle on itère avec remove ou append.
                # Ici, lorsque vous faites un remove,
                # vous raccourcissez la liste, et la boucle
                # for va sauter un élément. Vous pouvez le tester
                # avec le code suivant :
                # >>> l = ['a', 'b', 'c', 'd']
                # >>> for x in l:
                # ...     print(x)
                # ...     if x == 'b':
                # ...         l.remove(x)
                # ...
                # a
                # b
                # d
                self.users.remove(user)
        self.save()

    # Une alternative :
    def deleting_user_2(self, id_user_to_delete: int) -> None:
        self.users = [user for user in self.users if user.id != id_user_to_delete]
        self.save()

### Concernant les groupes ###
    @override
    def get_channel_members(self,id_channel:int)->list[User]:
        members_in_channel=[]
        for channel in self.channels:
            if channel.id==id_channel:
                for user in self.users :
                    if user.id in channel.member_ids:
                        members_in_channel.append(user)
        # Il vaut mieux renvoyer la liste d'utilisateurs et laisser
        # la classe Interaction décider comment afficher cette liste.
        # Elle pourra ainsi faire plus de choses qu'un simple print,
        # sans que vous ayez besoin de dupliquer ce code dans RemoteServer.
        # Par ailleurs, ça vous faciliterait l'implémentation d'autres
        # classes d'interactions, dans le cas où vous voudriez développer
        # une interface graphique par exemple
        return members_in_channel
    @override
    def adding_member_to_channel(self,id_channel:int, id_member:int)->None:
        for channel in self.get_channel():
            if channel.id==id_channel:
                channel.member_ids.append(id_member)
        self.save()
    @override
    def creating_new_group(self, name:str, membres:list[int])->None:
        channels_id=[channel.id for channel in self.get_channel()]
        if channels_id==[]:
            id=1
        else:
            id=max(channels_id)+1
        self.get_channel().append(Channel(id,name,membres))
        self.save()
    @override  
    def deleting_user_from_channel(self,channel_id:int,personne_del_id:int)->None:
        for channel in self.get_channel():
            # Afin d'éviter une erreur, vous pouvez vérifier
            # que la personne à supprimer fait bien partie du groupe
            if channel.id==channel_id and personne_del_id in channel.member_ids:
                channel.member_ids.remove(personne_del_id)
        self.save()

### Concernant les Messages ###
    @override
    def sending_message(self,sender_id:int,channel_id:int,content:str)->None:
        messages_id=[message.id for message in self.get_message()]
        if messages_id==[]:
            id=1
        else:
            id=max(messages_id)+1
        reception_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.get_message().append(Message(id,reception_date,sender_id, channel_id, content))
        self.save()
    @override
    def deleting_message(self,id:int)->None:
        for message in self.get_message():
            if message.id==id:
                self.messages.remove(message)
        self.save()
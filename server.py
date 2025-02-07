from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message

class Server :
    def __init__(self):
        pass
    
    def get_user(self)->list[User]:
        pass
    def get_channel(self)->list[Channel]:
        pass
    def get_message(self)->list[Message]:
        pass
    
    #### USER ####
    def adding_user(self,nom:str)->None:
        pass
    def deleting_user(self,user_to_delete_id:int)->None:
        pass
    
    #### CHANNEL ####
    def displaying_channel_members(self,channel_id:int)->list[User]:
        pass
    def adding_member_to_channel(self, id_channel:int, id_member:int)->None:
        pass
    def creating_new_group(self, name:str, membres:list[int])->None:
        pass
    def deleting_user_from_channel(self,channel_id:int,personne_del_id:int)->None:
        pass
    
    #### MESSAGE ####
    def sending_message(self,sender_id:int,channel_id:int,content:str)->None:
        pass
    def deleting_message(self,id:int)->None:
        pass



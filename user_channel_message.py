from datetime import datetime
import json
import requests
from argparse import ArgumentParser

class User:
    def __init__(self,id: int, name:str):
        self.id=id
        self.name=name
    def __repr__(self) -> str: 
        return f'User (id={self.id}, name={self.name})'
    
class Channel:
    def __init__(self,id:int,name:str,member_ids:list):
        self.id=id
        self.name=name
        self.member_ids=member_ids
    def __repr__(self) -> str: 
        return f'Channel (id={self.id}, name={self.name}; member_ids={self.member_ids})'

class Message:
    def __init__(self, id : int, reception_date : str, sender_id : int, channel_id : int, content :str):
        self.id=id
        self.reception_date=reception_date
        self.sender_id=sender_id
        self.channel_id=channel_id
        self.content=content
    def __repr__(self)->str:
        return f'Message (id = {self.id}, content = {self.content}, envoyé par l\'user d\'id {self.sender_id} ; channel = {self.channel_id}, date de réception = {self.reception_date})'

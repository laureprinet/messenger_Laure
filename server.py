from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message

class Server :
    # Pas besoin de déclarer __init__ et __repr__. Vous n'avez besoin
    # de déclarer que les fonctions qui sont appelées explicitement
    # sur des Server
    
    # Comme cette fonction renvoie une liste d'utilisateurs,
    # il vaudrait mieux l'appeler "get_users". Pour une fonction "get_user",
    # on s'attendrait à envoyer un identifiant en paramètre et
    # récupérer un unique User en retour
    def get_user(self)->list[User]:
        # Nous n'avons pas vu les exceptions en cours,
        # mais elles permettent de remonter des erreurs d'exécutions.
        # Ici ce code n'est pas censé être atteint, car la fonction
        # sera toujours appelée sur une sous-classe qui la redéfinira.
        # Si on oublie de la redéfinir, l'erreur sera assez explicite
        # (Not implemented)
        raise NotImplementedError()
    def get_channel(self)->list[Channel]:
        raise NotImplementedError()
    def get_message(self)->list[Message]:
        raise NotImplementedError()
    
    #### USER ####
    # Par convention, on utilise plutôt la forme "add_user" que "adding_user"
    # pour un nom de fonction
    def adding_user(self,nom:str)->None:
        raise NotImplementedError()
    def deleting_user(self,user_to_delete_id:int)->None:
        raise NotImplementedError()
    
    #### CHANNEL ####
    def get_channel_members(self,channel_id:int)->list[User]:
        raise NotImplementedError()
    def adding_member_to_channel(self, id_channel:int, id_member:int)->None:
        raise NotImplementedError()
    def creating_new_group(self, name:str, membres:list[int])->None:
        raise NotImplementedError()
    def deleting_user_from_channel(self,channel_id:int,personne_del_id:int)->None:
        raise NotImplementedError()
    
    #### MESSAGE ####
    def sending_message(self,sender_id:int,channel_id:int,content:str)->None:
        raise NotImplementedError()
    def deleting_message(self,id:int)->None:
        raise NotImplementedError()



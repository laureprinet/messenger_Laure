from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message
from server import Server


############# LES INTERACTIONS ###############
class Interaction:
    def __init__ (self, serv:Server):
                 self.server=serv

############# LE MENU PRINCIPAL ###################
    def choix_menu(self)->None:
        print('------------------------------------\n___________CHOIX MENU______________\n------------------------------------')
        print ('1.See users')
        print ('2.See channels')
        print ('3. See messages')
        print('x. Leave')
        print('------------------------------------')
        choice=input('Select an option: ')
        if choice=='x': 
            self.leave()
        elif choice=='1':
            self.choix_users()
        elif choice =='2':
            self.choix_channels()
        elif choice =='3':
            self.choix_messages()
        else :
            print('Unknown option:', choice)
            self.choix_menu()
    
    def leave(self)->None:
        print ('bye')
        return None

############ LES UTILISATEURS ##################

    def choix_users(self)->None:
        '''Les différents choix du menu user'''
        print('------------------------------------\n___________CHOIX USER______________\n------------------------------------')
        for user in self.server.get_user():
            print(user)
        print('------------------------------------')
        print('x. Main menu')
        print('n. create user')
        print('d. delete user')
        print('------------------------------------')
        choice_user=input('Enter an option: ')
        if choice_user=='n':
            self.add_user()
        elif choice_user=='d':
            self.delete_user()
        elif choice_user=='x':
            self.choix_menu()
        else:
            print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
            self.choix_users()

    def add_user(self)->None:
        '''Permet d'ajouter un nouveau contact'''
        nom=input('Choisir le nom du nouveau contact: ')
        self.server.adding_user(nom)
        print('------------------------------------')
        print ('a. add another user')
        print ('x. return to user menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.add_user()
        else :
            self.choix_users()

    def delete_user(self)->None:
        '''Permet de supprimer un utilisateur'''
        print('------------------------------------')
        id=int(input('Quel est l\'id de l\'utilisatueur à supprimer ?'))
        self.server.deleting_user(id)
        print('------------------------------------')
        print ('a. delete another user')
        print ('x. return to user menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            print('------------------------------------')
            self.delete_user()
        else :
            self.choix_users()

############ LES GROUPES #####################

    def choix_channels(self)->None:
        print('------------------------------------\n___________CHOIX CHANNEL______________\n------------------------------------')
        for channel in self.server.get_channel():
            print(channel)
        print('------------------------------------')
        print('x. Main menu')
        print('n. create channel')
        print('a. add a user to a channel')
        print ('b. delete user from a channel')
        print('c. display a channel')
        print('------------------------------------')
        choice_channels=input('Enter an option: ')
        if choice_channels=='n':
            self.new_groupe()
        elif choice_channels=='x':
            self.choix_menu()
        elif choice_channels=='a':
            self.add_member_to_channel()
        elif choice_channels=='b':
            self.delete_user_from_channel()
        elif choice_channels=='c':
            self.affichage_channel()
        else:
            print('Veuillez choisir une option dans celles existentes ')
            return self.choix_channels()

    def add_member_to_channel(self)->None:
        print('------------------------------------')
        groupe=int(input('Id du groupe pour ajouter: '))
        print('------------------------------------')
        for user in self.server.get_user():
            print(user)
        print('------------------------------------')
        personne_sup=int(input('Id de la personne à ajouter: '))
        self.server.adding_member_to_channel(groupe,personne_sup)  
        print('------------------------------------')
        print ('a. add another member to a channel')
        print ('x. return to channel menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.add_member_to_channel()
        else :
            self.choix_channels()

    def affichage_channel(self)->None:
        print('------------------------------------')
        groupe=int(input('Id du groupe à afficher: '))
        self.server.displaying_channel_members(groupe)
        print('------------------------------------')
        print ('a. display another channel')
        print ('x. return to channel menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.affichage_channel()
        else :
            self.choix_channels()

    def new_groupe(self)->None:
        print('------------------------------------')
        nom=input('Choisir un nom de groupe: ')
        print('------------------------------------')
        for user in self.server.get_user():
            print(User(user.id, user.name))
        print('------------------------------------')
        personnes=input('Rajouter les utilisateurs du groupe en listant leur id (ex : 1,2,5): ')
        member_ids=[int(id_str) for id_str in list(personnes.split(','))] #id des users sous forme de liste 
        self.server.creating_new_group(nom,member_ids)
        print('------------------------------------')
        print ('a. create another channel')
        print ('x. return to channel menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.new_groupe()
        else :
            self.choix_channels()

    def delete_user_from_channel(self)->None:
        print('------------------------------------')
        groupe_id=int(input('Id du groupe concerné: '))
        print('------------------------------------')
        print('Voici les membres du groupe')
        self.server.displaying_channel_members(groupe_id)
        print('------------------------------------')
        personne_del_id=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
        self.server.deleting_user_from_channel(groupe_id,personne_del_id)
        print('------------------------------------')
        print ('a. delete another user from a channel')
        print ('x. return to channel menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.delete_user_from_channel()
        else :
            self.choix_channels()
    
############ LES MESSAGES ##################

    def choix_messages(self)->None:
        print('------------------------------------\n___________CHOIX MESSAGE______________\n------------------------------------')
        for message in self.server.get_message():
            print(message)
        print('------------------------------------')
        print('x. Main menu')
        print('n. send a message')
        print ('d. delete a message')
        print('------------------------------------')
        choice_message=input('Enter an option: ')
        if choice_message=='n':
            self.send_message()
        elif choice_message=='x':
            self.choix_menu()
        elif choice_message=='d':
            self.delete_message()
        else:
            print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
            self.choix_messages()

    def send_message(self)->None: 
        print('------------------------------------')
        for channel in self.server.get_channel():
            print(channel)
        print('------------------------------------')
        channel_id = int(input('Id du groupe où envoyer le message : '))
        print('------------------------------------')
        print('Voici les utilisateurs dans le groupe :')
        self.server.displaying_channel_members(channel_id)
        print('------------------------------------')
        sender_id=int(input('Id de l\'expéditeur : '))
        content=input('Quel est le message à envoyer: ')
        self.server.sending_message(sender_id,channel_id,content)
        print('------------------------------------')
        print ('a. send another message')
        print ('x. return to message menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.send_message()
        else :
            self.choix_messages()

    def delete_message(self)->None:
        print('------------------------------------')
        id=int(input('Quel est l\'id du message à supprimer?'))
        self.server.deleting_message(id)
        print('------------------------------------')
        print ('a. delete another message')
        print ('x. return to message menu')
        reponse=input('Que voulez vous faire mtn?')
        if reponse=='a':
            self.delete_message()
        else :
            self.choix_messages()

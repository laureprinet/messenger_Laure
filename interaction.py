from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from user_channel_message import User, Channel, Message
from server import Server
from remoteserver import RemoteServer


############# LES INTERACTIONS ###############
class Interaction:
    def __init__ (self, serv:RemoteServer):
                 self.server=serv

############# LE MENU PRINCIPAL ###################
    def choix_menu(self):
        print ('1.See users')
        print ('2.See channels')
        print ('3. See messages')
        print('x. Leave')
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
    
    def leave(self):
        print ('bye')
        return None

############ LES UTILISATEURS ##################

    def choix_users(self):
        '''Les différents choix du menu user'''
        print('___________CHOIX UTILISATEUR______________')
        for user in self.server.get_user():
            print(User(user.id, user.name))
        print('x. Main menu')
        print('n. create user')
        print('d. delete user')
        choice_user=input('Enter an option: ')
        if choice_user=='n':
            self.add_user()
        # elif choice_user=='d':
        #     self.delete_user()
        elif choice_user=='x':
            self.choix_menu()
        else:
            print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
            self.choix_users()

    def add_user(self):
        '''Permet d'ajouter un nouveau contact'''
        id=max([user.id for user in self.server.get_user()])+1
        nom=input('Choisir le nom du nouveau contact: ')
        self.server.adding_user(nom)
        self.choix_users()

    # def delete_user(self):
    #     '''Permet de supprimer un utilisateur'''
    #     id=input('Quel est l\'id de l\'utilisatueur à supprimer ?')
    #     for user in self.server.get_user():
    #         if user.id==id:
    #             user_deleted=self.server.get_user().pop(user)
    #     print('Le contact supprimé est donc : ')
    #     print(User(user_deleted.id, user_deleted.name))
    #     self.server.save(SERVER_JSON_NAME) #On sauvegarde, comme on vient de modifier les données
    #     self.choix_users()

############ LES GROUPES #####################
    def choix_channels(self):
        for channel in self.server.get_channel():
            print(Channel(channel.id,channel.name, channel.member_ids))
        print('x. Main menu')
        print('n. create channel')
        print('a. add a user to a channel')
        print ('b. delete user from a channel')
        print('c. display a channel info')
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

    def add_member_to_channel(self):
        groupe=input('Id du groupe pour ajouter: ')
        for channel in self.server.get_channel():
            print(Channel(channel.id, channel.name, channel.member_ids))
        personne_sup=input('Id de la personne à ajouter: ')
        self.server.adding_member_to_channel(groupe,personne_sup)  
        self.choix_channels()

    def affichage_channel(self):
        groupe=input('Nom du groupe à afficher: ')
        for channel in self.server.get_channel():
            if channel.name==groupe:
                bon_channel=channel
                liste_user_de_bon_channel=[]
                for id in bon_channel.member_ids :
                    for user in self.server.get_user():
                        if user.id==id :
                            liste_user_de_bon_channel.append(user.name)  #Liste des noms des mebres du groupe
                print(bon_channel)
                print (liste_user_de_bon_channel)
                self.choix_channels()


    def new_groupe(self):
        nom=input('Choisir un nom de groupe: ')
        for user in self.server.get_user():
            print(User(user.id, user.name))
        personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
        member_ids=[int(id_str) for id_str in list(personnes.split(','))] #id des users sous forme de liste 
        self.server.creating_new_group(nom,member_ids)
        for channel in self.server.get_channel():
            print(channel)   #on réaffiche tous les groupes pour voir le nouveau
        self.choix_channels()

    def delete_user_from_channel(self):
        groupe=input('Nom du groupe concerné: ')
        for channel in self.server.get_channel():
            if channel.name==groupe:
                bon_channel=channel
        print (bon_channel.member_ids)  #afficher les user du groupe pour voir laquelle on veut enlever
        personne_del_id=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
        print(f'vous avez retirer l\'user avec id {bon_channel.member_ids.pop(personne_del_id)}. Voici alors les infos du groupe modifié :')
        print(Channel(bon_channel.id, bon_channel.name, bon_channel.member_ids))
        self.server.save()  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()
    #print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    #choix_channels()

############ LES MESSAGES ##################
    def choix_messages(self):
        for message in self.server.get_message():
            print(Message(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))
        print('x. Main menu')
        print('n. sen a message')
        print ('d. delete a message')
        choice_message=input('Enter an option: ')
        if choice_message=='n':
            self.send_message()
        elif choice_message=='x':
            self.choix_menu()
        elif choice_message=='d':
            self.delete_message()
        else:
            print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
            self.choix_users()

    def send_message(self): 
        for channel in self.server.get_channel():
            print(Channel(channel.id, channel.name, channel.member_ids))
        channel_id = input('Donner l\'id du groupe dans lequel le message sera envoyé')
        for channel in self.server.get_channel(): 
            if channel.id==channel_id:
                bon_channel=channel
        print('Voici les utilisateurs dans le groupe :')
        for id_user in bon_channel.member_ids:
            for user in self.server.get_user():
                if id_user==user.id:
                    print(User(user.id,user.name))
        sender_id=input('Donner l\'id de l\'expéditeur : ')
        content=input('Que voulez vous envoyer: ')
        reception_date=input('Quand envoyez-vous le message? (A remplir comme \'11h05, 05/05/24\')')
        id=max([message.id for message in self.server.get_message()])+1
        self.server.get_message().append(Message(id,reception_date,sender_id, channel_id, sender_id))
        for message in self.server.get_message():
            print(Message(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))   #on réaffiche tous les messages pour voir le nouveau apparaître
        self.server.save()  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()

    def delete_message(self):
        id=input('Quel est l\'id du message à supprimer?')
        for message in self.server.get_message():
            if message.id==id:
                bon_message=message
        print(f'Le message supprimé est donc : {bon_message.content}, envoyé par l\'utilisateur d\'id {bon_message.sender_id} ')
        self.server.save() #On sauvegarde, car les données ont été modifiées
        self.choix_menu()

from datetime import datetime
import json
import requests


# server = {
#     'users': [
#         {'id': 1, 'name': 'Alice'},
#         {'id': 2, 'name': 'Bob'}, 
#         {'id': 3, 'name': 'Third user'}

#     ],
#     'channels': [
#         {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
#     ],
#     'messages': [
#         {
#             'id': 1,
#             'reception_date': datetime.now(),
#             'sender_id': 1,
#             'channel': 1,
#             'content': 'Hi 👋'
#         }
#     ]
# }
# fichier=open('Server_json.json')
# server=json.load(fichier)

############## CREATION DES CLASSES ##################
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

class Messages:
    def __init__(self, id : int, reception_date : str, sender_id : int, channel_id : int, content :str):
        self.id=id
        self.reception_date=reception_date
        self.sender_id=sender_id
        self.channel_id=channel_id
        self.content=content
    def __repr__(self)->str:
        return f'Message (id = {self.id}, content = {self.content}, envoyé par l\'user d\'id {self.sender_id} ; channel = {self.channel_id}, date de réception = {self.reception_date})'
#Cette classe n'est pas encore utilisée dans le code... Les messages n'ont pas encore été pris en compte


############# LE SERVEUR #######################
class Server : 
    def __init__(self, name : str, users : list[User], channels : list[Channel], messages : list[Messages]):
        self.name=name
        self.users=users
        self.channels=channels
        self.messages=messages

    def __repr__(self) -> str :
        return f'Server(name={self.name}, users={self.users}, channels={self.channels})'

    
    def load_server(self,Server_json_name):          #On crée cette fonction afin de pouvoir la relancer plus tard ie pour relancer une variable au server si on l'a trop modifié dans une autre!
        with open(Server_json_name) as json_file:
            doc = json.load(json_file)
        
            self.users=[User(L['id'],L['name']) for L in doc['users']]     #j'ai créé data pour vraiment voir l'étape de copie qui ne me semblait pas évidente
        
            self.channels=[Channel(L['id'],L['name'],L['member_ids']) for L in doc['channels']]
        
            self.messages=[Messages(L['id'], L['reception_date'], L['sender_id'], L['channel_id'], L['content']) for L in doc['messages']]     

    def save(Server_json_name):
        server_json={}
        server_json['users']=[{'id':user.id,'name':user.name} for user in server.users]
        server_json['channels']=[{'id':channel.id,'name':channel.name, 'member_ids': channel.member_ids} for channel in server.channels]
        server_json['messages']=[{'id' : message.id, 'reception_date': message.reception_date, 'sender_id':message.sender_id, 'channel_id': message.channel_id, 'content':message.content} for message in server.messages]
        with open(Server_json_name, 'w') as file:
            json.dump(server_json, file)

    def get_user(self)->list[User]:
        return self.users
    
    def get_channel(self)->list[Channel]:
        return self.channels
    
    def get_message(self)->list[Messages]:
        return self.messages

class RemoteServer :
    def __init__(self,url):
        self.url=url

    def get_user(self)->list[User]:
        response_u = requests.get(self.url+'/users')
        response_u.json()
        return [User(user["id"], user["name"]) for user in response_u]

    def get_channel(self)->list[Channel]:
        response_c = requests.get(self.url+'/channels')
        response_c.json()
        return [Channel(channel["id"], channel["name"], channel["member_ids"]) for channel in response_c]

    def get_message(self)->list[Messages]:
        response_m= requests.get(self.url+'/messages')
        response_m.json()
        return [Messages(message["id"], message["reception_date"], message["sender_id"],message["channel_id"], message["content"]) for message in response_m]
    
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
        elif choice_user=='d':
            self.delete_user()
        elif choice_user=='x':
            self.choix_menu()
        else:
            print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
            self.choix_users()

    def add_user(self):
        '''Permet d'ajouter un nouveau contact'''
        nom=input('Choisir le nom du nouveau contact: ')
        id=max([user.id for user in self.server.get_user()])+1
        self.server.get_user().append(User(id,nom)) #dans Server mettre une fonction add.user
        for user in self.server.get_user():
            print(User(user.id, user.name))    #on réaffiche tous les users pour voir le nouveau apparaître
        self.server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()

    def delete_user(self):
        '''Permet de supprimer un utilisateur'''
        id=input('Quel est l\'id de l\'utilisatueur à supprimer ?')
        for user in self.server.get_user():
            if user.id==id:
                user_deleted=self.server.pop(user)
        print('Le contact supprimé est donc : ')
        print(Channel(user_deleted.id, user_deleted.name))
        self.server.save(SERVER_JSON_NAME) #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()

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
        groupe=input('Nom du groupe pour ajouter: ')
        for channel in self.server.get_channel():
            print(Channel(channel.id, channel.name, channel.member_ids))
        personne_sup=input('Id de la personne à ajouter: ')
        for channel in self.server.get_channel():
            if channel.name ==groupe:
                channel.member_ids.append(int(personne_sup))
                print(Channel(channel.id, channel.name, channel.member_ids))
        self.server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

    def affichage_channel(self):
        groupe=input('Nom du groupe à afficher: ')
        for channel in self.server.get_channel():
            if channel.name==groupe:
                bon_channel=channel
                liste_user_de_bon_channel=[]
                for id in bon_channel.member_ids :
                    for user in self.server.get_user():
                        if user.id==id :
                            liste_user_de_bon_channel.append(user.name)  #ajout du nom correspondant à l'user d'identifiant id
                print(Channel(channel.name, channel.id, channel.member_ids))
                print (liste_user_de_bon_channel)
                self.choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

    def new_groupe(self):
        nom=input('Choisir un nom de groupe: ')
        id=max([channel.id for channel in self.server.get_channel()])+1
        for user in self.server.get_user():
            print(User(user.id, user.name))
        personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
        member_ids=[int(id_str) for id_str in list(personnes.split(','))] #id des users sous forme de liste mais id en tant que int et pas string
        self.server.get_channel().append(Channel(id,nom,member_ids))
        for channel in self.server.get_channel():
            print(Channel(channel.id,channel.name,channel.member_ids))   #on réaffiche tous les groupes pour voir le nouveau
        self.server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()

    def delete_user_from_channel(self):
        groupe=input('Nom du groupe concerné: ')
        for channel in self.server.get_channel():
            if channel.name==groupe:
                bon_channel=channel
        print (bon_channel.member_ids)  #afficher les user du groupe pour voir laquelle on veut enlever
        personne_del_id=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
        print(f'vous avez retirer l\'user avec id {bon_channel.member_ids.pop(personne_del_id)}. Voici alors les infos du groupe modifié :')
        print(Channel(bon_channel.id, bon_channel.name, bon_channel.member_ids))
        self.server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()
    #print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    #choix_channels()

############ LES MESSAGES ##################
    def choix_messages(self):
        for message in self.server.get_message():
            print(Messages(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))
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
            for user in server.users:
                if id_user==user.id:
                    print(User(user.id,user.name))
        sender_id=input('Donner l\'id de l\'expéditeur : ')
        content=input('Que voulez vous envoyer: ')
        reception_date=input('Quand envoyez-vous le message? (A remplir comme \'11h05, 05/05/24\')')
        id=max([message.id for message in self.server.get_message()])+1
        self.server.get_message().append(Messages(id,reception_date,sender_id, channel_id, sender_id))
        for message in self.server.get_message():
            print(Messages(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))   #on réaffiche tous les messages pour voir le nouveau apparaître
        self.server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
        self.choix_menu()

    def delete_message(self):
        id=input('Quel est l\'id du message à supprimer?')
        for message in self.server.get_message():
            if message.id==id:
                bon_message=message
        print(f'Le message supprimé est donc : {bon_message.content}, envoyé par l\'utilisateur d\'id {bon_message.sender_id} ')
        self.server.save(SERVER_JSON_NAME) #On sauvegarde, car les données ont été modifiées
        self.choix_menu()


############## LANCEMENT #####################    
SERVER_JSON_NAME='Server_json.json'    
server=Server('Messenger',[],[],[])
server.load_server(SERVER_JSON_NAME)
#interaction=Interaction(server)
#interaction.choix_menu()


server_internet=RemoteServer('http://vps-cfefb063.vps.ovh.net/channels')
interaction=Interaction(server_internet)
interaction.choix_menu()

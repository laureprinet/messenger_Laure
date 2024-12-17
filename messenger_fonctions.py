from datetime import datetime
import json
import argparse

# Créer un objet ArgumentParser
parser = argparse.ArgumentParser()

# Ajouter un argument
parser.add_argument('-s', '--server', type=str, required=True, help="enter json path")

# Parser les arguments
args = parser.parse_args()

# Utiliser l'argument
print('Server json :', args.server)


SERVER_JSON_NAME=args.server
#'Server_json.json'  

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


############## CREATION DES CLASSES ####################

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

  
server=Server('Messenger',[],[],[])
server.load_server(SERVER_JSON_NAME)


class Interaction:
    def __init__ (self, serv : Server):
                 self.server=serv

#     def choix_menu():
#         print ('1.See users')
#         print ('2.See channels')
#         print ('3. See messages')
#         print('x. Leave')
#         choice=input('Select an option: ')
#         if choice=='x': 
#             leave()
#         elif choice=='1':
#             choix_users()
#         elif choice =='2':
#             choix_channels()
#         elif choice =='3':
#             choix_messages()
#         else :
#             print('Unknown option:', choice)
#             choix_menu()

#         def leave():
#             print ('bye')
#             return None

#         def choix_users():
#             '''Les différents choix du menu user'''
#             print('___________CHOIX UTILISATEUR______________')
#             for user in server['users']:
#                 print(User(user.id, user.name))
#             print('x. Main menu')
#             print('n. create user')
#             print('d. delete user')
#             choice_user=input('Enter an option: ')
#             if choice_user=='n':
#                 add_user()
#             elif choice_user=='d':
#                 delete_user()
#             elif choice_user=='x':
#                 choix_menu()
#             else:
#                 print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
#                 choix_users()



        

############# LE MENU PRINCIPAL #####################


def choix_menu():
    print ('1.See users')
    print ('2.See channels')
    print ('3. See messages')
    print('x. Leave')
    choice=input('Select an option: ')
    if choice=='x': 
        leave()
    elif choice=='1':
        choix_users()
    elif choice =='2':
        choix_channels()
    elif choice =='3':
        choix_messages()
    else :
        print('Unknown option:', choice)
        choix_menu()

def leave():
    print ('bye')
    return None

############ LES UTILISATEURS ##################

def choix_users():
    '''Les différents choix du menu user'''
    print('___________CHOIX UTILISATEUR______________')
    for user in server.users:
        print(User(user.id, user.name))
    print('x. Main menu')
    print('n. create user')
    print('d. delete user')
    choice_user=input('Enter an option: ')
    if choice_user=='n':
        add_user()
    elif choice_user=='d':
        delete_user()
    elif choice_user=='x':
        choix_menu()
    else:
        print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
        choix_users()

def add_user():
    '''Permet d'ajouter un nouveau contact'''
    nom=input('Choisir le nom du nouveau contact: ')
    id=max([user.id for user in server.users])+1
    server['users'].append(User(id,nom))
    for user in server.users:
        print(User(user.id, user.name))    #on réaffiche tous les users pour voir le nouveau apparaître
    server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()

def delete_user():
    '''Permet de supprimer un utilisateur'''
    id=input('Quel est l\'id de l\'utilisatueur à supprimer ?')
    for user in server.users:
        if user.id==id:
            user_deleted=server.pop(user)
    print('Le contact supprimé est donc : ')
    print(Channel(user_deleted.id, user_deleted.name))
    server.save(SERVER_JSON_NAME) #On sauvegarde, comme on vient de modifier les données
    choix_menu()


############ LES GROUPES #####################
def choix_channels():
    for channel in server.channels:
        print(Channel(channel.id,channel.name, channel.member_ids))
    print('x. Main menu')
    print('n. create channel')
    print('a. add a user to a channel')
    print ('b. delete user from a channel')
    print('c. display a channel info')
    choice_channels=input('Enter an option: ')
    if choice_channels=='n':
        new_groupe()
    elif choice_channels=='x':
        choix_menu()
    elif choice_channels=='a':
        add_member_to_channel()
    elif choice_channels=='b':
        delete_user_from_channel()
    elif choice_channels=='c':
        affichage_channel()
    else:
        print('Veuillez choisir une option dans celles existentes ')
        return choix_channels()

def add_member_to_channel():
    groupe=input('Nom du groupe pour ajouter: ')
    for channel in server.users:
        print(Channel(channel.id, channel.name, channel.member_ids))
    personne_sup=input('Id de la personne à ajouter: ')
    for channel in server.channels:
        if channel.name ==groupe:
            channel.member_ids.append(int(personne_sup))
            print(Channel(channel.id, channel.name, channel.member_ids))
    server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

def affichage_channel():
    groupe=input('Nom du groupe à afficher: ')
    for channel in server.channels:
        if channel.name==groupe:
            bon_channel=channel
            liste_user_de_bon_channel=[]
            for id in bon_channel.member_ids :
                for user in server.users:
                    if user.id==id :
                        liste_user_de_bon_channel.append(user.name)  #ajout du nom correspondant à l'user d'identifiant id
            print(Channel(channel.name, channel.id, channel.member_ids))
            print (liste_user_de_bon_channel)
            choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

def new_groupe():
    nom=input('Choisir un nom de groupe: ')
    id=max([channel.id for channel in server.channels])+1
    for user in server.users:
        print(User(user.id, user.name))
    personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
    member_ids=[int(id_str) for id_str in list(personnes.split(','))] #id des users sous forme de liste mais id en tant que int et pas string
    server.channels.append(Channel(id,nom,member_ids))
    for channel in server.channels:
        print(Channel(channel.id,channel.name,channel.member_ids))   #on réaffiche tous les groupes pour voir le nouveau
    server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()

def delete_user_from_channel():
    groupe=input('Nom du groupe concerné: ')
    for channel in server.channels:
        if channel.name==groupe:
            bon_channel=channel
    print (bon_channel.member_ids)  #afficher les user du groupe pour voir laquelle on veut enlever
    personne_del_id=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
    print(f'vous avez retirer l\'user avec id {bon_channel.member_ids.pop(personne_del_id)}. Voici alors les infos du groupe modifié :')
    print(Channel(bon_channel.id, bon_channel.name, bon_channel.member_ids))
    server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()
    #print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    #choix_channels()



############ LES MESSAGES ##################
def choix_messages():
    for message in server.messages:
        print(Messages(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))
    print('x. Main menu')
    print('n. sen a message')
    print ('d. delete a message')
    choice_message=input('Enter an option: ')
    if choice_message=='n':
        send_message()
    elif choice_message=='x':
        choix_menu()
    elif choice_message=='d':
        delete_message()
    else:
        print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
        choix_users()

def send_message(): 
    for channel in server.channels:
        print(Channel(channel.id, channel.name, channel.member_ids))
    channel_id = input('Donner l\'id du groupe dans lequel le message sera envoyé')
    for channel in server.channels: 
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
    id=max([message.id for message in server.messages])+1
    server.messages.append(Messages(id,reception_date,sender_id, channel_id, sender_id))
    for message in server.messages:
        print(Messages(message.id, message.reception_date, message.sender_id, message.channel_id, message.content))   #on réaffiche tous les messages pour voir le nouveau apparaître
    server.save(SERVER_JSON_NAME)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()

def delete_message():
    id=input('Quel est l\'id du message à supprimer?')
    for message in server.messages:
        if message.id==id:
            bon_message=message
    print(f'Le message supprimé est donc : {bon_message.content}, envoyé par l\'utilisateur d\'id {bon_message.sender_id} ')
    server.save(SERVER_JSON_NAME) #On sauvegarde, car les données ont été modifiées
    choix_menu()


############################################      
choix_menu()
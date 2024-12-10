from datetime import datetime
import json

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

##################################################
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


#################################################

Server_json_name='Server_json.json'

def load_server():          #On crée cette fonction afin de pouvoir la relancer plus tard ie pour relancer une variable au server si on l'a trop modifié dans une autre!
    with open(Server_json_name) as json_file:
        server = json.load(json_file)
        data_users=server['users'].copy()
        server['users']=[User(L['id'],L['name']) for L in data_users]     #j'ai créé data pour vraiment voir l'étape de copie qui ne me semblait pas évidente
        data_channels=server['channels'].copy()
        server['channels']=[Channel(L['id'],L['name'],L['member_ids']) for L in data_channels]
    return server     
#On a server['users']:list[dict]
#Transform server['users'] en list[User]

server=load_server()


#################################################


def choix_menu():
    print ('1.See users')
    print ('2.See channels')
    print('x. Leave')
    choice=input('Select an option: ')
    if choice=='x': 
        leave()
    elif choice=='1':
        choix_user()
    elif choice =='2':
        choix_channels()
    else :
        print('Unknown option:', choice)
        choix_menu()

def leave():
    print ('bye')
    return None

def choix_user():
    for user in server['users']:
        print(User(user.id, user.name))
    print('x. Main menu')
    print('n. create user')
    choice_user=input('Enter an option: ')
    if choice_user=='n':
        add_user()
    elif choice_user=='x':
        choix_menu()
    else:
        print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
        choix_user()

def add_user():
    nom=input('Choisir un nom: ')
    id=max([user.id for user in server['users']])+1
    server['users'].append(User(id,nom))
    for user in server['users']:
        print(User(user.id, user.name))    #on réaffiche tous les users pour voir le nouveau apparaître
    save()  #On sauvegarde, comme on vient de modifier les données
    choix_menu()

def choix_channels():
    for channel in server['channels']:
        print(Channel(channel.id,channel.name, channel.member_ids))
    print('x. Main menu')
    print('n. create channel')
    print('a. add a user to the channel')
    print('d. display a channel info')
    choice_channels=input('Enter an option: ')
    if choice_channels=='n':
        new_groupe()
    elif choice_channels=='x':
        choix_menu()
    elif choice_channels=='a':
        add_member_to_channel()
    elif choice_channels=='d':
        affichage_channel()
    else:
        print('Veuillez choisir une option dans celles existentes ')
        return choix_channels()


def add_member_to_channel():
    groupe=input('Nom du groupe pour ajouter: ')
    for channel in server['users']:
        print(Channel(channel.id, channel.name, channel.member_ids))
    personne_sup=input('Id de la personne à ajouter: ')
    for channel in server['channels']:
        if channel.name ==groupe:
            channel.member_ids.append(int(personne_sup))
            print(Channel(channel.id, channel.name, channel.member_ids))
    save(server)  #On sauvegarde, comme on vient de modifier les données
    choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

def affichage_channel():
    groupe=input('Nom du groupe à afficher: ')
    for channel in server['channels']:
        if channel.name==groupe:
            bon_channel=channel
            liste_user_de_bon_channel=[]
            for id in bon_channel.member_ids :
                for user in server['users']:
                    if user.id==id :
                        liste_user_de_bon_channel.append(user.name)  #ajout du nom correspondant à l'user d'identifiant id
            print(Channel(channel.name, channel.id, channel.member_ids))
            print (liste_user_de_bon_channel)
            choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()


def new_groupe():
    nom=input('Choisir un nom de groupe: ')
    id=max([channel.id for channel in server['channels']])+1
    for user in server['users']:
        print(User(user.id, user.name))
    personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
    member_ids=[int(id_str) for id_str in list(personnes.split(','))] #id des users sous forme de liste mais id en tant que int et pas string
    server['channels'].append(Channel(id,nom,member_ids))
    for channel in server['channels']:
        print(Channel(channel.id,channel.name,channel.member_ids))   #on réaffiche tous les groupes pour voir le nouveau
    save()  #On sauvegarde, comme on vient de modifier les données
    choix_menu()

def delete_user():
    groupe=input('Nom du groupe concerné: ')
    for channel in server['channels']:
        if channel.name==groupe:
            bon_channel=channel
    print (bon_channel.member_ids)  #afficher les user du groupe pour voir laquelle on veut enlever
    personne_del_id=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
    print(f'vous avez retirer l\'user avec id {bon_channel.member_ids.pop(personne_del_id)}. Voici alors les infos du groupe modifié :')
    print(Channel(bon_channel.id, bon_channel.name, bon_channel.member_ids))
    save()  #On sauvegarde, comme on vient de modifier les données
    choix_menu()
    #print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    #choix_channels()




def save():
    data_users=server['users'].copy()
    data_channels=server['channels'].copy()
    server_json={}
    server_json['users']=[{'id':user.id,'name':user.name} for user in data_users]
    server_json['channels']=[{'id':channel.id,'name':channel.name, 'member_ids': channel.member_ids} for channel in data_channels]
    with open(Server_json_name, 'w') as file:
        json.dump(server_json, file)
            
choix_menu()
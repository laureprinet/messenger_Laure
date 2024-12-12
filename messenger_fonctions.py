from datetime import datetime
import json
import argparse

# Créer un objet ArgumentParser
parser = argparse.ArgumentParser(description="Description de votre script.")

# Ajouter un argument
parser.add_argument('--argument', type=str, required=True, help="Description de l'argument.")

# Parser les arguments
args = parser.parse_args()

# Utiliser l'argument
print(f"Argument fourni : {args.argument}")

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
fichier=open('Server_json.json')
server=json.load(fichier)


def choix_menu():
    save()
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
    for d in server['users']:
        print(d['id'],'. ',d['name'])
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
    id=max([d['id'] for d in server['users']])+1
    server['users'].append({'id':id, 'name':(nom)})
    for d in server['users']:
        print(d['id'],'. ',d['name'])    #on réaffiche tous les users pour voir le nouveau apparaître
    choix_menu()

def choix_channels():
    for d in server['channels']:
        print(d['id'],'.',d['name'])
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
        add_channel()
    elif choice_channels=='d':
        affichage_channel()
    else:
        print('Veuillez choisir une option dans celles existentes ')
        return choix_channels()


def add_channel():
    groupe=input('Nom du groupe pour ajouter: ')
    for d in server['users']:
        print(d['id'],'. ',d['name'])
    personne_sup=input('Id de la personne à ajouter: ')
    for d in server['channels']:
        if d['name']==groupe:
            d['member_ids'].append(int(personne_sup))
            print(d)
            choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()

def affichage_channel():
    groupe=input('Nom du groupe à afficher: ')
    for d in server['channels']:
        if d['name']==groupe:
            print (d)
            choix_menu()
    # print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    # choix_channels()


def new_groupe():
    nom=input('Choisir un nom de groupe: ')
    id=max([d['id'] for d in server['channels']])+1
    for d in server['users']:
        print(d['id'],'. ',d['name'])
    personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
    L=[int(e) for e in list(personnes.split(','))] #id des users sous forme de liste mais id en tant que int et pas string
    server['channels'].append({'id':id, 'name':nom, 'member_ids':L})
    for d in server['channels']:
        print(d['id'],', ',d['name'])   #on réaffiche tous les groupes pour voir le nouveau
    choix_menu()

def delete_user():
    groupe=input('Nom du groupe concerné: ')
    for channel in server['channels']:
        if channel['name']==groupe:
            bon_channel=channel
    print (bon_channel['member_ids'])  #afficher les user du groupe pour voir laquelle on veut enlever
    personne_del=int(input('Id de la personne à retirer: ')) #int de l'id de la personne à supprimer
    print(f'vous avez retirer luser avec id {bon_channel['member_ids'].pop(personne_del)}. Voici alors les infos du groupe modifié')
    print(bon_channel)
    choix_menu()
    #print('Le nom de groupe est inexistant pour le moment. Veuillez choisir un groupe existant ou en créer un nouveau')
    #choix_channels()




def save():
    with open('Server_json.json', 'w') as file:
        json.dump(server, file)
            
choix_menu()
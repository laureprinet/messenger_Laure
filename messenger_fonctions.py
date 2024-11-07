from datetime import datetime

server = {
    'users': [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}, 
        {'id': 3, 'name': 'Third user'}

    ],
    'channels': [
        {'id': 1, 'name': 'Town square', 'member_ids': [1, 2]}
    ],
    'messages': [
        {
            'id': 1,
            'reception_date': datetime.now(),
            'sender_id': 1,
            'channel': 1,
            'content': 'Hi 👋'
        }
    ]
}




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
    for d in server['users']:
        print(d['id'],'. ',d['name'])
    print('x. Main leave')
    print('n. create user')
    choice_user=input('Enter an option: ')
    if choice_user not in ['x','n']:
        print('Votre choix ne correspond à aucune option existante. Veuillez recommencer')
        choix_user()
    elif choice_user=='x':
        choix_menu()
    else:           #le choix est 'n' donc ajout d'un user
        add_user()

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
    print('x. Main leave')
    print('n. create channel')
    print('a. add a user to the channel')
    print('d. display a channel info')
    choice_channels=input('Enter an option: ')
    if choice_channels not in ['x','n','a','d']:
        print('Veuillez choisir une option dans celles existentes ')
        return choix_channels()
    elif choice_channels=='x':
        choix_menu()
    elif choice_channels=='a':
        add_channel()
    elif choice_channels=='d':
        affichage_channel()
    else:                       #choice_channels='n' donc création d'un nouveau groupe
        new_groupe()


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

def affichage_channel():
    groupe=input('Nom du groupe à afficher: ')
    for d in server['channels']:
        if d['name']==groupe:
            print (d)
            choix_menu()

def new_groupe():
    nom=input('Choisir un nom de groupe: ')
    id=max([d['id'] for d in server['channels']])+1
    for d in server['users']:
        print(d['id'],'. ',d['name'])
    personnes=input('Rajouter les utilisateurs du groupe en listant leur id: ')
    server['channels'].append({'id':id, 'name':nom, 'member_ids':list(personnes)})
    for d in server['users']:
        print(d['id'],', ',d['name'])   #on réaffiche tous les groupes pour voir le nouveau
    choix_menu()


            
choix_menu()
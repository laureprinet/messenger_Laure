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
        print ('bye')
        return None
    elif choice=='1':
        for d in server['users']:
            print(d['id'],'. ',d['name'])
        print('x. Main leave')
        print('n. create user')
        choice_user=input('Enter an option: ')
        return choix_user(choice_user)
    elif choice =='2':
        for d in server['channels']:
            print(d['id'],'.',d['name'])
        print('x. Main leave')
        print('n. create channel')
        print('a. add a user to the channel')
        print('d. display a channel info')
        choice_channels=input('Enter an option: ')
        return choix_channels(choice_channels)
    else :
        print('Unknown option:', choice)
        choix_menu()


def choix_user(str):
    if str not in ['x','n']:
        choice3=input('Veuillez choisir une option entre n et x: ')
        return choix_user(choice3)
    elif str=='x':
        choix_menu()
    else:
        nom=input('Choisir un nom: ')
        id=max([d['id'] for d in server['users']])+1
        server['users'].append({'id':id, 'name':(nom)})
        for d in server['users']:
            print(d['id'],'. ',d['name'])
        choix_menu()

def choix_channels(str):
    if str not in ['x','n','a','d']:
        choice3=input('Veuillez choisir une option entre n, d, a et x: ')
        return choix_user(choice3)
    elif str=='x':
        choix_menu()
    elif str=='a':
        groupe=input('Nom du groupe pour ajouter: ')
        for d in server['users']:
            print(d['id'],'. ',d['name'])
        personne_sup=input('Id de la personne à ajouter: ')
        for d in server['channels']:
            if d['name']==groupe:
                d['member_ids'].append(personne_sup)
                choix_menu()
    elif str=='d':
        groupe=input('Nom du groupe à afficher: ')
        for d in server['channels']:
            if d['name']==groupe:
                print (d)
                choix_menu
    else:
        nom=input('Choisir un nom de groupe: ')
        id=max([d['id'] for d in server['channels']])+1
        for d in server['users']:
            print(d['id'],'. ',d['name'])
        personnes=input('Rajouter les utilisateurs du groupe sous forme de liste avec leur id: ')
        server['channels'].append({'id':id, 'name':nom, 'member_ids':personnes})
        for d in server['users']:
            print(d['id'],'. ',d['name'])
        choix_menu()


choix_menu()
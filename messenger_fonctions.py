from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from server import Server
from interaction import Interaction
from user_channel_message import User, Channel, Message
from remoteserver import RemoteServer
from localserver import LocalServer

argument_parser=ArgumentParser()
argument_parser.add_argument('-f','--filename')
argument_parser.add_argument('-u','--url')
#argument_parser.add_argument('-p','--portail')
action='store_true'
arguments=argument_parser.parse_args()
server: Server
if arguments.filename is not None :
    server = LocalServer(arguments.filename)
    server.load_server(server.filename)
elif arguments.url is not None :
    server=RemoteServer(arguments.url)
# elif arguments.portail is not None :
#     server=PortailServer()
else :
    print ("Error : -f or -u should be set")
    exit(-1)

interaction=Interaction(server)
interaction.choix_menu()

############## LANCEMENT ##################### 

## Si on veut lancer depuis un fichier local 
# SERVER_JSON_NAME='Server_json.json'    
# server=Server(SERVER_JSON_NAME)
# server.load_server(SERVER_JSON_NAME)

## Si on veut lancer depuis un serveur sur le web   
# server_internet=RemoteServer('https://groupe5-python-mines.fr')

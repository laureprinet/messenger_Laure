from datetime import datetime
import json
import requests
from argparse import ArgumentParser
from remoteserver import RemoteServer
#from portailserver import PortailServer
from server import Server
from interaction import Interaction
from user_channel_message import User, Channel, Message

# argument_parser=ArgumentParser()
# argument_parser.add_argument('f','--filename')
# argument_parser.add_argument('u','--url')
# argument_parser.add_argument('-p','--portail')
# action='store_true'
# arguments=argument_parser.parse_args()
# server: Server
# if arguments.filename is not None :
#     server = LocalServer(arguments.filename)
# elif arguments.url is not None :
#     server=RemoteServer(arguments.url)
# elif arguments.portail is not None :
#     server=PortailServer()
# else :
#     print ("Error : -f or -u should be set")
#     exit(-1)



############## LANCEMENT #####################    
SERVER_JSON_NAME='Server_json.json'    
server=Server(SERVER_JSON_NAME)
server.load_server(SERVER_JSON_NAME)


server_internet=RemoteServer('https://groupe5-python-mines.fr')
interaction=Interaction(server_internet)
interaction.choix_menu()

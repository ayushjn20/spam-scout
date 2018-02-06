from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from boards.models import *
from django.views.decorators.csrf import csrf_exempt
import facebook
import json
from py2neo import Graph, Node, Relationship, authenticate

#user_access_token
token="EAACEdEose0cBAAMqpl0oh1Ne58w11uxMDqsFIm8TZCPZBejYFI0GsD5ZBDmKJwnDL8E2IrEJqHYRwEDI5GhhkOS4gNJcOfFZA6sVbnwGtWCqRv6DL7oFtgXSHEyyDK588h0yro901POYN1IScZANMYW0tPxOwqcR2oauqo63hVZAXphHdhE80yg4CwN9iglQsZD"
graph = facebook.GraphAPI(access_token= token, version="2.11")

#this will return a dictionary of friends
friends = graph.get_connections(id='me', connection_name='friends')
friendList = friends['data']
print(type(friendList))
print(friendList[0].keys())  
 

@csrf_exempt
def home(request):
 if request.user.authenticate():
     #returns a node instance and creates if does not exits
     self = graph_db.get_or_create_indexed_node("me","fb_id","0")
     if request.method == 'POST':
         print(request.POST.keys())
         try:
             if(request.POST['id'] in [ d['id'] for d in friendList]):
               currentList=CurrentList(name=request.POST['name'], key=request.POST['id'])
               currentList.save()
               return HttpResponse("Success1!")
         except Exception as e:
            print(e)
            return HttpResponse("Failure1!")

     elif request.method == 'GET':
        return HttpResponse(json.dumps(friendList))



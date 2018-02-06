from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from boards.models import *
from django.views.decorators.csrf import csrf_exempt
import facebook
import json

#user_access_token
token="EAACEdEose0cBAH9PGHosKww8SArVtsxsFQQnDO4rZBcKBzSigXVy8GWoMkQId7h4svtdy6ANibATJPSHDDZCewgGcojwGl0ELX0gZCQZAMmx2rLOsTrwl5DrhPmcdZAuAzxS3lzoMljLqPH5Emb7fINl0Uxn0rnZAYvixZAtOujoDWGT3UMRo4OB2BxIM1n1FQZD"
graph = facebook.GraphAPI(access_token= token, version="2.11")

#this will return a dictionary of friends
friends = graph.get_connections(id='me', connection_name='friends')
friendList = friends['data']
print(type(friendList))
print(friendList[0].keys())  
 
#friends = graph.get_object("me/friends")
#write in trusted circle list
#graph.put_object

@csrf_exempt
def home(request):
#    template = loader.get_template('index.html')
#    return HttpResponse(template.render())\
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


from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from boards.models import *
from django.views.decorators.csrf import csrf_exempt
import facebook
import json

#user_access_token
token="EAACEdEose0cBAH9PGHosKww8SArVtsxsFQQnDO4rZBcKBzSigXVy8GWoMkQId7h4svtdy6ANibATJPSHDDZCewgGcojwGl0ELX0gZCQZAMmx2rLOsTrwl5DrhPmcdZAuAzxS3lzoMljLqPH5Emb7fINl0Uxn0rnZAYvixZAtOujoDWGT3UMRo4OB2BxIM1n1FQZD"
graph = facebook.GraphAPI(access_token= token, version="2.1")

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
      if(request.POST['id'] in [ d['id'] for d in friendList ] ):
        
        #Node creation
        """
        create_graph_connection(\
          {'name':(request.user.first_name + request.user.last_name),\
          'fb_id':request.user.facebook.fb_id}, \
          {'name': request.POST['name'],\
          'fb_id': request.POST['id']})
        """
        return HttpResponse("Success1!")
    
    except Exception as e:
      print(e)
      return HttpResponse("Failure1!")
  elif request.method == 'GET': 
    
    return HttpResponse(json.dumps(friendList))


@csrf_exempt
def rem_trust(request):
  if request.method == 'POST':
    print(request.POST.keys())

    #remove_connection()
    return HttpResponse("")
  else 


@csrf_exempt
def add_spam(request):
  if request.method == 'POST':
    print(request.POST.keys())
    try:
      Spam.objects.get_or_create(domain=request.POST['domain'])
    except KeyError:
      return HttpResponse("Invalid request")
    except Exception as e:
      return HttpResponse("")


@csrf_exempt
def rem_spam(request):
  if request.method == 'POST':
    print(request.POST.keys())
    try:
      Spam.objects.get_or_create(domain=request.POST['domain'])
    except KeyError:
      return HttpResponse("Invalid request")
    except Exception as e:
      return HttpResponse("")
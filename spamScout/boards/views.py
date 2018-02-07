from  django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from boards.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import facebook
import json
from py2neo import Graph, Node, Relationship, authenticate

#user_access_token
token="EAACEdEose0cBACQ4NzibFPZAg5zl7gkZAeiriZBgsrZBFMNyNS8f923I6Ch0R4kqKj7asV07qwhbQ6BzW2egryvbMo0ZCO4Y8O0ZAZAIRPeRZCcPZBLB2VcaGnw8qVaXgBHRxtRCRZCTbZAhnajpyAZC98slayk6T7ZBg0eo6EsDJShXI0uRB5gZBV0SVETKwgar6OA0TZCfu41WJ10KwZDZD"
graph_fb = facebook.GraphAPI(access_token= token, version="2.1")

#this will return a dictionary of friends
friends = graph_fb.get_connections(id='me', connection_name='friends')
friendList = friends['data']

# print(type(friendList))
# print(friendList[0].keys())  
try:
  authenticate("localhost:7474","neo4j","ayush123")
  graph = Graph("http://localhost:7474/db/data/")
except:
  pass

@csrf_exempt
def home(request):
  if True:
    
    try:
      fb_token = req.POST['token']
    except:
      try:
        fb_token = req.GET['token']
      except:
        return HttpResponse("Invalid Login")

    graph_fb = fb_authenticate(fb_token)
    if(not graph_fb):
      return HttpResponse("Invalid token")

    friends = graph_fb.get_connections(id='me', connection_name='friends')
    friendList = friends['data']

    me = graph_fb.get_object('me')

    trust_list = inner_circle(me)
    print(trust_list)
    #template = loader.get_template('index.html')
    #return HttpResponse(template.render())
    if request.method == 'POST':
      print(request.POST.keys())
      try:
        if(request.POST['id'] in [ d['id'] for d in friendList ] ):  
          #Node creation
          graph_connection(\
            {'name':(request.user.first_name + request.user.last_name),\
            'fb_id':request.user.facebook.fb_id},\
            {'name': request.POST['name'],\
            'fb_id': request.POST['id']}
            )
          return HttpResponse("Success1!")

        else: HttpResponse("Not ur friend!")      
      
      except Exception as e:
        print(e)
        return HttpResponse("Failure1!")
    
    elif request.method == 'GET': 
      spam_list = CustomUser.objects.get(user=request.user).spam_list
      print(spam_list)
      return HttpResponse(json.dumps({'friendList':friendList, 'trustList':trust_list}))
  
  else: return HttpResponse("Login")


@csrf_exempt
def rem_trust(request):
  if request.method == 'POST':
    print(request.POST.keys())
    remove_connection(me, {"name":request.POST['name'], "id":request.POST["fb_id"]})
    #remove_connection()
    return HttpResponse("")
  else: return Http404("Invalid request")


@csrf_exempt
def add_spam(request):
  if request.method == 'POST':
    print(request.POST.keys())
    try:
      Spam.objects.get_or_create(domain=request.POST['domain'])
    except KeyError:
      return HttpResponse("Invalid request")
    except Exception as e:
      return HttpResponse("Internal Server Error")
  else: return Http404("Invalid request")

@csrf_exempt
def rem_spam(request):

  if request.method == 'POST':
    print(request.POST.keys())
    try:
      spam = Spam.objects.get(domain = request.POST['domain'])
      CustomUser.objects.get(user=request.user).spam_list.remove(spam)
      return HttpResponse("Success!")
    except KeyError:
      return HttpResponse("Invalid request")
    except Exception as e:
      return HttpResponse("")
    if request.method == 'POST':
      print(request.POST.keys())


#queries to check for existing nodes and if exits create relation
def graph_connection(me, person, inFriendList):
  try:
    if(inFriendList):
    #if True: 
      try:
        r = graph.data("MATCH (a:Person),(b:Person) WHERE a.fb_id = '"+me['id']+"' AND b.fb_id = '"+person['id']+"' CREATE (a)-[r:KKNOWS]->(b) RETURN r")
        if(r):
          return True
      except Exception as e:
        return False
  except Exception as e:
      pass
  return False

# queries to remove connection

def remove_connection(me, person, inFriendList):
  try:
    if(inFriendList):
      r = graph.data("MATCH (a:Person { fb_id : '"+me['id']+"'})-[r:KKNOWS]->(b:Person { fb_id : '"+person['id']+"'}) DELETE r")
      if(r): return True
    else: return False
  
  except Exception as e:
    pass
  return False

# queries for taking inner circle

def inner_circle(me):
  try:
    d = graph.data("MATCH (a:Person {fb_id : '"+me['id']+"'})-[:KKNOWS]->(b) RETURN b")
    return d
  except:
    return None
  # try:
  #   trust_list = graph.match_incoming(rel_type='KKNOWS', start_node=me[id],limit=None)
  #   return trust_list
  # except Exception as e:
  #   return False
  

def circle2(me):
  try:
    first_list = inner_circle(me)
    outer_list = []
    for person in first_list:
      outer_list += inner_circle(person)
    
    return {"inner":first_list,"outer":outer_list}
  except:
    return False

def community_score(me, domain):

  #inner --> 2x
  #outer --> x
  circles = circle2(me)
  n = len(circles['inner'])
  m = len(circles['outer'])
  x = 100/(2*n+1)

  score = 0
  for person in circles['inner']:
    spamList1 = CustomUser.objects.get(fb_id=person['id']).spam_list__set.all()
    if(domain in spamList1):
      score += 2*x

  for person in circles['outer']:
    spamList2 = CustomUser.objects.get(fb_id=person['id']).spam_list__set.all()
    if(domain in spamList2):
      score += x
  return score

def check_existence(person):
  n = graph.data("MATCH (a:Person) WHERE a.fb_id = '"+person['id']+"' RETURN a")
  if(n):
    return True
  else: return False

def add_node(person):
  try:
    n = graph.data("CREATE (n:Person { name: '"+person['name']+"', fb_id: '"+person['id']+"' })")
    if(n): return True
    else: return False
  except:
    return False


def fb_authenticate(access_token):
  try:
    return facebook.GraphAPI(access_token= access_token, version="2.1")

  except:
    try:
      return facebook.GraphAPI(access_token= access_token, version="2.0")

    except:
      try:
        return facebook.GraphAPI(access_token= access_token, version="2.2")

      except:
        return False
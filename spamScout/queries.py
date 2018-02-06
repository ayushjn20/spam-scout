#queries to check for existing nodes and if exits create relation

def graph_connection():
  if request.method == 'POST':
    try:
      if(request.POST['id'] in [ d['id'] for d in friendList]):
        node_me = graph.find_one('friends', property_key='id', property_value=1)
        existing_node = graph.find_one('friends', property_key='id', property_value=2)

        trust_node = Relationship(node_me, 'KKNOWS', existing_node)
        graph.create(trust_node)

        return HttpResponse('relation created');

    except Exception as e:
        return HttpResponse('failed');
  elif request.method == 'GET':
    return HttpResponse(json.dumps(friendList))

# queries to remove connection

def remove_connection():
  if request.method == 'POST':
    try:
      if(request.POST['id'] in [ d['id'] for d in friendList]):
       existing_node1 = graph.find_one('friends', property_key='id', property_value=2)
       graph.delete('KKNOWS')

       return HttpResponse('relation created');

    except Exception as e:
      return HttpResponse('failed');
  elif request.method == 'GET':
    return HttpResponse(json.dumps(friendList))

# queries for taking inner circle

def inner_circle():
  if request.method == 'POST':
    try:
      if(request.POST['id'] in [ d['id'] for d in friendList]):
        

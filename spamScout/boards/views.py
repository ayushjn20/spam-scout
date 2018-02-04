from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import facebook

graph = facebook.GraphAPI(access_token= "EAACEdEose0cBAIzaLNu4P3ddhUWBjoNbTwzieolzrhJnxubWQlWLnxbJyPfurRkbuOLKdbGc3pavcmGWv3dpRocZBbMpCTu97DNHcvEISJXzEJB7wAM8GvGLVh1fvPjXQRxf9YwqEg8eWC6Ms0zDWpjTwK0Fo7gjoQ3KUPZBg3D1MyCsaNlbpQOiW2qS3Bqk6t7KouNgZDZD", version="2.11")
friends = graph.get_connections(id='me', connection_name='friends')

def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

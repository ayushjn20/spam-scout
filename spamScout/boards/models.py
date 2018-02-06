from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
#    UniqueIdProperty, RelationshipTo, RelationshipFrom)

#config.DATABASE_URL = 'bolt://neo4j:ratina@localhost:7687'

import facebook
import json

class CustomUser(models.Model):
  user = models.OneToOne(User)
  fb_id = models.CharField(max_length=30)
  spam_list = models.OneToMany(Spams)
  fb_token = models.CharField(max_length=500)


class CurrentList(models.Model):
  key = models.IntegerField(default="0")
  name = models.CharField(max_length=30)

  def __str__(self):
    return self.name


class Spam(models.Model)
  domain = models.UUIDField(default=uuid.uuid4) 


"""
@receiver(post_save, sender=CurrentList)
def current(sender, instance, **kwargs):
    
    if instance is not None:
       graph = neo4j.Graph('http://localhost:7474/db/data')
       query = '''
       CREATE (n:CurrentList {name: {name}})
       '''
       graph.cypher.execute(query, name=instance.name)

#class Trustlist(models.Model):
#      key = models.IntegerField(default="0")
#      name = models.CharField(max_length=30)

#      def __str__(self):
#          return self.name
"""

from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
#    UniqueIdProperty, RelationshipTo, RelationshipFrom)

#config.DATABASE_URL = 'bolt://neo4j:ratina@localhost:7687'

import facebook
import json

class CurrentList(models.Model):

      key = models.IntegerField(default="0")
      name = models.CharField(max_length=30)

      def __str__(self):
          return self.name
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

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


class Spam(models.Model):
  domain = models.CharField(max_length=30, unique=True)


class CustomUser(models.Model):
  user = models.OneToOneField(User)
  fb_id = models.CharField(max_length=30)
  spam_list = models.ManyToManyField(Spam)
  fb_token = models.CharField(max_length=500)
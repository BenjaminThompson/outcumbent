from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Topic(models.Model):
    URL = models.TextField(max_length=500)
    poster = models.ForeignKey(User, related_name='+')
    dateCreated = models.DateTimeField()

    def __unicode__(self):
        return '%s' % (self.URL)

class TopicRemark(models.Model):
    topic = models.ForeignKey(Topic, related_name='+')
    writer = models.ForeignKey(User, related_name='+')
    dateCreated = models.DateTimeField()
    remarks = models.TextField(max_length=5000)

    def __unicode__(self):
        return '%s' % (self.remarks[:100])

class TopicVote(models.Model):
    topic = models.ForeignKey(Topic, related_name='+')
    voter = models.ForeignKey(User, related_name='+')
    dateCreated = models.DateTimeField()
    vote = models.SmallIntegerField()

class Tag(models.Model):
    text = models.TextField(max_length=128, unique=True)

    def __unicode__(self):
        return '%s' % (self.text)

class TopicTag(models.Model):
    topic = models.ForeignKey(Topic, related_name='+')
    tagger = models.ForeignKey(User, related_name='+')
    tag = models.ForeignKey(Tag, related_name='+')

class UserTag(models.Model):
    user = models.ForeignKey(User, related_name='+')
    tagger = models.ForeignKey(User, related_name='+')
    tag = models.ForeignKey(Tag, related_name='+')

admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(TopicRemark)
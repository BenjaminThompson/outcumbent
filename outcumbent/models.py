from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Tag(models.Model):
    text = models.TextField(max_length=128, unique=True)

    def __unicode__(self):
        return '%s' % (self.text)

class UserTag(models.Model):
    user = models.ForeignKey(User, related_name='+')
    tagger = models.ForeignKey(User, related_name='+')
    tag = models.ForeignKey(Tag, related_name='+')

    def __unicode__(self):
        return '%s' % (self.user+":"+self.tag)

class Chamber(models.Model):
    name = models.TextField(max_length=6)

    def __unicode__(self):
        return '%s' % (self.name)

class Party(models.Model):
    name = models.TextField(max_length=127)

    def __unicode__(self):
        return '%s' % (self.name)

class Legislator(models.Model):
    user = models.ForeignKey(User, related_name='+')
    chamber = models.ForeignKey(Chamber, related_name='+')
    firstName = models.TextField(max_length=100)
    lastName = models.TextField(max_length=100)
    party = models.ForeignKey(Party, related_name='+')
    identifier = models.TextField(max_length=50)

    def __unicode__(self):
        return '%s' % (self.identifier)

class Legislation(models.Model):
    rollCallNum = models.IntegerField()
    congress = models.IntegerField()
    session = models.SmallIntegerField()
    chamber = models.ForeignKey(Chamber, related_name='+')
    identifier = models.TextField(max_length=50)
    title = models.TextField()
    description = models.TextField(max_length=100)
    hyperlink = models.TextField()

    def __unicode__(self):
        return '%s' % (self.title)

class LegislationUserVote(models.Model):
    legislation = models.ForeignKey(Legislation, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    dateCreated = models.DateTimeField()
    vote = models.SmallIntegerField()

class LegislationLegislatorVote(models.Model):
    legislation = models.ForeignKey(Legislation, related_name='+')
    legislator = models.ForeignKey(Legislator, related_name='+')
    dateCreated = models.DateTimeField()
    vote = models.SmallIntegerField()

class LegislationUserTag(models.Model):
    legislation = models.ForeignKey(Legislation, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    tag = models.ForeignKey(Tag, related_name='+')

class LegislationUserRemark(models.Model):
    legislation = models.ForeignKey(Legislation, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    dateCreated = models.DateTimeField()
    remarks = models.TextField(max_length=5000)

    def __unicode__(self):
        return '%s' % (self.remarks[:100])



admin.site.register(Tag)
admin.site.register(Chamber)
admin.site.register(Party)
admin.site.register(Legislator)
admin.site.register(Legislation)
admin.site.register(LegislationUserVote)
admin.site.register(LegislationLegislatorVote)
admin.site.register(LegislationUserTag)
admin.site.register(LegislationUserRemark)

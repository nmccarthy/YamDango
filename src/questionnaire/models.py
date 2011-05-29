from django.db import models
from django import forms
from django.contrib.auth.models import User

#standard models
class Product(models.Model):
    displayName = models.CharField(max_length=70)
    uniqueName = models.CharField(max_length=35)

    def __unicode__(self):
        return self.displayName

class Questionnaire(models.Model):
    name = models.CharField(max_length=35)
    product = models.ForeignKey(Product)
      
    def __unicode__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=140)
    questionnaire = models.ForeignKey(Questionnaire)
    sortOrder = models.IntegerField()
    
    def __unicode__(self):
        return self.text

class ResponseSet(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    responder = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.timestamp)

class Response(models.Model):
    text = models.CharField(max_length=280)
    question = models.ForeignKey(Question)
    responseSet = models.ForeignKey(ResponseSet)

    def __unicode__(self):
        return self.text

class PendingUser(models.Model):
    inviteEmail = models.EmailField('User who was invited', blank=True)
    inviter = models.ForeignKey(User, blank=True)

    def __unicode__(self):
        return self.inviteEmail

#forms models
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=35)
    password = forms.CharField()

    def __unicode__(self):
        return self.signupName

class InviteForm(forms.Form):
    email = forms.EmailField(max_length=35)
    
    def __unicode__(self):
        return self.username
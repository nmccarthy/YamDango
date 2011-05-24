from django.db import models

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

class Response(models.Model):
    text = models.CharField(max_length=280)
    question = models.ForeignKey(Question)
    
    def __unicode__(self):
        return self.text

class Responder(models.Model):
    name = models.CharField(max_length=35)
    company = models.CharField(max_length=35)
    email = models.CharField(max_length=35)
    
    def __unicode__(self):
        return self.name

class ResponseSet(models.Model):
    date = models.DateTimeField('Date Submitted')
    responder = models.ForeignKey(Responder)
    
    def __unicode__(self):
        return self.date
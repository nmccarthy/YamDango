from django.shortcuts import render_to_response
from questionnaire.models import Questionnaire, Question, Product

def index(request):
    
    #count questions in various questionnaires by finding its product. Product found based on uniqueName field.
    #because of annoying no JOIN rules for Django on App Engine, the following logic is all I could figure out.
    uName = 'adsync'
    if Product.objects.filter(uniqueName=uName):
        productId = Product.objects.values().filter(uniqueName=uName).get()['id']
        if Questionnaire.objects.filter(product__id=productId):
            questionnaireId = Questionnaire.objects.values().filter(product__id=productId).get()['id']
            if Question.objects.filter(questionnaire__id=questionnaireId):
                numADQuestions = Question.objects.filter(questionnaire__id=questionnaireId).count()
            else:
                numADQuestions = 0
        else:
            numADQuestions = 0
    else:
        numADQuestions = 0

    uName = 'sharepoint'
    if Product.objects.filter(uniqueName=uName):
        productId = Product.objects.values().filter(uniqueName=uName).get()['id']
        if Questionnaire.objects.filter(product__id=productId):
            questionnaireId = Questionnaire.objects.values().filter(product__id=productId).get()['id']
            if Question.objects.filter(questionnaire__id=questionnaireId):
                numSPQuestions = Question.objects.filter(questionnaire__id=questionnaireId).count()
            else:
                numSPQuestions = 0
        else:
            numSPQuestions = 0
    else:
        numSPQuestions = 0

    uName = 'sso'
    if Product.objects.filter(uniqueName=uName):
        productId = Product.objects.values().filter(uniqueName=uName).get()['id']
        if Questionnaire.objects.filter(product__id=productId):
            questionnaireId = Questionnaire.objects.values().filter(product__id=productId).get()['id']
            if Question.objects.filter(questionnaire__id=questionnaireId):
                numSSOQuestions = Question.objects.filter(questionnaire__id=questionnaireId).count()
            else:
                numSSOQuestions = 0
        else:
            numSSOQuestions = 0
    else:
        numSSOQuestions = 0

    return render_to_response('questionnaire/index.html',
                              {'numADQuestions': numADQuestions,
                               'numSPQuestions': numSPQuestions,
                               'numSSOQuestions': numSSOQuestions})

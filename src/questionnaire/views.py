from django.shortcuts import render_to_response
from questionnaire.models import Questionnaire, Question, SignUpForm, InviteForm, PendingUser, Response, ResponseSet
from django.template import Context, RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import datetime

distroEmails = ['nmccarthy@yammer-inc.com']

def sandbox(request):
    deletemes = Response.objects.all()
    
    for deleteme in deletemes:
        deleteme.delete()
    
    deletemes = ResponseSet.objects.all()
    
    for deleteme in deletemes:
        deleteme.delete()

    return HttpResponseRedirect('/')

def registration(request):

    #if user is already signed in, no need to sign up again
    if request.user.is_active:
        return HttpResponseRedirect('/')

    try:
        signUpEmail = request.GET.getlist('email')[0]
    except:
        raise Http404

    #has the user previously signed up?
    if User.objects.filter(email = signUpEmail):
        return render_to_response('error/alreadySignedUp.html', context_instance = RequestContext(request))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            newUser = form.save()
            newUser.email = signUpEmail
            newUser.save()
            newUser.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, newUser)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('registration/register.html',
                              {'form': form,
                               'signUpEmail': signUpEmail,
                               },
                              context_instance = RequestContext(request))

@login_required
def invite(request):

    if request.user.is_staff:
        if request.method == 'POST':
            form = InviteForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                if PendingUser.objects.filter(inviteEmail=email) or User.objects.filter(email=email):
                    return render_to_response('error/duplicateInvite.html')
                else:
                    pu = PendingUser(inviteEmail = email, inviter = request.user)
                    pu.save()

                form = InviteForm()

                #point to email templates
                plaintext = get_template('email/invite.txt')
                htmly = get_template('email/invite.html')

                #pass email address to email template
                d = Context({ 'email': email})

                #build email components
                subject, from_email = 'Yammer Integration Downloads', 'nmccarthy@yammer-inc.com'
                text_content = plaintext.render(d)
                html_content = htmly.render(d)

                #build email
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
        else:
            form = InviteForm()
    else:
        return HttpResponseRedirect('/')

    return render_to_response("invitation/invite.html",
                              {'form': form},
                              context_instance = RequestContext(request))

@login_required
def index(request):
    
    #count questions in various questionnaires by finding its product. Product found based on uniqueName field.
    #the JOIN-based queries below only work because of the dbindexer configuration from http://www.allbuttonspressed.com/blog/django/joins-for-nosql-databases-via-django-dbindexer-first-steps
    adName = 'adsync'
    numADQuestions = Question.objects.filter(questionnaire__product__uniqueName=adName).count()

    spName = 'sharepoint'
    numSPQuestions = Question.objects.filter(questionnaire__product__uniqueName=spName).count()

    ssoName = 'sso'
    numSSOQuestions = Question.objects.filter(questionnaire__product__uniqueName=ssoName).count()

    return render_to_response('questionnaire/index.html',
                              {'numADQuestions': numADQuestions,
                               'numSPQuestions': numSPQuestions,
                               'numSSOQuestions': numSSOQuestions,
                               }, context_instance = RequestContext(request))

@login_required
def adsyncQuestionnaire(request):

    if request.method == 'POST':
    #if the form is being submitted
        responses = []      #prep responses as an empty list; will be used for email template variables
        queryObject = request.POST.copy()
        rSet = ResponseSet(responder = request.user)
        rSet.save()
        for param in queryObject:
            if param[:8] == 'response':
                try:
                    question = Question.objects.filter(id=param[8:])[0]
                    response = Response(text = queryObject[param], question = question, responseSet = rSet)
                    response.save()

                    #build a dictionary to be passed to the email template
                    responses.append({'q': question.text, 'r': response.text})
                except:
                    raise Http404

        #point to email templates
        plaintext = get_template('email/response.txt')
        htmly = get_template('email/response.html')

        #pass variables to email template
        d = Context({ 'responses': responses, 'questionnaireName': question.questionnaire.name, 'submitter': request.user.username, 'submitterEmail':request.user.email })

        #build email components
        subject = request.user.email + ' responded to the ' + question.questionnaire.name
        from_email = 'nmccarthy@yammer-inc.com'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)

        #build email
        msg = EmailMultiAlternatives(subject, text_content, from_email, distroEmails)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return HttpResponseRedirect('/questionnaires/adsync/download')
    else:
    #if the form is being accessed via a GET Method
        #prod is the uniqueName field in the Product Model.
        prod = 'adsync'
        adQuestions = Question.objects.filter(questionnaire__product__uniqueName=prod).order_by('sortOrder')

        questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)

        #get questions for questionnaire
        try:
            questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)[0]
        except:
            raise Http404

    return render_to_response('questionnaire/adsyncQuestionnaire.html',
                              {'adQuestions': adQuestions,
                               'questionnaire': questionnaire
                               }, context_instance = RequestContext(request))

@login_required
def sharepointQuestionnaire(request):

    if request.method == 'POST':
    #if the form is being submitted
        responses = []      #prep responses as an empty list; will be used for email template variables
        queryObject = request.POST.copy()
        rSet = ResponseSet(responder = request.user)
        rSet.save()
        for param in queryObject:
            if param[:8] == 'response':
                try:
                    question = Question.objects.filter(id=param[8:])[0]
                    response = Response(text = queryObject[param], question = question, responseSet = rSet)

                    #build a dictionary to be passed to the email template
                    responses.append({'q': question.text, 'r': response.text})
                    response.save()
                except:
                    raise Http404

        #point to email templates
        plaintext = get_template('email/response.txt')
        htmly = get_template('email/response.html')

        #pass variables to email template
        d = Context({ 'responses': responses, 'questionnaireName': question.questionnaire.name, 'submitter': request.user.username, 'submitterEmail':request.user.email })

        #build email components
        subject = request.user.email + ' responded to the ' + question.questionnaire.name
        from_email = 'nmccarthy@yammer-inc.com'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)

        #build email
        msg = EmailMultiAlternatives(subject, text_content, from_email, distroEmails)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return HttpResponseRedirect('/questionnaires/sharepoint/download')
    else:
    #if the form is being accessed via a GET Method
        #prod is the uniqueName field in the Product Model.
        prod = 'sharepoint'
        spQuestions = Question.objects.filter(questionnaire__product__uniqueName=prod).order_by('sortOrder')
    
        questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)
    
        #get questions for questionnaire
        try:
            questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)[0]
        except:
            raise Http404

    return render_to_response('questionnaire/sharepointQuestionnaire.html',
                              {'spQuestions': spQuestions,
                               'questionnaire': questionnaire
                               }, context_instance = RequestContext(request))

@login_required
def ssoQuestionnaire(request):
    
    if request.method == 'POST':
    #if the form is being submitted
        responses = []      #prep responses as an empty list; will be used for email template variables
        queryObject = request.POST.copy()
        rSet = ResponseSet(responder = request.user)
        rSet.save()
        for param in queryObject:
            if param[:8] == 'response':
                try:
                    question = Question.objects.filter(id=param[8:])[0]
                    response = Response(text = queryObject[param], question = question, responseSet = rSet)

                    #build a dictionary to be passed to the email template
                    responses.append({'q': question.text, 'r': response.text})
                    response.save()
                except:
                    raise Http404
        #point to email templates
        plaintext = get_template('email/response.txt')
        htmly = get_template('email/response.html')

        #pass variables to email template
        d = Context({ 'responses': responses, 'questionnaireName': question.questionnaire.name, 'submitter': request.user.username, 'submitterEmail':request.user.email })

        #build email components
        subject = request.user.email + ' responded to the ' + question.questionnaire.name
        from_email = 'nmccarthy@yammer-inc.com'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)

        #build email
        msg = EmailMultiAlternatives(subject, text_content, from_email, distroEmails)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return HttpResponseRedirect('/questionnaires/sso/download')
    else:
    #if the form is being accessed via a GET Method
        #prod is the uniqueName field in the Product Model.
        prod = 'sso'
        ssoQuestions = Question.objects.filter(questionnaire__product__uniqueName=prod).order_by('sortOrder')
    
        questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)
    
        #get questions for questionnaire
        try:
            questionnaire = Questionnaire.objects.filter(product__uniqueName=prod)[0]
        except:
            raise Http404

    return render_to_response('questionnaire/ssoQuestionnaire.html',
                              {'ssoQuestions': ssoQuestions,
                               'questionnaire': questionnaire
                               }, context_instance = RequestContext(request))
@login_required
def adSyncDownload(request):

    return render_to_response('questionnaire/adSyncDownload.html', context_instance = RequestContext(request))

@login_required
def sharepointDownload(request):

    return render_to_response('questionnaire/sharepointDownload.html', context_instance = RequestContext(request))

@login_required
def ssoDownload(request):

    return render_to_response('questionnaire/ssoDownload.html', context_instance = RequestContext(request))
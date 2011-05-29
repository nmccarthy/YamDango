from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()
handler500 = 'djangotoolbox.errorviews.server_error'
handler404 = 'questionnaire.views.notFound'

urlpatterns = patterns('',
    (r'^$', 'questionnaire.views.index'),
    (r'^questionnaires/adsync$', 'questionnaire.views.adsyncQuestionnaire'),
    (r'^questionnaires/sharepoint$', 'questionnaire.views.sharepointQuestionnaire'),
    (r'^questionnaires/sso$', 'questionnaire.views.ssoQuestionnaire'),
    (r'^questionnaires/adsync/download$', 'questionnaire.views.adSyncDownload'),
    (r'^questionnaires/sharepoint/download$', 'questionnaire.views.sharepointDownload'),
    (r'^questionnaires/sso/download$', 'questionnaire.views.ssoDownload'),
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^accounts/login', login),
    (r'^accounts/logout', logout),
    (r'^accounts/signup', 'questionnaire.views.registration'),
    (r'^invite', 'questionnaire.views.invite'),
#    (r'^sandbox$', 'questionnaire.views.sandbox'),
    (r'^qadmin/', include(admin.site.urls)),
)
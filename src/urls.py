from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()
handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$', 'questionnaire.views.index'),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',{'template': 'home.html'}),
    (r'^qadmin/', include(admin.site.urls)),
)

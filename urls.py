from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# handler403 is used as one view like handler404
#
#def handler403(request,exception):
#  from django.http import HttpResponseForbidden
#  return HttpResponseForbidden("handler@!!!!")

urlpatterns = patterns('',
    # Example:
    (r'^$','http403.views.testview'),
    (r'^403view/$','http403.views.Http403View'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

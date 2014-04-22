from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'outcumbent.views.home'),
    url(r'^api/$', 'outcumbent.views.api'),
    url(r'^login/$', 'outcumbent.views.loginpage'),
    url(r'^logout/$', 'outcumbent.views.logoutpage'),
    url(r'^topic/$', 'outcumbent.views.topic'),
    url(r'^profile/$', 'outcumbent.views.profile'),
    url(r'^register/$', 'outcumbent.views.register'),

    url(r'^admin/', include(admin.site.urls)),
)

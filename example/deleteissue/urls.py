from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^step1/', 'deleteissue.views.step1'),
    url(r'^step2/', 'deleteissue.views.step2'),
)

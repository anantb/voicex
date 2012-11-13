from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','http_handler.views.index'),
    url(r'^index', 'http_handler.views.index'),
    url(r'^voicex_us', 'http_handler.views.voicex_us'),
    url(r'^mungano_us', 'http_handler.views.mungano_us'),
    url(r'^voicex_ke', 'http_handler.views.voicex_ke'),
    url(r'^mungano_ke', 'http_handler.views.mungano_ke')
)

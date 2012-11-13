from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','query_handler.views.index'),
    url(r'^index', 'query_handler.views.index'),
    url(r'^voicex_us', 'query_handler.views.voicex_us'),
    url(r'^mungano_us', 'query_handler.views.mungano_us'),
    url(r'^voicex_ke', 'query_handler.views.voicex_ke'),
    url(r'^mungano_ke', 'query_handler.views.mungano_ke')
)

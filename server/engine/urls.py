from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','engine.views.index'),
    url(r'^index', 'engine.views.index'),
    url(r'^voicex_us', 'engine.views.voicex_us'),
    url(r'^mungano_us', 'engine.views.mungano_us'),
    url(r'^voicex_ke', 'engine.views.voicex_ke'),
    url(r'^mungano_ke', 'engine.views.mungano_ke')
)

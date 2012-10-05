from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','voicex.views.index'),
    url(r'^index', 'voicex.views.index'),
    url(r'^voicex/us', 'voicex.views.voicex_us'),
    url(r'^mungano/us', 'voicex.views.mungano_us'),
    url(r'^voicex/ke', 'voicex.views.voicex_ke'),
    url(r'^mungano/ke', 'voicex.views.mungano_ke'),
    url(r'^voicex$', 'voicex.views.voicex_us'),
    url(r'^mungano$', 'voicex.views.mungano_us')
)

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$','voicex.views.index'),
    url(r'^index', 'voicex.views.index'),
    url(r'^voicex_us', 'voicex.views.voicex_us'),
    url(r'^mungano_us', 'voicex.views.mungano_us'),
    url(r'^voicex_ke', 'voicex.views.voicex_ke'),
    url(r'^mungano_ke', 'voicex.views.mungano_ke')
)

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import settings
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)
    
urlpatterns = patterns('',
    (r'^admin/jsi18n', i18n_javascript),
    url(r'^about/$', 'mental.views.about'),
    (r'^login/$', login, {'template_name':'login.html'} ),
    (r'^logout/$', logout,{'template_name':'logout.html'}),
    # Examples:
    # url(r'^$', 'kfjz.views.home', name='home'),
    # url(r'^kfjz/', include('kfjz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
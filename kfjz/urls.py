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
    (r'^login/$', login, {'template_name':'login.html'} ),
    (r'^logout/$', logout,{'template_name':'logout.html'}),

    url(r'^about/$', 'mental.views.about'),
    url(r'^loginjz/$', 'mental.views.loginjz'),
    
    url(r'^mentalinput/$', 'mental.views.mentalinput'),
    url(r'^mentalselect/$', 'mental.views.mentalselect'),
    url(r'^mentalmodify/(\d+)/$', 'mental.views.mentalmodify'),

    url(r'^approvalinput/(.*|\d+)/$', 'mental.views.approvalinput'),
    url(r'^approvallist/$', 'mental.views.approvallist'),
    url(r'^approvalmodify/(\d+)/$', 'mental.views.approvalmodify'),

    url(r'^applyinput/(.*|\d+)/$', 'mental.views.applyinput'),
    url(r'^applylist/$', 'mental.views.applylist'),
    url(r'^applymodify/(\d+)/$', 'mental.views.applymodify'),

    # Examples:
    # url(r'^$', 'kfjz.views.home', name='home'),
    # url(r'^kfjz/', include('kfjz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT )
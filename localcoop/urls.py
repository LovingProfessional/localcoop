from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'localcoop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('subscriptions.views',
    url(r'^register/','register_coopuser_view'),
    url(r'^sorry/','sorry_past_deadline_view'),
    url(r'^process-registration/','process_registration'),
    url(r'^thanks-for-registering/','thanks_for_registering'),
    url(r'^login/','login'),
    url(r'^login-successful', 'login_successful'),
    url(r'^user/(?P<username_string>\w+)/$','user_page'),
)

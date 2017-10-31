from django.conf.urls import url

from views import login_view, signup_view, main_page_view, post_view

urlpatterns = [
    url(r'^blog/login/$', login_view, name='login'),
    url(r'^blog/signup/$', signup_view, name='signup'),
    url(r'^blog/$', main_page_view, name='mainpage'),
    url(r'^blog/post/(?P<pk>\d+)$', post_view, name='post_detail'),

]

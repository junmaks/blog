from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<username>/blog', get_users, name='author_name'),
    path('<username>/new_post/', add_post, name='new_post'),
    path('<username>/my_blog/', get_my_blog, name='my_blog'),
    path('<username>/my_subscriptions/', get_subscriptions, name='my_subscriptions'),
    path('posts/<int:post_id>/', view_post, name='view_post'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
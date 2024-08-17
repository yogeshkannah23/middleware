from django.urls import path
from login import views

urlpatterns = [
    path('',views.index,name='login-api'),


    path('register/',views.Register.as_view(),name='login-register'),
    path('login/',views.LoginView.as_view(),name='login-loginview'),
    path('user_view/',views.UserView.as_view(),name='login-user_view'),
    
    path('add_post/',views.AddPost.as_view(),name='login-add_post'),
    path('post_list/',views.GetAllPost.as_view(),name='login-post_list'),
    path('get_by_user/',views.GetByUser.as_view(),name='login-get_by_user')
]
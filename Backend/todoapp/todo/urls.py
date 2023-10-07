from django.urls import path
from . import views
from .views import SignupView, LoginView,CreateTodoView,GetTodoView
urlpatterns=[
    path("", views.my_views , name="my_view"),
    path("signup/" , SignupView.as_view() , name="signup" ),
    path('login/' , LoginView.as_view() , name="login" ),
    path('create-todo/' , CreateTodoView.as_view() , name="create-todo"),
    path('<str:user_id>/todo/' , GetTodoView.as_view() , name = "get-todo-view")
]
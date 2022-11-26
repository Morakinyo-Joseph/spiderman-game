from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name="home"),

    path('login', views.signin, name="login"),

    path('logout', views.log_out, name="logout"),

    path('post', views.posting, name="post"),

    path('list', views.list, name="list"),

    path('delete/<int:pk>', views.deletion, name="delete")

]

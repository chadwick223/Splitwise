from django.urls import path
from .import views


urlpatterns = [
    path("",views.home,name="home"),
    path("groups/create/",views.create_group,name="create_group"),
    path("groups/<int:group_id>/", views.group_detail, name="group_detail"),
    path("groups/<int:group_id>/expenses/add/", views.add_expense, name="add_expense"),
    path("groups/<int:group_id>/settle/", views.settle_expense, name="settle_expense"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),


    
]

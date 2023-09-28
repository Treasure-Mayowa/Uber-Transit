from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("driver/register", views.driver_register, name="driver-register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("driver/dashboard", views.driver_dashboard, name="driver-dashboard"),
    path("accessibility-guide", views.accessibility, name="accessibility-guide"),
]
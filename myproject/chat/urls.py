from django.urls import path

from . import views
app_name="chat"

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup_view, name='signup'),
    path("login/", views.login_view, name='login'),
    path("home/", views.home, name='home'),
    path("logout/", views.logout_view, name='logout'),
    path("display/",views.display, name="display"),
    path("watchlist", views.watchlist, name="watchlist"),
    #
    path("get-movie/<str:movie_name>/", views.apirequest, name="api")


]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from core import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('logout/', LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path('', LoginView.as_view(template_name="core/login.html",
                               redirect_authenticated_user=True), name="login"),
]

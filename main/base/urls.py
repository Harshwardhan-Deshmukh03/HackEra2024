from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.userhome, name="userhome"),
    path('adminhome/',views.adminhome,name="adminhome"),

    path('login/',views.loginUser,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/', views.logoutUser, name="logout"),






    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="base/password_reset.html"), name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="base/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="base/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="base/password_reset_done.html"),
         name="password_reset_complete"),
]

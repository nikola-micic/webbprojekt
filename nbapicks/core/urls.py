from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('', views.index, name="index"),
    path('teams/', views.teams, name="teams"),
    path('teams/sort=az', views.teamsaz, name="teamsaz"),
    path('teams/sort=za', views.teamsza, name='teamsza'),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('predictions/', views.predictions, name="predictions"),
    path('leaderboards/', views.leaderboards, name="leaderboards"),
    path('leaderboards/<str:table>/', views.leaderboards_detail, name="leaderboards_detail"),
    path('contact/', views.contact, name="contact"),
    path('pick-history/', views.pick_history, name="pickhistory"),
    #path('predictions/<game_id>/', views.predict_game, name="predict_game"),
]
from django.urls import path
from chat.views import UserView, UserDetailView
app_name = 'chat'
urlpatterns = [
    path('api/users/', UserView.as_view()),
    path('api/users/<int:id>/', UserDetailView.as_view()),
]
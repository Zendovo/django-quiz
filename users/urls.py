from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('redirect/', LoginRedirectView.as_view(), name='home-redirect'),
    path('attempts/', PrevAttemptsView.as_view(), name='prev-attempts'),
    path('attempts/<int:id>/', PrevAttemptDetailView.as_view(), name='prev-attempts'),
]
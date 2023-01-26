from django.urls import path
from .views import *

urlpatterns = [
    path('', QuizListView.as_view(), name="quiz-list-view"),
    path('<int:id>/', QuizAttemptView.as_view(), name="quiz-attempt-view"),
    path('intm/<int:id>/', QuizPasswordView.as_view(), name="quiz-password-view"),
]
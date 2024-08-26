from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LevelViewSet, QuizViewSet, QuestionViewSet, ChoiceViewSet, SubmissionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'levels', LevelViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

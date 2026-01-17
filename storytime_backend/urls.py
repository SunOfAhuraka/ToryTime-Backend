
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from storytime.views import QuizResultViewSet, StoryViewSet, ChildViewSet, RecordingViewSet, RegisterView

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'children', ChildViewSet, basename='child')
router.register(r'recordings', RecordingViewSet, basename='recording')
router.register(r'quiz-results', QuizResultViewSet, basename='quizresult')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
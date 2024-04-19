from django.urls import path
from .auth.views import ObtainAuthTokenAPIView, DeleteAuthTokenAPIView, RegisterUserAPIView
from .views import VideoListCreateAPIView, VideoRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view()),
    path('login/', ObtainAuthTokenAPIView.as_view()),
    path('logout/', DeleteAuthTokenAPIView.as_view()),
    path('videos/', VideoListCreateAPIView.as_view()),
    path('videos/<int:pk>/', VideoRetrieveUpdateDestroyAPIView.as_view()),
    # path('videos/<int:pk>/stream/', VideoStreamAPIView.as_view(), name='video-stream'),
]
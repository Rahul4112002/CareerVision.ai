from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('prediction/', views.prediction, name='prediction'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('roadmap/', views.roadmap, name='roadmap'),
    path('job/', views.job_view, name='job'),  # New URL pattern for job page
]

# This is to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
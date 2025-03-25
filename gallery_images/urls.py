from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('gallery/preview/<int:index>/', views.preview_image, name='preview_image'),
    path('gallery/<int:index>/', views.gallery_image, name='gallery_image'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

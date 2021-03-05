from django.urls import path
from django.conf.urls.static import static

from . import views
from . import settings

urlpatterns = [
    path('', views.index, name = 'index'),
    path('submit', views.submit, name = 'submit'),
    path('<round_name>', views.thanks, name = 'thanks'),
] + static('/static-clips',
           document_root = settings.MUSICSURVEY_CLIP_ROOT)

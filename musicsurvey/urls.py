from django.urls import path

from . import views
from . import settings

urlpatterns = [
    path('', views.index, name = 'index'),
    path('submit', views.submit, name = 'submit'),
    path('<round_name>', views.thanks, name = 'thanks')
]

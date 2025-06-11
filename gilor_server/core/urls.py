from django.urls import path
from .views import api_home, snake, save_score, madlibs

urlpatterns = [
    path('', api_home),
    path('snake', snake, name='snake'),
    path('save_score', save_score, name='save_score_api'),
    path('madlibs', madlibs, name='madlibs'),

]
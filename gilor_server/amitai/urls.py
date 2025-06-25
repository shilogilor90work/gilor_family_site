from django.urls import path, include
from .views import api_home, snake, save_score, adding_data, create_data


urlpatterns = [
    path('', api_home),
    path('snake', snake, name='snake'),
    path('save_score', save_score, name='save_score_api'),
    path('madlibs/', include('amitai.madlibs_urls')), 
    path('adding_data', adding_data, name='adding_data'),
    path('create_data', create_data, name='create_data'),

]
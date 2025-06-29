from django.urls import path
from .views import api_home, snake, save_score, adding_data, create_data, read_data, delete_all_templates, madlibs_game, read_finished_data, create_finished_data, get_random_template#, delete_data, update_data


urlpatterns = [
    path('', api_home),
    path('snake', snake, name='snake'),
    path('save_score', save_score, name='save_score_api'),
    path('madlibs_game', madlibs_game, name='madlibs_game'),
    # path('madlibs/', include('amitai.madlibs_urls')), 
    path('adding_data', adding_data, name='adding_data'),
    path('create_data', create_data, name='create_data'),
    path('read_data', read_data, name='read_data'),
    path('delete_all_templates', delete_all_templates, name='delete_all_templates'),
    path('read_finished_data', read_finished_data, name='read_finished_data'),
    path('create_finished_data', create_finished_data, name='create_finished_data'),
    path('get_random_template', get_random_template, name='get_random_template'),
    # path('delete_data', delete_data, name='delete_data'),
    # path('update_data', update_data, name='update_data'),
]
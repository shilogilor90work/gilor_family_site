from django.urls import path
from .views import api_home, snake, save_score, two_player, adding_data, create_data, get_all_templates, delete_all_templates, like_template, dislike_template, madlibs_game, get_finished_template_by_id, get_finished_data, create_finished_data, get_random_template, delete_data, update_data


urlpatterns = [
    path('', api_home),
    path('snake', snake, name='snake'),
    path('save_score', save_score, name='save_score_api'),
    path('madlibs_game', madlibs_game, name='madlibs_game'),
    # path('madlibs/', include('amitai.madlibs_urls')), 
    path('adding_data', adding_data, name='adding_data'),
    path('create_data', create_data, name='create_data'),
    path('get_all_templates', get_all_templates, name='get_all_templates'),
    path('delete_all_templates', delete_all_templates, name='delete_all_templates'),
    path('get_finished_data', get_finished_data, name='get_finished_data'),
    path('create_finished_data', create_finished_data, name='create_finished_data'),
    path('get_random_template', get_random_template, name='get_random_template'),
    path('get_finished_template_by_id/<int:id>', get_finished_template_by_id, name='get_finished_template_by_id'),
    path('delete_data/<int:id>', delete_data, name='delete_data'),
    path('update_data/<int:id>', update_data, name='update_data'),
    path('like_template/<int:id>', like_template, name='like_template'),
    path('dislike_template/<int:id>', dislike_template, name='dislike_template'),
    path('two_player', two_player, name='two_player'),
]
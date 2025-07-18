from django.http import JsonResponse
from django.shortcuts import render
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta
import re
from .serializers import MadlibsSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import madlibs
from .models import GameRecord
import random
from .models import madlibs_user_history
def api_home(request):
    return JsonResponse({"message": "Welcome to the API"})

def snake(request):
    """
    Renders the HTML page containing the Snake game and passes top scores.
    """
    # Fetch the top 10 game records by score, highest first
    # IMPORTANT: Added 'game_duration' to the .values() call
    top_scores = GameRecord.objects.order_by('-score', '-time_created').values('name', 'score', 'game_duration')[:10]

    top_scores_list = []
    for record in top_scores:
        # DurationField returns a timedelta object.
        # Format it for display. You can choose your desired format.
        # For simplicity, let's format it as HH:MM:SS if hours exist, else MM:SS
        total_seconds = int(record['game_duration'].total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            formatted_duration = f"{minutes:02}:{seconds:02}"

        top_scores_list.append({
            'name': record['name'],
            'score': record['score'],
            'game_duration_formatted': formatted_duration # Add the formatted duration
        })

    context = {
        'top_scores': top_scores_list
    }
    print("shilo")
    print(context)
    return render(request, 'snake_game/snake.html', context)


@csrf_exempt # WARNING: Use proper CSRF protection in production!
def GameScore(request): # Renamed function for clarity
    """
    API endpoint to receive and save the complete game record.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data with default values or validation
            name = data.get('name', 'Anonymous') # Default to 'Anonymous' if not provided
            score = data.get('score')
            game_duration_ms = data.get('game_duration_ms') # Expecting milliseconds
            food_eaten = data.get('food_eaten')

            # Basic validation
            if not all([score is not None, game_duration_ms is not None, food_eaten is not None]):
                return JsonResponse({'status': 'error', 'message': 'Missing required game data (score, duration, food_eaten)'}, status=400)

            if not isinstance(score, int) or not isinstance(food_eaten, int):
                return JsonResponse({'status': 'error', 'message': 'Score and food eaten must be integers'}, status=400)

            if not isinstance(game_duration_ms, (int, float)):
                return JsonResponse({'status': 'error', 'message': 'Game duration must be a number in milliseconds'}, status=400)

            # Convert milliseconds to timedelta for Django's DurationField
            from datetime import timedelta
            game_duration = timedelta(milliseconds=game_duration_ms)

            # Create and save the GameRecord
            GameRecord.objects.create(
                name=name,
                score=score,
                game_duration=game_duration,
                food_eaten=food_eaten
            )

            return JsonResponse({'status': 'success', 'message': 'Game record saved successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the error for debugging in a real application
            print(f"Error saving game record: {e}")
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {e}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt # WARNING: Use proper CSRF protection in production!
def save_score(request):
    """
    API endpoint to receive and save the game score.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data with default values or handle missing keys
            name = data.get('name')
            score_value = data.get('score')
            game_duration_ms = data.get('game_duration_ms')
            food_eaten = data.get('food_eaten')

            # Basic validation for required fields
            if not all([name, score_value is not None, game_duration_ms is not None, food_eaten is not None]):
                return JsonResponse({'status': 'error', 'message': 'Missing one or more required fields (name, score, game_duration_ms, food_eaten)'}, status=400)

            # Validate data types
            if not isinstance(name, str):
                return JsonResponse({'status': 'error', 'message': 'Name must be a string'}, status=400)
            if not isinstance(score_value, int):
                return JsonResponse({'status': 'error', 'message': 'Score must be an integer'}, status=400)
            if not isinstance(game_duration_ms, (int, float)): # Allow float for milliseconds
                return JsonResponse({'status': 'error', 'message': 'Game duration (ms) must be a number'}, status=400)
            if not isinstance(food_eaten, int):
                return JsonResponse({'status': 'error', 'message': 'Food eaten must be an integer'}, status=400)

            # Convert game_duration_ms to timedelta for DurationField
            game_duration = timedelta(milliseconds=game_duration_ms)

            # Save the record to the database
            GameRecord.objects.create(
                name=name,
                score=score_value,
                game_duration=game_duration,
                food_eaten=food_eaten
            )
            return JsonResponse({'status': 'success', 'message': 'Game record saved successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception for debugging in production environments
            # import logging
            # logging.exception("Error saving game record")
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)




def madlibs_game(request):
    return render(request, 'madlibs_game/madlibs_game.html')

def adding_data(request):
    return render(request, 'adding_data/adding_data.html')


@csrf_exempt # WARNING: Use proper CSRF protection in production!
def create_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body).get("data")
            name = data.get('name', 'Anonymous')  # Default to 'Anonymous' if not provided
            templateText = data.get('templateText')
            if not isinstance(name, str):
                return JsonResponse({'status': 'error', 'message': 'Name must be a string'}, status=400)
                placeholders = ["noun", "adjective", "verb", "funny_word", "funny_name"]

            # Find all items inside square brackets
            found = re.findall(r"\[(.*?)\]", templateText)

            # Count each placeholder and assign to local variables
            noun = found.count("noun")
            adjective = found.count("adjective")
            verb = found.count("verb")
            funny_word = found.count("funny_word")
            funny_name = found.count("funny_name")
            # Save the record to the database
            print("saving")
            madlibs.objects.create(
                paragraph=templateText,
                noun=noun,
                adjective=adjective,
                verb = verb,
                funny_word = funny_word,
                funny_name = funny_name,
                likes = 0,
                dislikes = 0,
            )
            print("saved")
            return JsonResponse({'status': 'success', 'message': 'Data received successfully', 'name': name})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception for debugging in production environments
            # import logging
            # logging.exception("Error saving game record")
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)
        
def get_all_templates(request):
    """
    API endpoint to read all madlibs data.
    """
    if request.method == 'GET':
        try:
            # Fetch all madlibs records
            madlibs_data = madlibs.objects.all().values('id', 'paragraph', 'noun', 'adjective', 'verb', 'funny_word', 'funny_name', 'likes', 'dislikes')
            return JsonResponse(list(madlibs_data), safe=False)  # Return as a list of dictionaries
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'}, status=405)
    
def delete_data(request, id):
    """
    API endpoint to delete a specific madlib by ID.
    """
    if request.method == 'DELETE':
        try:
            # Fetch the madlib record by ID
            try:
                madlib = madlibs.objects.get(id=id)
            except madlibs.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Madlib not found'}, status=404)

            # Delete the record
            madlib.delete()
            return JsonResponse({'status': 'success', 'message': 'Madlib deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only DELETE requests are allowed'}, status=405)

def update_data(request, id):
    """
    API endpoint to update a specific madlib by ID.
    """
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # Fetch the madlib record by ID
            try:
                madlib = madlibs.objects.get(id=id)
            except madlibs.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Madlib not found'}, status=404)

            # Update fields if provided in the request
            if 'paragraph' in data:
                madlib.paragraph = data['paragraph']
            if 'noun' in data:
                madlib.noun = data['noun']
            if 'adjective' in data:
                madlib.adjective = data['adjective']
            if 'verb' in data:
                madlib.verb = data['verb']
            if 'funny_word' in data:
                madlib.funny_word = data['funny_word']
            if 'funny_name' in data:
                madlib.funny_name = data['funny_name']
            if 'likes' in data:
                madlib.likes = data['likes']
            if 'dislikes' in data:
                madlib.dislikes = data['dislikes']

            # Save the updated record
            madlib.save()
            return JsonResponse({'status': 'success', 'message': 'Madlib updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only PUT requests are allowed'}, status=405)


@csrf_exempt # WARNING: Use proper CSRF protection in production!
def create_finished_data(request):
    """
    API endpoint to create a finished madlib with user input.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body).get("data")
            print(data)
            paragraph_id = data.get('paragraph_id')
            user_name = data.get('user_name')
            noun = data.get('noun', [])
            adjective = data.get('adjective', [])
            verb = data.get('verb', [])
            funny_word = data.get('funny_word', [])
            funny_name = data.get('funny_name', [])


            # Validate required fields
            if not paragraph_id or not user_name:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields: paragraph_id and user_name'}, status=400)

            # Create the madlibs_user_history record
            from .models import madlibs_user_history
            madlibs_user_history.objects.create(
                paragraph_id=paragraph_id,
                user_name=user_name,
                noun=noun,
                adjective=adjective,
                verb=verb,
                funny_word=funny_word,
                funny_name=funny_name,
                likes=0,
                dislikes=0,
            )
            return JsonResponse({'status': 'success', 'message': 'Finished madlib created successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

def get_finished_data(request):
    """
    API endpoint to read all finished madlibs data.
    """
    if request.method == 'GET':
        try:
            # Fetch all finished madlibs records
            from .models import madlibs_user_history
            finished_data = madlibs_user_history.objects.all().values(
                'id', 'paragraph_id', 'user_name', 'noun', 'adjective', 'verb', 
                'funny_word', 'funny_name', 'likes', 'dislikes'
            )
            return JsonResponse(list(finished_data), safe=False)  # Return as a list of dictionaries
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'}, status=405)

@csrf_exempt # WARNING: Use proper CSRF protection in production!
def delete_all_templates(request):
    """
    API endpoint to delete all madlibs data.
    """
    if request.method == 'DELETE':
        try:
            # Delete all madlibs records
            madlibs.objects.all().delete()
            return JsonResponse({'status': 'success', 'message': 'All madlibs deleted successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only DELETE requests are allowed'}, status=405)

class MadlibsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Madlibs to be viewed or edited.
    """
    queryset = madlibs.objects.all().order_by('-id') # Order by ID descending, adjust as needed
    serializer_class = MadlibsSerializer
    authentication_classes = [] # Set to an empty list to disable authentication
    permission_classes = [AllowAny] # Allow any user to access this view

def get_random_template(request):
    """
    API endpoint to get a random madlib template.
    """
    if request.method == 'GET':
        try:
            # Fetch all madlibs records
            templates = list(madlibs.objects.all())
            if not templates:
                return JsonResponse({'status': 'error', 'message': 'No templates available'}, status=404)

            # Select a random template
            random_template = random.choice(templates)
            serializer = MadlibsSerializer(random_template)
            return JsonResponse(serializer.data, safe=False)  # Return the serialized data
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'}, status=405)

def get_finished_template_by_id(request, id):
    """
    API endpoint to get a finished madlib template by ID.
    """
    if request.method == 'GET':
        try:
            # Fetch the finished madlib record by ID
            try:
                finished_template = madlibs_user_history.objects.get(id=id)
            except madlibs_user_history.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Finished template not found'}, status=404)

            serializer = MadlibsSerializer(finished_template)
            return JsonResponse(serializer.data, safe=False)  # Return the serialized data
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only GET requests are allowed'}, status=405)
@csrf_exempt
def like_template(request, id):
    """
    API endpoint to like a finished madlib template by ID.
    """
    print("like_template called with ID:", id)
    if request.method == 'POST':
        try:
            # Fetch the finished madlib record by ID
            try:
                print("before template found:", id)
                finished_template = madlibs.objects.get(id=id)
                print("after template found:", id)
            except madlibs.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Finished template not found'}, status=404)

            # Increment likes
            finished_template.likes += 1
            finished_template.save()

            return JsonResponse({'status': 'success', 'message': 'Template liked successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def dislike_template(request, id):
    """
    API endpoint to dislike a finished madlib template by ID.
    """
    if request.method == 'POST':
        try:
            # Fetch the finished madlib record by ID
            try:
                finished_template = madlibs.objects.get(id=id)
            except madlibs.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Finished template not found'}, status=404)

            # Increment dislikes
            finished_template.dislikes += 1
            finished_template.save()

            return JsonResponse({'status': 'success', 'message': 'Template disliked successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

def two_player(request):
    """
    Renders the HTML page for the two-player game.
    """
    return render(request, 'two_player/two_player.html')
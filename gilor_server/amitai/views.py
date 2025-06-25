from django.http import JsonResponse
from django.shortcuts import render
from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta
from .serializers import MadlibsSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import madlibs
from .models import GameRecord

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




def madlibs_url(request):
    return render(request, 'madlibs/madlibs.html')

def adding_data(request):
    return render(request, 'adding_data/adding_data.html')

def create_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paragraph = data.get('paragraph')
            if not isinstance(paragraph, str):
                return JsonResponse({'status': 'error', 'message': 'Name must be a string'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception for debugging in production environments
            # import logging
            # logging.exception("Error saving game record")
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)
        




class MadlibsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Madlibs to be viewed or edited.
    """
    queryset = madlibs.objects.all().order_by('-id') # Order by ID descending, adjust as needed
    serializer_class = MadlibsSerializer
    authentication_classes = [] # Set to an empty list to disable authentication
    permission_classes = [AllowAny] # Allow any user to access this view

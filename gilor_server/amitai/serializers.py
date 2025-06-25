# your_app_name/serializers.py
from rest_framework import serializers
from .models import madlibs # Adjust 'your_app_name' to your actual app name

class MadlibsSerializer(serializers.ModelSerializer):
    class Meta:
        model = madlibs
        fields = '__all__' # Include all fields from your model
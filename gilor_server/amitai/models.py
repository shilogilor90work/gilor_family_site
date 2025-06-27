from django.db import models
from django.db.models import JSONField


# Create your models here.
class GameRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    score = models.IntegerField()
    game_duration = models.DurationField()
    food_eaten = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.score}"

class madlibs(models.Model):
    id = models.AutoField(primary_key=True)
    paragraph = models.TextField()
    noun = models.IntegerField(default=0)
    adjective = models.IntegerField(default=0)
    verb = models.IntegerField(default=0)
    funny_word = models.IntegerField(default=0)
    funny_name = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    def __str__(self):
        return self.id

class madlibs_user_history(models.Model):
    id = models.AutoField(primary_key=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    paragraph_id = models.IntegerField()
    user_name = models.CharField(max_length=255) 
    noun = JSONField(
        models.CharField(max_length=200),
        default=list, # important for default empty list
    )
    adjective = JSONField(
        models.CharField(max_length=200),
        default=list, # important for default empty list
    )
    verb = JSONField(
        models.CharField(max_length=200),
        default=list, # important for default empty list
    )
    funny_word = JSONField(
        models.CharField(max_length=200),
        default=list, # important for default empty list
    )
    funny_name  = JSONField(
        models.CharField(max_length=200),
        
        default=list, # important for default empty list
    )
    def __str__(self):
        return self.user_id

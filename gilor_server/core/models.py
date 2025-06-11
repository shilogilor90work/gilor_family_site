from django.db import models

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
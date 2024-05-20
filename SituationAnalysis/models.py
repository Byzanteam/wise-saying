from django.db import models


class Suggestion(models.Model):
    month = models.CharField(max_length=100)
    suggestion = models.TextField()

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Food(models.Model):
    name_food = models.CharField(max_length=200, blank=True)
    quantity_food = models.TextField(max_length=30, null=True)
    dangers_food = models.TextField(max_length=400, null=True)
    store_food = models.TextField(max_length=200, null=True)
    nutri_score_food = models.CharField(max_length=30, null=True)
    link_food = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.name_food

class Categories(models.Model):
    name_categories = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.name_categories

class foodcate(models.Model):
    Food_id = models.ForeignKey(Food, on_delete=models.CASCADE, default="1")
    Categories_id = models.ForeignKey(Categories, on_delete=models.CASCADE, default="1")

    def __str__(self):
        return self.Food_id

class saved(models.Model):
    Food_id_foodsub = models.ManyToManyField(Food, related_name='foodsub')
    Food_id_foodissub = models.ManyToManyField(Food, related_name='foodissub')

    def __str__(self):
        return self.Food_id_foodsub
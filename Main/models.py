from django.db import models
from django.contrib.auth.models import User

#python manage.py makemigrations Main
#python manage.py migrate Main
#python manage.py createsuperuser

class PeopleGroup(models.Model):
    name = models.CharField(primary_key=True, max_length=100, default="",)
    date_begin = models.DateField()
    date_end = models.DateField()
    protocol = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    group = models.ForeignKey("PeopleGroup", on_delete=models.SET_NULL, null=True)
    recipes = models.ManyToManyField("Recipe",blank=True, editable=False)
    food = models.ManyToManyField("FoodPortion",blank=True, editable=False)
    def __str__(self):
        return self.user.username

class FoodPortion(models.Model):
    name = models.CharField(max_length=100, default="")
    quantity = models.FloatField(blank=True, null=True,)
    measurement = models.ForeignKey("Measurement", on_delete=models.SET_NULL, null=True, blank=True, default=1)
    food_group = models.ForeignKey("FoodGroup", on_delete=models.SET_NULL, null=True, default=1)

class FoodGroup(models.Model):
    number = models.IntegerField(primary_key=True, default=1)
    description = models.CharField(max_length=100, default="")
    def __str__(self):
        return str(self.number)

class Measurement(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    short_name = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.name


class ProtocolMeal(models.Model):
    protocol = models.IntegerField()
    meal = models.ForeignKey("Meal", on_delete=models.CASCADE)
    description = models.TextField(default="", blank=True,)
    suggestions = models.TextField(default="", blank=True,)
    meal_options = models.ManyToManyField("MealOption")
    recipes = models.ManyToManyField("Recipe")

class MealOption(models.Model):
    meal_units = models.ManyToManyField("MealUnit")

class MealUnit(models.Model):
    quantity = models.IntegerField()
    food_group = models.ForeignKey("FoodGroup", on_delete=models.CASCADE)
    def __str__(self):
        return str(self.quantity) + " group " + str(self.food_group)

class Meal(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100, default="")
    ingredients = models.TextField(default="", blank=True,)
    description = models.TextField(default="", blank=True,)

# TASKS

class AllTasks(models.Model):
    name = models.CharField(max_length=20, default="")
    position = models.IntegerField(default=1)
    font_awesome_icon = models.CharField(max_length=100, default="")
    background_color = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.name

class TextTask(AllTasks):
    task_type = 'text'
    title = models.CharField(max_length=500, default="")
    text = models.TextField(default="", blank=True,)

class ChallengeTask(AllTasks):
    task_type = 'challenge'
    title = models.CharField(max_length=500, default="")
    text = models.TextField(default="", blank=True,)
    image = models.ImageField(upload_to='static/DB_images')

class MultipleChoiceSurveyTask(AllTasks):
    task_type = 'multiple_choice_survey'
    question = models.CharField(max_length=1000)
    choices = models.TextField(max_length=5000)
    multiple_choices_allowed = models.BooleanField()
    def __str__(self):
        return self.question

class SurveyVote(models.Model):
    question = models.CharField(max_length=5000)
    people_group = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    choice = models.CharField(max_length=5000)
    def __str__(self):
        return self.choice

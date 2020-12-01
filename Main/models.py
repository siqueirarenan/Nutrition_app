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
    last_task_line = models.IntegerField(default=True)
    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    group = models.ForeignKey("PeopleGroup", on_delete=models.SET_NULL, null=True)
    recipes = models.ManyToManyField("Recipe", blank=True, editable=False)
    food = models.ManyToManyField("FoodPortion", blank=True, editable=False)
    completed_tasks = models.ManyToManyField("AllTasks", blank=True, default=None)
    def __str__(self):
        return self.user.username

class FoodPortion(models.Model):
    name = models.CharField(max_length=100, default="")
    quantity = models.FloatField(blank=True, null=True,)
    measurement = models.ForeignKey("Measurement", on_delete=models.SET_NULL, null=True, blank=True, default=1)
    def __str__(self):
        return str(self.name) + " " + str(self.quantity) + str(self.measurement)

class FoodGroup(models.Model):
    number = models.IntegerField(primary_key=True, default=1)
    description = models.CharField(max_length=100, default="")
    food_portions = models.ManyToManyField('FoodPortion')
    def __str__(self):
        return "Food group " + str(self.number) + " - " + str(self.description)

class Measurement(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    short_name = models.CharField(max_length=20, default="")
    def __str__(self):
        return self.short_name


class ProtocolMeal(models.Model):
    protocol = models.IntegerField()
    MEAL_CHOICES = [
        ('Café-da-manhã', 'Café-da-manhã'),
        ('Lanche da manhã', 'Lanche da manhã'),
        ('Almoço', 'Almoço'),
        ('Lanche da tarde', 'Lanche da tarde'),
        ('Café da tarde', 'Café da tarde'),
        ('Jantar', 'Jantar'),
        ('Ceia', 'Ceia'),
    ]
    meal = models.CharField(max_length=20, choices=MEAL_CHOICES, default = 'Almoço')
    meal_order = models.IntegerField(editable=False, default=1)
    description = models.TextField(default="", blank=True, help_text="Every time you write 'group x' (group 1, group 2..), it will become a link")
    suggestions = models.TextField(default="", blank=True,)
    recipes = models.ManyToManyField("Recipe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meal_order = self.MEAL_CHOICES.index((str(self.meal), str(self.meal)))
    def __str__(self):
        return "Protocol " + str(self.protocol) + " - " + str(self.meal)

# class MealOption(models.Model):
#     meal_units = models.ManyToManyField("MealUnit")
#
# class MealUnit(models.Model):
#     quantity = models.IntegerField()
#     food_group = models.ForeignKey("FoodGroup", on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.quantity) + " group " + str(self.food_group)

class Recipe(models.Model):
    name = models.CharField(max_length=100, default="")
    ingredients = models.TextField(default="", blank=True,)
    description = models.TextField(default="", blank=True,)
    def __str__(self):
        return self.name

# TASKS

class AllTasks(models.Model):
    name = models.CharField(max_length=20, default="")
    line_position = models.IntegerField(default=1, blank=True, null=True)
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
    choices = models.TextField(max_length=5000, help_text="write the choices in different lines")
    multiple_choices_allowed = models.BooleanField()
    def __str__(self):
        return self.question
    def delete(self): #Avoid deletion
        pass

class WritingSurveyTask(AllTasks):
    task_type = 'writing_survey'
    question = models.CharField(max_length=5000)
    def __str__(self):
        return self.question

class SurveyVote(models.Model):
    question = models.CharField(max_length=5000)
    people_group = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    choice = models.CharField(max_length=5000)
    def __str__(self):
        return self.choice

class CalculationTask(AllTasks):
    task_type = 'calculation'
    title = models.CharField(max_length=500, default="")
    fields = models.TextField(max_length=1000, help_text="write the fields in different lines")
    equations = models.TextField(max_length=1000, help_text="write the equations in different lines")
    result_sentence = models.TextField(max_length=1000, help_text="write the sentence by using eq1, eq2, eq3... for the results of the equations.")
    def __str__(self):
        return self.title

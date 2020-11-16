from django.db import models

#python manage.py makemigrations Main
#python manage.py migrate Main

class FoodGroup(models.Model):

    name = models.TextField()


class Receipt(models.Model):

    name = models.TextField()
    description = models.TextField()
    food_group = models.ForeignKey("FoodGroup", on_delete=models.SET_NULL, null=True)
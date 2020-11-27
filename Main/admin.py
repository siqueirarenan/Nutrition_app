from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import *

class PeopleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_begin','protocol','is_active','last_task_line')
class FoodGroupAdmin(admin.ModelAdmin):
    list_display = ('number','description')
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')
class FoodPortionAdmin(admin.ModelAdmin):
    list_display = ('name','quantity','measurement','food_group')
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name',)
class MealUnitAdmin(admin.ModelAdmin):
    list_display = ('quantity','food_group')
class ProtocolMealAdmin(admin.ModelAdmin):
    list_display = ('protocol','meal','description')
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user','group')
class TextTaskAdmin(admin.ModelAdmin):
    list_display = ('id','title')
class ChallengeTaskAdmin(admin.ModelAdmin):
    list_display = ('id','title')
class MultipleChoiceSurveyTaskAdmin(admin.ModelAdmin):
    list_display = ('question',)
class WritingSurveyTaskAdmin(admin.ModelAdmin):
    list_display = ('question',)
class CalculationTaskAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(PeopleGroup, PeopleGroupAdmin)
admin.site.register(FoodGroup, FoodGroupAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(FoodPortion, FoodPortionAdmin)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealUnit, MealUnitAdmin)
admin.site.register(MealOption)
admin.site.register(ProtocolMeal, ProtocolMealAdmin)

admin.site.register(TextTask, TextTaskAdmin)
admin.site.register(ChallengeTask, ChallengeTaskAdmin)
admin.site.register(MultipleChoiceSurveyTask, MultipleChoiceSurveyTaskAdmin)
admin.site.register(WritingSurveyTask, WritingSurveyTaskAdmin)
admin.site.register(CalculationTask, CalculationTaskAdmin)


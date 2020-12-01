from django.contrib import admin
from django.contrib.admin import AdminSite, sites
from .models import *
from django.contrib.sites.models import Sit

class MyAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Usuários": 0,
            "User groups": 1,
            "People groups": 2,
            "Text tasks": 3,
            "Challenge tasks": 4,
            "Writing survey tasks": 5,
            "Multiple choice survey tasks": 6,
            "Calculation tasks": 7,
            "Recipes": 8,
            "Protocol meals": 9,
            "Food groups": 10,
            "Food portions": 11,
            "Measurements": 12
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])
        return app_list
admin_site = MyAdminSite(name='myadmin')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','first_name','last_name','is_active','last_login')
class PeopleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_begin','protocol','is_active','last_task_line')
class FoodGroupAdmin(admin.ModelAdmin):
    list_display = ('number','description')
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')
class FoodPortionAdmin(admin.ModelAdmin):
    list_display = ('name','quantity','measurement')
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
class MySitesAdmin(sites.SiteAdmin):
     list_display = ('id','provider')
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

admin.site.register(Site, MySitesAdmin)

admin_site.register(User, UserAdmin)
admin_site.register(UserGroup, UserGroupAdmin)
admin_site.register(PeopleGroup, PeopleGroupAdmin)
admin_site.register(FoodGroup, FoodGroupAdmin)
admin_site.register(Measurement, MeasurementAdmin)
admin_site.register(FoodPortion, FoodPortionAdmin)

admin_site.register(Recipe, RecipeAdmin)
# admin.site.register(MealUnit, MealUnitAdmin)
# admin.site.register(MealOption)
admin_site.register(ProtocolMeal, ProtocolMealAdmin)

admin_site.register(TextTask, TextTaskAdmin)
admin_site.register(ChallengeTask, ChallengeTaskAdmin)
admin_site.register(MultipleChoiceSurveyTask, MultipleChoiceSurveyTaskAdmin)
admin_site.register(WritingSurveyTask, WritingSurveyTaskAdmin)
admin_site.register(CalculationTask, CalculationTaskAdmin)


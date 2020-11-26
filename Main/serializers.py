from rest_framework import routers, serializers, viewsets
from Main.models import *

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name','last_name']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description']


class SurveyVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SurveyVote
        fields = ['question', 'people_group', 'user', 'choice']


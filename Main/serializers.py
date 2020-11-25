from rest_framework import routers, serializers, viewsets
from Main.models import Recipe

# Serializers define the API representation.
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description']

# ViewSets define the view behavior.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
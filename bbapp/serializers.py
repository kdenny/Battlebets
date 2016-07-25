from django.forms import widgets
from rest_framework import serializers
from bbapp.models import UserProfile


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos')
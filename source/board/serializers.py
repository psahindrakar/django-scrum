from datetime import date

from django.utils.translation import ugettext_lazy as _  
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Sprint, Task


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active')


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, read_only=True, required=False)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'order', 'assigned', 'started', 'due', 'completed',)


class SprintSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'tasks')

    def validate_end(self, value):                
        if(value < date.today()): 
            msg = _('End date cannot be in the past.') 
            raise serializers.ValidationError(msg) 
        return attrs
from datetime import date

from django.utils.translation import ugettext_lazy as _  
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Sprint, Task


User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    See: http://tomchristie.github.io/rest-framework-2-docs/api-guide/serializers
    """
    def __init__(self, *args, **kwargs):
        # Do not pass the custom fields received in kwargs to super class
        context = kwargs.pop('context', None)
        # context = self.context
        fields = context.pop('fields', None) if context else None

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(self.fields)
            required = set(fields)
            to_remove = allowed - required
            if to_remove != allowed:  
                for field_name in to_remove:
                    self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active')


class TaskSerializer(DynamicFieldsModelSerializer):
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, read_only=True, required=False)
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'order', 'assigned', 'started', 'due', 'completed',)


class SprintSerializer(DynamicFieldsModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'tasks')

    def validate_end(self, value):                
        if(value < date.today()): 
            msg = _('End date cannot be in the past.') 
            raise serializers.ValidationError(msg) 
        return attrs
from django.forms import ModelForm
from .models import Room, Topic
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        labels = {
            'name':'Create Topic'
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

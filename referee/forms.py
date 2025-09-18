from django import forms

from referee.models import Room, Fight


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', ]
        labels = {
            'name': 'Имя комнаты',
        }

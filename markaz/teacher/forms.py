from django import forms
from teacher.models import *


class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file']


class NotificationForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(widget=forms.TextInput(attrs={'class' : 'datepicker'}))

    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'scheduled_at']



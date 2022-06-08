from django import forms
from .models import *

class PresentForms(forms.ModelForm):
    group_student = forms.ModelChoiceField(queryset = Groups_students.objects.all(),
        widget=forms.Select(attrs={
            'class' : 'form-student',
            'name':'text4'
    }))
    present = forms.CharField(label="", widget=forms.TextInput(attrs={
        'placeholder' : 'Present:',
        'name':'text2'
    }))
   
    class Meta:
        model = Present
        fields = [
            "group_student",
            "present",
        ]


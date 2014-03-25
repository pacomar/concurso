#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from preguntas.models import *
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

class ComienzaForm(forms.Form):
	nombre = forms.CharField(label='Tu nombre', required=True)

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta   
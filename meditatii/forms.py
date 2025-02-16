from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Meditation



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'cnp_cui', 'email', 'nume_real', 'phone_number', 'company_name', 'user_type', 'password1', 'password2')# 'email', 'nume_real',

    def clean_cnp_cui(self):
        cnp_cui = self.cleaned_data.get('cnp_cui')
        if len(cnp_cui) <= 13:
            raise forms.ValidationError("CNP/CUI trebuie să aibă mai putin sau egal cu 13 caractere.")
        return cnp_cui

class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['student', 'date', 'payment_amount']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(user_type='student')



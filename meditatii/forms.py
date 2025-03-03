from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Meditation, Notes



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'cnp_cui', 'email', 'nume_real', 'phone_number', 'company_name', 'user_type', 'password1', 'password2')# 'email', 'nume_real',

    def clean_cnp_cui(self):
        cnp_cui = self.cleaned_data.get('cnp_cui')
        if len(cnp_cui) <= 13:
            raise forms.ValidationError("CNP/CUI trebuie să aibă mai putin sau egal cu 13 caractere.")
        return cnp_cui

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('student', 'title', 'note', 'date')
        widgets = {
            'student': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'title': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'note': forms.Textarea(attrs={
                'rows': 4,
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            })
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['student'].queryset = User.objects.filter(user_type='student')

class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['student', 'date', 'payment_amount']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm'
            }),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm'
            }),
            'payment_amount': forms.NumberInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(user_type='student')



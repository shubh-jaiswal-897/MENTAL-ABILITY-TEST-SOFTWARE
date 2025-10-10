from django import forms
from .models import ContactSubmission


class AnswerForm(forms.Form):
    choice = forms.IntegerField(widget=forms.RadioSelect, required=True)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter the subject'}),
            'message': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Enter your message'}),
        }




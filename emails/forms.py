from django import forms

from .models import Email

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = (
            '__all__'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['body'].initial = 'Hello,'
        self.fields['attachment'].required = False  # Set attachment field as not required
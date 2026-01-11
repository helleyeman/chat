from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    terms_agreement = forms.BooleanField(
        required=True,
        label="I agree that this app is for FRIENDLY social connections only. I will NOT share sexual content. I understand that violating these rules will result in an immediate ban."
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'gender', 'country', 'state', 'age', 'call_price']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}), # Render as select, populated by JS
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Gender is now self-declared and not locked by voting
        # if self.instance.pk and self.instance.is_gender_locked:
        #     self.fields['gender'].disabled = True
        #     self.fields['gender'].help_text = "Gender is verified by community voting and cannot be changed."
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("You must be at least 18 years old to use this app.")
        return age
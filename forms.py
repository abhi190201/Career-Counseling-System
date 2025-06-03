import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .validators import validate_password
from .models import CustomUser

from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User

# -------------------------------
# Custom Signup Form
# -------------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Enter your username',
            'email': 'Enter your email',
            'full_name': 'Enter your full name',
            'password1': 'Enter your password',
            'password2': 'Confirm your password',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})
            if field_name in ['username', 'email', 'full_name']:
                field.initial = ''

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already exists. Please choose another.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already registered. Please use another.')
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name:
            raise ValidationError('Full name is required.')
        if not re.match(r'^[A-Za-z\s]+$', full_name):
            raise ValidationError('Full name can only contain letters and spaces.')
        return full_name

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

# -------------------------------
# Custom Login Form
# -------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

# -------------------------------
# Profile Update Form
# -------------------------------
class ProfileForm(forms.ModelForm):
    GRADUATION_STREAM_CHOICES = [
        ("BSc Computer Science", "BSc Computer Science"),
        ("BSc IT", "BSc IT"),
        ("BCA", "BCA"),
        ("BTech Computer Science", "BTech Computer Science"),
        ("BTech IT", "BTech IT"),
        ("BE Computer Science", "BE Computer Science"),
        ("BE IT", "BE IT"),
        ("BSc Software Engineering", "BSc Software Engineering"),
        ("BSc Data Science", "BSc Data Science"),
        ("BSc AI & ML", "BSc AI & ML"),
        ("BSc Cybersecurity", "BSc Cybersecurity"),
        ("BTech AI & Data Science", "BTech AI & Data Science"),
        ("BTech Cybersecurity", "BTech Cybersecurity"),
        ("BSc Computer Applications", "BSc Computer Applications"),
        ("Other", "Other"),
    ]

    graduation_stream = forms.ChoiceField(choices=GRADUATION_STREAM_CHOICES, required=False)
    other_graduation_stream = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'profile_picture',
            'tenth_percentage',
            'twelfth_percentage',
            'graduation_percentage',
            'graduation_year',
            'graduation_stream',
            'resume',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'tenth_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'twelfth_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'graduation_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_stream = self.instance.graduation_stream
        if current_stream and current_stream not in dict(self.GRADUATION_STREAM_CHOICES):
            self.initial['graduation_stream'] = "Other"
            self.initial['other_graduation_stream'] = current_stream

    def clean_graduation_percentage(self):
        grad = self.cleaned_data.get('graduation_percentage')
        if grad is not None and (grad < 0 or grad > 100):
            raise ValidationError('Graduation Percentage must be between 0 and 100.')
        return grad



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'profile_picture'] # Add any other fields you want to include in the profile update form
        

from django import forms
from .models import InterestQuestion

class InterestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    ('option_a', question.option_a),
                    ('option_b', question.option_b),
                    ('option_c', question.option_c),
                    ('option_d', question.option_d)
                ],
                widget=forms.RadioSelect
            )

# forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['other_graduation_stream']
        widgets = {
            'other_graduation_stream': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your graduation stream manually'
            }),
        }

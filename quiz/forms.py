from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import PracticeMode
from django.contrib import messages

# professor 

class RegisterForm(UserCreationForm):
    class Meta: 
        model = get_user_model()
        fields = ('email','username','password1','password2')
        
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Email')    

class PracticeModeForm(forms.Form):
    TOPIC_CHOICES = [
        ('Limits','Limits'),
        ('Derivative of a function','Derivative of a function'),
        ('Derivatives of trigonometric functions','Derivative of trigonometric functions'),
        ('Derivatives of inverse trigonometric functions','Derivative of inverse trigonometric functions'),
        ('Derivatives of Logarithmic and exponential functions','Derivative of logarithmic and exponential functions'),
        ('Derivatives of Hyperbolic and inverse hyperbolic functions','Derivative of hyperbolic and inverse hyperbolic functions'),
        ('Implicit Differentiation','Implicit Differentiation'),
        ('Explicit Differentiation','Explicit Differentiation'),
        ('Higher Derivative','Higher Derivative'),
    ]
    
    topic = forms.ChoiceField(choices=TOPIC_CHOICES, label='Select Topic')
    num_questions = forms.IntegerField(min_value=1, max_value=50, label='Number of Questions')
    
    def __str__(self):
        return f'{self.user.username} - Topic: {self.topic}, Num Questions: {self.num_questions}'
    
# practice solo
class SoloPracticeModeForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('easy','Easy'),
        ('medium','Medium'),
        ('hard','Hard'),
    ]
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, label='Select Difficulty Level')
    num_questions = forms.IntegerField(min_value=1, max_value=50, label='Number of Questions')
    def __str__(self):
        return f'{self.user.username}, Difficulty: {self.difficulty}, Num Questions: {self.num_questions}'
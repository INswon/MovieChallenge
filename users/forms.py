from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ProgressGoalForm(forms.ModelForm):
    class Meta:
        model = ProgressGoal
        fields = ['goal_title', 'target_date', 'current_progress', 'total_movies', 'genre_preferences', 'status', 'movies_watched', 'movie_ratings']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),  # 日付入力を適切に設定
            'movies_watched': forms.Textarea(attrs={'rows': 4}),  # 映画リストを入力するテキストエリア
            'movie_ratings': forms.Textarea(attrs={'rows': 4}),  # 評価や感想を入力するテキストエリア
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProgressGoal

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
            'goal_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: 週に5本の映画を見る'
            }),
            'target_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'current_progress': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': '0',
                'required': True 
            }),
            'total_movies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '例: 10',
                'required': True 
            }),
            'genre_preferences': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: アクション, コメディ'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'movies_watched': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '例: タイトル1, タイトル2'
            }),
            'movie_ratings': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '例: タイトル1 - 評価: 4/5, 感想: 面白かった'
            }),
        }
        help_texts = {
            'goal_title': '目標のタイトルを入力してください。',
            'target_date': '目標を達成したい日付を選択してください。',
            'total_movies': '達成したい映画の本数を入力してください。',
        }

        def clean_total_movies(self):
            total_movies = self.cleaned_data.get('total_movies')
            if total_movies is None or total_movies <= 0:
                raise forms.ValidationError('目標の映画鑑賞数を1以上で設定してください。')
            return total_movies

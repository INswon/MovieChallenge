from django import forms
from .models import UserMovieRecord

class MovieRecordForm(forms.ModelForm):
    class Meta:
        model = UserMovieRecord
        fields = ['title', 'poster', 'rating', 'date_watched']
        widgets = {
            'date_watched': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'poster': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("タイトルを入力してください。")
        return title

    def clean_date_watched(self):
        date_watched = self.cleaned_data.get('date_watched')
        if not date_watched:
            raise forms.ValidationError("鑑賞日を入力してください。")
        return date_watched

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in range(1, 6):
            raise forms.ValidationError("評価は1から5の間で選択してください。")
        return rating

    def __init__(self, *args, **kwargs):
        super(MovieRecordForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['poster'].required = True
        self.fields['date_watched'].required = True
        self.fields['rating'].required = True
   
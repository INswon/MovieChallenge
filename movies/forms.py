from django import forms
from .models import UserMovieRecord

# 映画検索フォームの作成
class MovieSearchForm(forms.Form):
    movie_title = forms.CharField(max_length=100, label='映画タイトル', widget=forms.TextInput(attrs={'placeholder': '映画のタイトルを入力'}))

# 映画記録フォームの作成
class MovieRecordForm(forms.ModelForm):

    delete_poster = forms.BooleanField(required=False, label="ポスター画像を削除") 
    
    class Meta:
        model = UserMovieRecord
        fields = ['title', 'poster', 'rating', 'date_watched']
        widgets = {
            'date_watched': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'poster': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    # タイトルのバリデーション
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("タイトルを入力してください。")
        return title

    # 鑑賞日のバリデーション
    def clean_date_watched(self):
        date_watched = self.cleaned_data.get('date_watched')
        if not date_watched:
            raise forms.ValidationError("鑑賞日を入力してください。")
        return date_watched

    # 評価（1〜5）のバリデーション
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in range(1, 6):
            raise forms.ValidationError("評価は1から5の間で選択してください。")
        return rating
    
    # 保存時にポスター削除のチェックがあれば削除処理
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data.get("delete_poster"):
            if instance.poster:
                instance.poster.delete(save=False)
            instance.poster = None  

        if commit:
            instance.save()
        return instance
    
    # 必須項目の明示的な指定
    def __init__(self, *args, **kwargs):
        super(MovieRecordForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['poster'].required = False
        self.fields['date_watched'].required = True
        self.fields['rating'].required = True
   

from django import forms

from web.models import Game, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-input'}),
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'price', 'description', 'image')

from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    #PostForm:フォームの名前.
    #このフォームが ModelForm の一種だとDjangoに伝える必要があります (Djangoが私たちのためにいくつか魔法をかけられるように)。
    #forms.ModelFormがその役割を果たします。
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

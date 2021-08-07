from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':form.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')


        widgets = {
            'author':form.TextInput(attrs={'class':'textinputclass'}),
            'text': form.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


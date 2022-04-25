from django import forms
from django.contrib.auth.models import User
from blog.models import Post,Comment

class PostForm(forms.ModelForm):
    # author = forms.CharField(widget=forms.HiddenInput(), required=False)
    author = forms.ModelChoiceField(queryset= User.objects.all() , widget=forms.HiddenInput())
    
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            
            'title':forms.TextInput(attrs={'class':'textinputclass form-control'}),
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent form-control'})
        }

#   secretdocs = forms.ChoiceField(choices=[(doc.uid, doc.name) for doc in Document.objects.all()])
#   class Meta:
#       model = Documents
#       fields = ('secretdocs', )
#       widgets = {
#           'secretdocs': Select(attrs={'class': 'select'}),
#       }



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')


        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


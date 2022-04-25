from rest_framework import serializers
from blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # fields = ('author', 'title', 'text')
        fields = '__all__'




class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        # fields = ('author', 'text')
        fields = '__all__'
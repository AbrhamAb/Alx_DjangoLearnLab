from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'author',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)

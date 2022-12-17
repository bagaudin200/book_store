from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation
from rest_framework import serializers


class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rate = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author', 'likes_count', 'annotated_likes', 'rate')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rating')
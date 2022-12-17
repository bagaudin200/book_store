from django.test import TestCase
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')

        book_1 = Book.objects.create(name='Finish him', price=2500, author='Author 1')
        book_2 = Book.objects.create(name='Bullzai', price=2700, author='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rating=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rating=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rating=4)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rating=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rating=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rate=Avg('userbookrelation__rating')).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Finish him',
                'price': '2500.00',
                'author': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
                'rate': '4.67'
            },
        {
            'id': book_2.id,
            'name': 'Bullzai',
            'price': '2700.00',
            'author': 'Author 2',
            'likes_count': 2,
            'annotated_likes': 2,
            'rate': '3.50'
        },
        ]
        self.assertEqual(expected_data, data)
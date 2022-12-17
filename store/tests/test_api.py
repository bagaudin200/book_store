from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from django.contrib.auth.models import User
import json
from django.db.models import Count, Case, When, Avg

class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Finish him', price=2500, author='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Bullzai', price=2700, author='Author 5')
        self.book_3 = Book.objects.create(name='Rat Author 1', price=3500, author='Author 3')

        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, rating=5)

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rate=Avg('userbookrelation__rating')).order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rate'], '5.00')
        self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_get_filter(self):

        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rate=Avg('userbookrelation__rating')).order_by('id')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {"name": "Python 3",
                 "price": 150,
                 "author": "Mak Walberg",
                  }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {"name": self.book_1.name,
                "price": 575,
                "author": self.book_1.author}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {"name": self.book_1.name,
                "price": 575,
                "author": self.book_1.author}
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

class BookRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_1 = Book.objects.create(name='Finish him', price=2500, author='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Bullzai', price=2700, author='Author 5')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {"like": True,
                }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)
        data = {"in_bookmarks": True,
                }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {"rating": 3,
                }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(3, relation.rating)





from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer, UserBookRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from store.permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.db.models import Count, Case, When, Avg

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    # def get_queryset(self):
    #     queryset = Book.objects.all()
    #     item_name = self.request.query_params.get('price')
    #     if item_name:
    #         queryset = queryset.filter(price=item_name)
    #     return queryset

class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rate=Avg('userbookrelation__rating')).order_by('id')
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])

        return obj

def auth(request):
    return render(request, 'oauth.html')

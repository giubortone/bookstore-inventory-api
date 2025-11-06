from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDeleteView, CalculatePriceView, BookSearchByCategoryView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),
    path('books/<int:pk>/calculate-price/', CalculatePriceView.as_view(), name='calculate-price'),
    path('books/search/', BookSearchByCategoryView.as_view(), name='book-search-category'),

]

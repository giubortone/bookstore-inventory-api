from django.urls import path
from .views import (
    BooksView,
    BookDetailView,
    BookPriceView,
    BookSearchByCategoryView,
)

urlpatterns = [
    path("books/", BooksView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/calculate-price/", BookPriceView.as_view(), name="calculate-price"),
    path("books/search/", BookSearchByCategoryView.as_view(), name="book-search"),
]

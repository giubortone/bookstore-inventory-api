from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

import requests
from requests import RequestException, Timeout, HTTPError

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Book
from .serializers import BookSerializer

DEFAULT_EXCHANGE_RATE = Decimal(getattr(settings, "EXCHANGE_RATE_DEFAULT", "40"))
LOCAL_CURRENCY = getattr(settings, "LOCAL_CURRENCY", "VES")
EXCHANGE_API_URL = getattr(settings, "EXCHANGE_API_URL", "https://api.exchangerate-api.com/v4/latest/USD")
EXCHANGE_API_TIMEOUT = int(getattr(settings, "EXCHANGE_API_TIMEOUT", 5))


class BooksView(generics.ListCreateAPIView):
    """GET lista libros, POST crea uno."""
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    search_fields = ["title", "author", "isbn", "category"]
    ordering_fields = ["created_at", "updated_at", "title", "stock_quantity", "cost_usd"]
    ordering = ["-created_at"]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE por id."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookPriceView(views.APIView):
    """POST /api/books/{id}/calculate-price/ — calcula y guarda precio sugerido."""
    MARGIN_PERCENTAGE = 40  # según enunciado

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        cost_usd: Decimal = book.cost_usd

        # tasa desde API externa con fallback
        try:
            resp = requests.get(EXCHANGE_API_URL, timeout=EXCHANGE_API_TIMEOUT)
            resp.raise_for_status()
            data = resp.json() or {}
            rate_raw = data.get("rates", {}).get(LOCAL_CURRENCY)
            exchange_rate = Decimal(str(rate_raw)) if rate_raw is not None else DEFAULT_EXCHANGE_RATE
        except (Timeout, HTTPError, RequestException, ValueError, KeyError):
            exchange_rate = DEFAULT_EXCHANGE_RATE

        cost_local = (cost_usd * exchange_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        margin = Decimal("1") + (Decimal(self.MARGIN_PERCENTAGE) / Decimal("100"))
        selling_price_local = (cost_local * margin).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        book.selling_price_local = selling_price_local
        book.save(update_fields=["selling_price_local", "updated_at"])

        return Response({
            "book_id": book.id,
            "cost_usd": str(cost_usd),
            "exchange_rate": str(exchange_rate),
            "cost_local": str(cost_local),
            "margin_percentage": self.MARGIN_PERCENTAGE,
            "selling_price_local": str(selling_price_local),
            "currency": LOCAL_CURRENCY,
            "calculation_timestamp": timezone.now().isoformat(),
        }, status=status.HTTP_200_OK)


class BookSearchByCategoryView(generics.ListAPIView):
    """GET /api/books/search/?category=valor — búsqueda simple."""
    serializer_class = BookSerializer

    def get_queryset(self):
        category = self.request.query_params.get("category")
        if not category:
            raise ValidationError({"category": "El parámetro 'category' es obligatorio."})
        q = category.strip()
        return Book.objects.filter(
            Q(category__icontains=q) | Q(title__icontains=q) | Q(author__icontains=q)
        ).order_by("-created_at")



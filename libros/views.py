from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
import requests

from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    Lista todos los libros o crea uno nuevo

    GET  /api/books/      - Lista los libros
    POST /api/books/      - Crea un nuevo libro
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina un libro específico por id

    GET    /api/books/{id}/   - Obtiene el libro por su id
    PUT    /api/books/{id}/   - Actualiza todos los campos del libro
    PATCH  /api/books/{id}/   - Actualiza solo campos enviados del libro 
    DELETE /api/books/{id}/   - Elimina el libro por su id
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CalculatePriceView(views.APIView):
    """
    Calcula y actualiza el precio de venta de un libro

    POST /api/books/{id}/calculate-price/

    Proceso:
    - Obtiene la tasa de cambio USD → VES desde la API externa
    - Aplica un margen de ganancia del 40%
    - Actualiza el campo 'selling_price_local' del libro
    """
    DEFAULT_EXCHANGE_RATE = 40   # tasa por defecto
    MARGIN_PERCENTAGE = 40       # margen requerido

    def post(self, request, pk):
        """Realiza el cálculo de precio basado en la tasa de cambio y guarda el resultado."""
        # Verificar existencia del libro
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        cost_usd = float(book.cost_usd)

        # Obtener tasa de cambio
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
            if response.status_code != 200:
                raise Exception("API Error")

            data = response.json()
            exchange_rate = data["rates"].get("VES", self.DEFAULT_EXCHANGE_RATE)
        except Exception:
            exchange_rate = self.DEFAULT_EXCHANGE_RATE

        # Calcular valores
        cost_local = cost_usd * exchange_rate
        selling_price_local = cost_local * (1 + self.MARGIN_PERCENTAGE / 100)

        # Guardar resultado
        book.selling_price_local = selling_price_local
        book.save()

        return Response({
            "book_id": book.id,
            "cost_usd": cost_usd,
            "exchange_rate": exchange_rate,
            "cost_local": round(cost_local, 2),
            "margin_percentage": self.MARGIN_PERCENTAGE,
            "selling_price_local": round(selling_price_local, 2),
            "currency": "VES",
            "calculation_timestamp": timezone.now()
        }, status=status.HTTP_200_OK)


class BookSearchByCategoryView(generics.ListAPIView):
    """
    Busca libros filtrando por categoria

    GET /api/books/search/?category={categoria}
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')

        if not category:
            raise ValidationError({"category": "El parámetro 'category' es obligatorio"})

        return Book.objects.filter(category__icontains=category.strip())

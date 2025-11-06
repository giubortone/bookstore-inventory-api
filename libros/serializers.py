from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

    def validate_cost_usd(self, value):
        if value <= 0:
            raise serializers.ValidationError("El costo en USD debe ser mayor a 0$")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value

    def validate_isbn(self, value):
        cleaned = value.replace("-", "")
        if len(cleaned) not in (10, 13) or not cleaned.isdigit():
            raise serializers.ValidationError("El ISBN debe tener 10 o 13 dígitos")
        return value
    
    def validate(self, attrs):
        isbn = attrs.get("isbn")
        if isbn:
            qs = Book.objects.filter(isbn=isbn)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"isbn": "Ya existe un libro con este ISBN."})
        return attrs


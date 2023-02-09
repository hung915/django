from decimal import Decimal

from rest_framework import serializers

from .models import Collection, Product


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "collection"]

    # id = serializers.IntegerField()
    # title = serializers.CharField()
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # Relationship: Primary_key
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # Relationship: String -> Collection __str__
    # collection = serializers.StringRelatedField()

    # Relationship: Object
    # collection = CollectionSerializer()

    # Relationship: Hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="collection-detail"
    # )

    # def calculate_tax(self, product: Product):
    #     return product.unit_price * Decimal(1.1)

    # def validate(self, data):
    #     if data["password"] != data["confirm_password"]:
    #         return serializers.ValidationError("Passwords do not match")
    #     return data

# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Q, F
from django.db.models.aggregates import Sum, Count, Min, Max
from django.shortcuts import render

from store.models import Collection, Customer, Order, OrderItem, Product
from tags.models import TagItem


# Request handler (action)
def say_hello(request):
    # return HttpResponse("Hello World")
    # try:
    #     exists = Product.objects.filter(pk=0).exists()
    # except ObjectDoesNotExist:
    #     pass
    # for product in query_set:
    #     print(product)

    # Products: inventory < 10 and price < 20
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # Products: inventory < 10 or price < 20
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) & ~Q(unit_price__lt=20)
    # )

    # Products: inventory = price
    # query_set = Product.objects.filter(inventory=F("unit_price"))
    # query_set = Product.objects.values_list("id", "title", "collection__title")
    # product = Product.objects.order_by("unit_price", "-title")[0]
    # product = Product.objects.earliest("unit_price")
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values("product_id").distinct())

    # query_set = Product.objects.only("id", "title") # select only needed fields
    # query_set = Product.objects.defer("description") # exclude

    # select_related (1 product - 1 collection)
    # query_set = Product.objects.select_related("collection").all()

    # prefetch_related (1 product - n promotion)
    # query_set = Product.objects.prefetch_related("promotions").all()

    # query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]

    # result = Product.objects.aggregate(Count("id"))

    # query_set2 = Order.objects.filter(customer__id=1).all()
    query_set1 = Order.objects.filter(customer_id=2).all()

    total_orders = Order.objects.aggregate(Count("id"))
    product_1_sold = OrderItem.objects.filter(
        product_id__in=Product.objects.filter(id=1)
    ).aggregate(Sum("quantity"))
    # product_1_sold = OrderItem.objects.filter(product_id__in=Product.objects.filter(id=1).values("id")).aggregate(Count("id"))
    customer_1_orders = Order.objects.filter(
        customer_id__in=Customer.objects.filter(id=1)
    ).aggregate(Count("id"))
    min_price = Product.objects.filter(
        collection_id__in=Collection.objects.filter(id=3)
    ).aggregate(Min("unit_price"))

    # content_type = ContentType.objects.get_for_model(Product)

    # query_set = TagItem.objects.select_related("tag").filter(
    #     content_type=content_type,
    #     object_id=1
    # )
    query_set = TagItem.objects.get_tags_for(Product, 1)

    # collection = Collection.objects.get(pk=12)
    # collection.title = "Games A"
    # collection.featured_product_id = 2
    # collection.featured_product = Product(id=1)
    # collection.save()

    Collection.objects.filter(id=12).update(featured_product_id=None)

    # collection = Collection.objects.create(name="abc", featured_product_id=1)


    return render(
        request, "hello.html", {"name": "Mosh", "tags": list(query_set)}
    )

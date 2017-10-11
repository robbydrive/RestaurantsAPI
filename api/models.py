from django.db import models, IntegrityError
from django.contrib.auth.models import User


class APIMixin(object):
    """
    Interface indicating models used as resources for API GET endpoints
    Provides get_dict(self) method used to get dictionary representation
    suitable for transforming into JSON
    """
    def get_dict(self):
        raise NotImplementedError


class Category(models.Model, APIMixin):
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Category name")

    def get_dict(self):
        subs_queryset = Category.objects.filter(parent__pk=self.pk)
        dishes_queryset = Dish.objects.filter(category=self)
        d = Category.objects.filter(pk=self.pk).values('id', 'name')[0]
        d['type'] = 'categories'
        d['children'] = []
        for sub_category in subs_queryset:
            d['children'].append(sub_category.get_dict())
        for dish in dishes_queryset:
            d['children'].append(dish.get_dict())
        return d

    class Meta:
        permissions = (
            ('view_categories', 'Can view current menu (categories)'),
            ('create_categories', 'Can create new categories'),
            ('edit_categories', 'Can edit created categories'),
        )


class Dish(models.Model, APIMixin):
    name = models.CharField(max_length=250, verbose_name="Dish name")
    price = models.IntegerField(verbose_name="Dish price")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def get_dict(self):
        d = Dish.objects.filter(pk=self.pk).values('id', 'name', 'price')[0]
        d['type'] = 'dishes'
        return d


class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name="Restaurant name")
    address = models.CharField(max_length=300, verbose_name="Restaurant address")


class Order(models.Model, APIMixin):
    UNPAID = 'DUE'
    PAID = 'OK'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid'),
        (CANCELLED, 'Cancelled'),
    ]

    creation_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNPAID)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING, null=False)
    operator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    dishes = models.ManyToManyField(Dish, through='OrderDish')

    def get_dict(self):
        d = Order.objects.filter(pk=self.pk).values('id', 'status', 'restaurant', 'operator')[0]
        d.update({
            'type': 'orders',
            'dishes': []
        })
        for dish in OrderDish\
                    .objects\
                    .filter(order_id=self.pk)\
                    .select_related('dish')\
                    .values('dish__id', 'dish__name', 'fact_price'):
            dish.update({
                'type': 'dishes'
            })
            d['dishes'].append(dish)
        return d

    @classmethod
    def create_from_payload(cls, payload, user):
        """
        Creates new Order and OrderDish instances from raw data
        :param payload: dict (usually - request's body)
        :param user: user that created the order
        :return: created Order instance
        """
        try:
            new_order = Order.objects.create(
                restaurant=Restaurant.objects.get(pk=payload.get('restaurant_id', None)),
                operator=user
            )
        except IntegrityError:
            return None
        for dish in payload.get('dishes', []):
            try:
                OrderDish.objects.create(order=new_order,
                                         dish=Dish.objects.get(pk=dish.get('id', None)),
                                         fact_price=dish.get('price', None))
            except IntegrityError:
                new_order.delete()
                return None
        return new_order


    class Meta:
        permissions = (
            ('create_orders', 'Can create new orders'),
            ('view_orders', 'Can view orders'),
            ('edit_orders', 'Can edit created orders'),
        )


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish)
    fact_price = models.IntegerField(verbose_name="Dish price at order creation time")
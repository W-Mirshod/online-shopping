from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify

from shopping.managers import CustomUserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(BaseModel):
    class Ratings(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    rating = models.IntegerField(choices=Ratings.choices, default=Ratings.ZERO.value)
    quantity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=False)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.slug:
            i = 1
            while True:
                new_slug = f"{slugify(self.name)}-{i}"
                if not Product.objects.filter(slug=new_slug).exists():
                    self.slug = new_slug
                    break
                i += 1

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=150, default='N/A', blank=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.name


class Comment(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField()
    is_accessible = models.BooleanField(default=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    birth_of_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

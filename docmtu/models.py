import datetime
import hashlib

from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=60)
    portion = models.CharField(max_length=15)
    calories = models.IntegerField()
    hash = models.CharField(max_length=16, unique=True, primary_key=True, editable=False, default='')

    def __str__(self):
        return self.name

    def __hash__(self):
        return hashlib.md5(f"{self.name}{self.portion}".encode()).hexdigest()[:16]

    def to_dict(self):
        return {
            'name': self.name,
            'portion': self.portion,
            'calories': self.calories
        }


class MenuCategory(models.Model):
    name = models.CharField(max_length=50)
    category_id = models.CharField(max_length=24, editable=False, default='')
    items = models.ManyToManyField('MenuItem', related_name='categories')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.category_id,
            'items': [item.to_dict() for item in self.items.all()]
        }


class MenuPeriod(models.Model):
    period_id = models.CharField(max_length=24, editable=False)
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField('MenuCategory', related_name='periods')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.period_id,
            'name': self.name,
            'categories': [category.to_dict() for category in self.categories.all() if len(category.items.all()) > 0]
        }


class DiningLocation(models.Model):
    location_id = models.CharField(max_length=24, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    menus = models.ManyToManyField('Menu', related_name='locations')

    def __str__(self):
        return self.name


class Menu(models.Model):
    date = models.DateField()
    closed = models.BooleanField(default=False)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    periods = models.ManyToManyField('MenuPeriod', related_name='menus')
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date}'

    def is_open(self):
        if self.closed:
            return False
        now = datetime.datetime.now().time()
        if self.opening_time and self.closing_time:
            return self.opening_time <= now <= self.closing_time
        return False

    def to_dict(self):
        return {
            'date': self.date,
            'periods': [period.to_dict() for period in self.periods.all()],
            'closed': self.closed,
            'opening_time': self.opening_time.strftime('%I:%M %p') if self.opening_time else None,
            'closing_time': self.closing_time.strftime('%I:%M %p') if self.closing_time else None,
            'is_open': self.is_open(),
            'today': self.date == datetime.datetime.now().date()
        }


class Change(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='changes')
    change = models.TextField()

    def __str__(self):
        return f'{self.menu.date} - {self.change}'

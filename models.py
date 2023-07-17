from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class Tariff(Model):
    date = fields.DateField(default=datetime.today())
    cargo_type = fields.CharField(max_length=150)
    rate = fields.FloatField()

    def __str__(self):
        return f"{self.rate}, {self.cargo_type}"


class Cargo(Model):
    name = fields.CharField(max_length=100, unique=True)
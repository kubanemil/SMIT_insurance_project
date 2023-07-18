from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class Cargo(Model):
    name = fields.CharField(max_length=100, unique=True)


class Tariff(Model):
    date = fields.DateField(default=datetime.today())
    cargo_type = fields.ForeignKeyField('models.Cargo', related_name='tariff', on_delete='CASCADE')
    rate = fields.FloatField()

    def __str__(self):
        return f"{self.rate}, {self.cargo_type}"

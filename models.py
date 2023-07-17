from tortoise import fields
from tortoise.models import Model


class Cargo(Model):
    name = fields.CharField(max_length=150)
    rate = fields.FloatField()

    def __str__(self):
        return f"{self.type}, {self.rate}"
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_str_to_dollars(self):
        return f"{self.price:.2f}"

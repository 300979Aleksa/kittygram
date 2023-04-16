from django.db import models

class Cat(models.Model):
    class Meta:
        db_table = 'cats'

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=25)
    birth_year = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name}, {self.color}'
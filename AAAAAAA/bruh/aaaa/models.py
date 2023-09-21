from collections.abc import Iterable
from django.db import models

# Create your models here.

class User(models.Model):
    pass

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE, null=False)

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    duration = models.BigIntegerField()
    productID = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def to_dict(self):
        return{
            'lesson_name': self.name
        }

class Status(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    timecode = models.BigIntegerField()
    isWathed = models.BooleanField(default=False)
    timestamp = models.BigIntegerField()

    def save(self, *args, **kwargs):
        
        border = self.lesson.duration * 0.8

        if self.timecode > border:
            self.isWathed = True
        
        super(Status, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'lesson')

class Access(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
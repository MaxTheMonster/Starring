from django.db import models
from django.template.defaultfilters import slugify


class Person(models.Model):
    name = models.CharField(max_length=128)
    stars = models.IntegerField(default=5)
    slug = models.SlugField(default="slug")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Person, self).save(*args, **kwargs)



class Rating(models.Model):
    stars = models.IntegerField()
    name = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.rating

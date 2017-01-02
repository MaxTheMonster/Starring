from django.db import models
from django.template.defaultfilters import slugify


class Person(models.Model):
    name = models.CharField(max_length=128)
    stars = models.DecimalField(default=5, decimal_places=2, max_digits=4)
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
        return str(self.stars)

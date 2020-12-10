from django.conf import settings
from django.db import models
from django.urls import reverse

class Character(models.Model):

    name = models.CharField(max_length=100, blank=True)

    race = models.CharField(max_length=100, default="Dwarf", blank=True)

    advantage = models.IntegerField(default=0)

    disadvantage = models.IntegerField(default=0)

    shock = models.IntegerField(default=0)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    data = models.BinaryField(blank=True)

    def __str__(self):

        if self.name:
            return self.name
        else:
            return "<No Name>"

    def get_absolute_url(self):

        return reverse('strata:edit', kwargs={'pk': self.pk})

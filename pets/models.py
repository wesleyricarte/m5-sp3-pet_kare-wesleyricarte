from django.db import models


class Sex(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )

    group = models.ForeignKey(
        "groups.Group",
        related_name="pets",
        on_delete=models.PROTECT,
        null=True,
    )

    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="pets"
    )

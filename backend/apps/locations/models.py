from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    currency_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("country", "name")

    def __str__(self) -> str:
        return f"{self.name}, {self.country.name}"


class Town(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="towns")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("city", "name")

    def __str__(self) -> str:
        return f"{self.name}, {self.city.name}"

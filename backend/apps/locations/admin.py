from django.contrib import admin

from .models import City, Country, Town


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "currency_code")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    list_filter = ("city__country",)

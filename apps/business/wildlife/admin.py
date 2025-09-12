from django.contrib import admin
from .models import ConservationStatus, Specie, Animal, Habitat

# Register your models here.
admin.site.register(ConservationStatus)
admin.site.register(Specie)
admin.site.register(Animal)


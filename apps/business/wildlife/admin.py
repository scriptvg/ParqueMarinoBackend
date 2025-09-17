from django.contrib import admin
from .models import (
    Animal, ConservationStatus, Habitat, Specie
)

# Register your models here.
admin.site.register(Animal)
admin.site.register(ConservationStatus)
admin.site.register(Habitat)
admin.site.register(Specie)

from django.db import models


class Sections(models.Model):
  name = models.CharField(max_length=30, unique=True, null=False, verbose_name="Section Name")
  
  class Meta:
      verbose_name = "Section"
      verbose_name_plural = "Sections"
      ordering = ["name"]
      
  def __str__(self):
     return self.name

  @property
  def num_habitats(self):
    return self.habitats.count()
  
class Habitats(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, verbose_name="Habitat Name")
    nums_animals = models.PositiveIntegerField(null=False, verbose_name="Number of Animals")
    description = models.CharField(max_length=100, null=False, verbose_name="Description")
    section = models.ForeignKey('Sections', on_delete=models.CASCADE, related_name='habitats')

    class Meta:
        verbose_name = "Habitat"
        verbose_name_plural = "Habitats"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    @property
    def num_animals(self):
        return self.animals.count()


from django.db import models

class Clothes(models.Model):
    cloth_name = models.CharField(max_length=200)
    cloth_var = models.CharField(max_length=200)
    cloth_col_1 = models.CharField(max_length=200)
    cloth_col_2 = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.cloth_name} {self.cloth_var} {self.cloth_col_1} {self.cloth_col_2}'


# Create your models here.

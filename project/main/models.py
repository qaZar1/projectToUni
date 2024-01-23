from django.db import models

# Create your models here.

class Relevance(models.Model):
    title = models.CharField('Название')
    table = models.TextField('Таблица')
    img = models.ImageField('График', upload_to='relevance/img')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'

class Geography(models.Model):
    title = models.CharField('Название')
    table = models.TextField('Таблица')
    img = models.ImageField('График', upload_to='geography/img')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'География'
        verbose_name_plural = 'Географии'

class Skills(models.Model):
    title = models.CharField('Название')
    table = models.TextField('Таблица')
    img = models.ImageField('График', upload_to='skills/img')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

from django.db import models
from django.urls import reverse
from datetime import timedelta, date
from django.utils.timezone import now
class Region(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название региона')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True,)
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('terminals', kwargs={'region_id': self.slug})



class Terminal(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название терминала')
    photo = models.ImageField(verbose_name='Фото здания терминала', blank=True, null=True, upload_to='terminals/')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Регион', related_name='terminals')
    address = models.TextField(verbose_name='Адрес терминала')
    rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Аренда", default=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')

    def __str__(self):
        return self.name


class Incassation(models.Model):
    terminal = models.ForeignKey(
        Terminal, 
        on_delete=models.CASCADE, 
        verbose_name="Терминал", 
        related_name="incassations"
    )
    last_collected = models.DateField(
        verbose_name="Дата последней инкассации", 
        default=now
    )
    interval_days = models.PositiveIntegerField(
        verbose_name="Интервал дней для инкассации", 
        default=30
    )
    next_collection = models.DateField(
        verbose_name="Дата следующей инкассации", 
        blank=True, 
        null=True
    )

    def save(self, *args, **kwargs):
        # Автоматически вычисляем дату следующей инкассации только если она не задана
        if self.last_collected and (not self.next_collection or self.next_collection <= self.last_collected):
            self.next_collection = self.last_collected + timedelta(days=self.interval_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Инкассация для {self.terminal.name}"

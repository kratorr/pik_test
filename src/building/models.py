from django.db import models


class Building(models.Model):
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес'
    )
    construction_year = models.PositiveIntegerField(
        verbose_name="Год постройки",
        db_index=True
    )

    def __str__(self):
        return f"{self.address}"


class BricksTask(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='brick_tasks',
        verbose_name='Задание на кладку'
    )
    count = models.PositiveIntegerField(verbose_name='Количество кирпичей')
    date = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return f"{self.building}, кол-во кирпичей {self.count}"

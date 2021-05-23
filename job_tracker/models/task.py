from datetime import date

from django.db import models

from job_tracker.models.action import Action


class Task(models.Model):
    """Задача."""

    actions = models.ManyToManyField(
        Action,
        blank=True,
        verbose_name='Действия'
    )

    job_day = models.DateField(
        default=date.today,
        verbose_name='Рабочий день'
    )

    name = models.CharField(
        max_length=128,
        verbose_name='Название'
    )

    time = models.DurationField(
        verbose_name='затраченное время'
    )

    def __str__(self):
        return 'Task{{id:{0}, name:{1}, time:{2}}}'.format(
            self.id, self.name, self.time
        )

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

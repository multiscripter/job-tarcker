from django.db import models


class Action(models.Model):
    """Действие."""

    text = models.CharField(
        max_length=128,
        verbose_name='Действие'
    )

    def __str__(self):
        return 'Action{{id:{0}, text:{1}}}'.format(self.id, self.text)

    class Meta:
        db_table = 'actions'
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'

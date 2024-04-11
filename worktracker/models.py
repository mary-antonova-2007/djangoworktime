from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    designation = models.CharField(max_length=100, verbose_name='Обозначение проекта')
    name = models.CharField(max_length=200, verbose_name='Наименование проекта')

    def __str__(self):
        return f"{self.designation} - {self.name}"


class Product(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name='Наименование изделия')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('paused', 'На паузе'),
        ('completed', 'Завершена'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    task_type = models.CharField(max_length=100, verbose_name='Тип задачи')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Статус')

    def __str__(self):
        product_str = f" - {self.product}" if self.product else ""
        return f"{self.task_type} - {self.project}{product_str}"


class TimeStamp(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timestamps')
    start_time = models.DateTimeField(verbose_name='Время начала выполнения')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Время окончания выполнения')

    def __str__(self):
        return f"Задача: {self.task.id}, Начало: {self.start_time}, Окончание: {self.end_time}"

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

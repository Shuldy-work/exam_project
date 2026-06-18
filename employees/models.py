from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    position = models.CharField(max_length=100, verbose_name="Должность")
    hire_date = models.DateField(verbose_name="Дата приёма")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    def clean(self):
        if not self.full_name or self.full_name.strip() == '':
            raise ValidationError({'full_name': 'Полное имя не может быть пустым.'})
        if not self.position or self.position.strip() == '':
            raise ValidationError({'position': 'Должность не может быть пустой.'})
        if self.hire_date and self.hire_date > date.today():
            raise ValidationError({'hire_date': 'Дата приёма не может быть в будущем.'})
        if self.salary <= 0:
            raise ValidationError({'salary': 'Зарплата должна быть больше 0.'})
        if '@' not in self.email:
            raise ValidationError({'email': 'Введите корректный email с символом @.'})
        # Проверка уникальности email (дополнительно, хотя unique=True уже есть)
        if Employee.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError({'email': 'Сотрудник с таким email уже существует.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
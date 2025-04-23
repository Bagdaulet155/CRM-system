from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.conf import settings

# Custom User моделі
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='manager',
        verbose_name=_('User Type')
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='custom_user_groups',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions',
        related_query_name='custom_user',
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# CustomUser қолдану үшін:
User = get_user_model()


class LogEntry(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='custom_log_entries'  
    )



class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Client Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    address = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Address'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))  # Автоматическое заполнение текущей даты и времени
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_clients', 
        verbose_name=_('Created By')
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def average_rating(self):
        """Возвращает среднюю оценку для клиента, если есть отзывы"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return None


class Deal(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('rejected', _('Rejected')),
    ]
    
    created_by = models.ForeignKey(
    CustomUser,
    on_delete=models.SET_NULL,
    null=True,
    related_name='created_deals',
    verbose_name=_('Created By')
)


    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='deals', verbose_name=_('Client'))
    title = models.CharField(max_length=255, verbose_name=_('Deal Title'))
    description = models.TextField(verbose_name=_('Description'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    document = models.FileField(upload_to='deal_documents/%Y/%m/%d/', null=True, blank=True, verbose_name=_('Document'))
    image = models.ImageField(upload_to='deal_images/%Y/%m/%d/', null=True, blank=True, verbose_name=_('Image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', verbose_name=_('Status'))
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assigned_deals', verbose_name=_('Assigned To'))

    # Таңдаулылар
    favorites = models.ManyToManyField(User, related_name='favorite_deals', blank=True, verbose_name=_('Favorites'))

    class Meta:
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Deal'))
    task_description = models.TextField(verbose_name=_('Description'))
    due_date = models.DateTimeField(verbose_name=_('Due Date'))
    completed = models.BooleanField(default=False, verbose_name=_('Completed'))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name=_('Priority'))
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', verbose_name=_('Assigned To'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['completed']),
            models.Index(fields=['due_date']),
        ]

class ClientReview(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User моделін алып келеді
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name=_("Оценка (1–5)")
    )
    comment = models.TextField(verbose_name=_("Комментарий"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        constraints = [
            models.UniqueConstraint(fields=['client', 'user'], name='unique_review_per_client_user')
        ]

    def __str__(self):
        return f"{self.client.name} - {self.rating}★"

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Отправитель"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name="Получатель"
    )
    content = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Сообщение от {self.sender} для {self.receiver} от {self.created_at}"

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Отправитель"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name="Получатель"
    )
    content = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Сообщение от {self.sender} для {self.receiver} от {self.created_at}"
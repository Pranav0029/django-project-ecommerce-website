from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    current_user = models.CharField(max_length=1, default='N')  # ✅ NEW COLUMN
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

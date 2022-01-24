from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Accounts(models.Model):
    name = models.CharField(max_length=20, null=None)    
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    date_created = models.DateField(auto_now_add=True)
    api = models.ForeignKey("TelegramApp", on_delete=models.CASCADE, related_name="api", null=False)


    def __str___(self):
        return self.name, self.phone, self.api


class TelegramApp(models.Model):
    name = models.CharField(max_length=20, null=None)
    api_id = models.CharField(max_length=200, unique=True)
    api_hash = models.CharField(max_length=200, unique=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name